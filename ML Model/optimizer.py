import json
import os
from estimator import estimate_priority
import joblib
model = joblib.load("priority_model.pkl")


INTERFACE = "wlan0"   # interface facing ESP32

# Clear old rules
os.system(f"sudo tc qdisc del dev {INTERFACE} root 2>/dev/null")

# Root qdisc
os.system(f"sudo tc qdisc add dev {INTERFACE} root handle 1: htb default 30")

# Classes
os.system(f"sudo tc class add dev {INTERFACE} parent 1: classid 1:10 htb rate 6mbit ceil 8mbit")   # HIGH
os.system(f"sudo tc class add dev {INTERFACE} parent 1: classid 1:20 htb rate 3mbit ceil 4mbit")   # MEDIUM
os.system(f"sudo tc class add dev {INTERFACE} parent 1: classid 1:30 htb rate 500kbit ceil 1mbit") # LOW

# Load ESP32 metrics
with open("metrics.json", "r") as f:
    data = json.load(f)

devices = data.get("devices", [])

print("\nApplying optimization:\n")

for d in devices:
    # --- Baseline metric estimation (dummy except RSSI) ---
    metrics = {
        "rssi": d["rssi"],
        "throughput": 3.0,     # dummy Mbps
        "rtt": 60,             # dummy ms
        "loss": 1,             # dummy %
        "congestion": False
    }

    priority = estimate_priority(metrics)

    if priority == "HIGH":
        classid = "1:10"
    elif priority == "MEDIUM":
        classid = "1:20"
    else:
        classid = "1:30"

    print(f"{d['mac']} → RSSI {d['rssi']} → {priority}")

    os.system(
        f"sudo tc filter add dev {INTERFACE} protocol ip parent 1: "
        f"prio 1 u32 match u16 0x0800 0xffff at -2 flowid {classid}"
    )

print("\nBaseline optimization applied.\n")
