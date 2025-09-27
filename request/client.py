# client.py
import argparse
import asyncio
import time
import random
import string

import grpc
import user_pb2
import user_pb2_grpc

def random_name():
    return ''.join(random.choices(string.ascii_letters, k=8))

def random_address():
    return f"{random.randint(1,999)} Example St."

def random_gender():
    return random.choice(["M", "F", "Other"])

def random_age():
    return random.randint(1, 90)

async def worker(name, stub, end_time, counters, worker_id):
    # counters: dict with 'total', 'minute', 'errors'
    while time.time() < end_time:
        req = user_pb2.UserRequest(
            name=random_name(),
            address=random_address(),
            gender=random_gender(),
            age=random_age()
        )
        try:
            start = time.time()
            resp = await stub.Process(req, timeout=10)  # 10s timeout per RPC
            latency = (time.time() - start)
            # update counters (safe in asyncio single-thread)
            counters['total'] += 1
            counters['minute'] += 1
        except Exception as e:
            counters['errors'] += 1
            # optional: print("request error:", e)
            await asyncio.sleep(0)  # yield
    # worker done
    return

async def reporter(counters, duration):
    elapsed = 0
    while elapsed < duration:
        # sleep until next minute or until finish whichever first
        to_sleep = min(60, duration - elapsed)
        await asyncio.sleep(to_sleep)
        elapsed += to_sleep
        # report minute count
        print(f"[report] minute elapsed: {elapsed//60} | replies in last window: {counters['minute']}, total so far: {counters['total']}, errors: {counters['errors']}")
        # reset minute counter
        counters['minute'] = 0

async def run(target, concurrency, duration):
    counters = {'total': 0, 'minute': 0, 'errors': 0}
    end_time = time.time() + duration

    async with grpc.aio.insecure_channel(target) as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        # spawn workers equal to concurrency
        workers = [asyncio.create_task(worker(f"w{i}", stub, end_time, counters, i)) for i in range(concurrency)]
        # spawn reporter
        rep_task = asyncio.create_task(reporter(counters, duration))
        # wait for workers to finish
        await asyncio.gather(*workers)
        # ensure reporter finishes
        await rep_task

    # final summary
    print("=== FINAL ===")
    print(f"Total successful replies: {counters['total']}")
    print(f"Total errors: {counters['errors']}")
    if duration > 0:
        rps = counters['total'] / duration
        rpm = rps * 60
        print(f"Average RPS: {rps:.2f}, Average RPM: {rpm:.2f}")

def parse_args():
    p = argparse.ArgumentParser(description="gRPC parallel client tester")
    p.add_argument("--target", default="127.0.0.1:50051", help="target host:port")
    p.add_argument("--concurrency", "-c", type=int, default=50, help="number of parallel workers")
    p.add_argument("--duration", "-d", type=int, default=60, help="duration in seconds")
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()
    try:
        asyncio.run(run(args.target, args.concurrency, args.duration))
    except KeyboardInterrupt:
        print("Interrupted by user")

