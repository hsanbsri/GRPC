const cpuEl = document.getElementById("cpu");
const server2El = document.getElementById("server2");

async function updateStatus() {
    try {
        let res = await fetch("http://localhost:5000/status");
        let data = await res.json();
        cpuEl.innerText = data.cpu_avg.toFixed(1) + "%";
        server2El.innerText = data.cpu_avg > 80 ? "ON" : "OFF";
    } catch (err) {
        cpuEl.innerText = "Error";
        server2El.innerText = "-";
    }
}

setInterval(updateStatus, 5000);
updateStatus();
