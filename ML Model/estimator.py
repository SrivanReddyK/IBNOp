import time
import random
import json

# SIMULATED NETWORK METRICS 
def generate_dummy_metrics():
    return {
        "bandwidth": {
            "throughput_per_device": {
                "device_1": round(random.uniform(0.5, 2.0), 2),   # Mbps
                "device_2": round(random.uniform(1.5, 4.0), 2),
                "device_3": round(random.uniform(4.0, 8.0), 2)
            }
        },

        "latency": {
            "ping": random.randint(20, 80),   # ms
            "rtt": random.randint(30, 120)    # ms
        },

        "reliability": {
            "packet_loss": round(random.uniform(0, 8), 2),  # %
            "jitter": random.randint(2, 15)                 # ms
        },

        "load": {
            "queue_length": random.randint(5, 25),
            "congestion": round(random.uniform(0.2, 0.95), 2)
        },

        "device_info": {
            "device_1": {"app_type": "chat", "priority": "high", "usage_pattern": "burst"},
            "device_2": {"app_type": "video", "priority": "medium", "usage_pattern": "continuous"},
            "device_3": {"app_type": "download", "priority": "low", "usage_pattern": "heavy"}
        }
    }


# --------------------------------------------------
# NETWORK STATE DETECTION
# --------------------------------------------------

def detect_network_state(metrics):
    if (
        metrics["latency"]["rtt"] > 90 or
        metrics["reliability"]["packet_loss"] > 5 or
        metrics["load"]["congestion"] > 0.7
    ):
        return "CONGESTED"
    return "NORMAL"


# --------------------------------------------------
# AUTOMATIC INTENT INFERENCE
# --------------------------------------------------

def infer_intent(metrics):
    if metrics["latency"]["rtt"] > 90:
        return "LOW_LATENCY"
    elif metrics["reliability"]["packet_loss"] > 5:
        return "HIGH_RELIABILITY"
    else:
        return "FAIRNESS"


# --------------------------------------------------
# PER-DEVICE ANALYSIS
# --------------------------------------------------

def analyze_devices(metrics):
    heavy_devices = []
    priority_devices = []

    for device, bw in metrics["bandwidth"]["throughput_per_device"].items():
        if bw > 4.5:
            heavy_devices.append(device)

    for device, info in metrics["device_info"].items():
        if info["priority"] == "high":
            priority_devices.append(device)

    return heavy_devices, priority_devices


# --------------------------------------------------
# OPTIMIZATION DECISION
# --------------------------------------------------

def generate_decision(intent, heavy_devices, priority_devices):
    if intent == "LOW_LATENCY":
        return {
            "throttle_devices": heavy_devices,
            "prioritize_devices": priority_devices
        }

    if intent == "HIGH_RELIABILITY":
        return {
            "reduce_packet_loss_for": priority_devices
        }

    return {
        "fair_bandwidth_distribution": "all_devices"
    }


# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

def main():
    print("\n🚀 Raspberry Pi Network Analyzer (Dummy Test)\n")

    while True:
        metrics = generate_dummy_metrics()

        network_state = detect_network_state(metrics)
        intent = infer_intent(metrics)
        heavy_devices, priority_devices = analyze_devices(metrics)
        decision = generate_decision(intent, heavy_devices, priority_devices)

        print("📊 Network Metrics:")
        print(json.dumps(metrics, indent=2))
        print("\n🧠 Network State:", network_state)
        print("🎯 Inferred Intent:", intent)
        print("⚙️ Optimization Decision:")
        print(json.dumps(decision, indent=2))
        print("=" * 70)

        time.sleep(5)


# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    main()
