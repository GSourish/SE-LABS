import json
from datetime import datetime

# Global state
meters = {}
RATE_TIER_1 = 3.5
RATE_TIER_2 = 5.0
RATE_TIER_3 = 7.5
SPIKE_LIMIT = 500

def record_reading(meter_id, units, history=None):
    if history is None:
        history = []
    
    # Optional safety check: Prevent cumulative consumption from dropping below zero
    current_total = meters.get(meter_id, 0)
    if current_total + units < 0:
        print(f"Warning: Reading results in negative consumption for {meter_id}. Resetting to 0.")
        units = -current_total  # Adjust units so total becomes 0

    history.append((meter_id, units, str(datetime.now())))
    meters[meter_id] = current_total + units
    return history

def compute_bill(meter_id, tier_rates):
    units = meters.get(meter_id, 0)
    if units <= 100:
        return units * tier_rates[0]
    elif units <= 300:
        return (100 * tier_rates[0]) + ((units - 100) * tier_rates[1])
    else:
        return (100 * tier_rates[0]) + (200 * tier_rates[1]) + ((units - 300) * tier_rates[2])

def raise_rates(percent):
    global RATE_TIER_1, RATE_TIER_2, RATE_TIER_3
    RATE_TIER_1 *= (1 + percent / 100)
    RATE_TIER_2 *= (1 + percent / 100)
    RATE_TIER_3 *= (1 + percent / 100)

def flag_spikes():
    spikes = []
    for m in meters:
        if meters[m] > SPIKE_LIMIT:
            spikes.append(m)
    return spikes

def load_meter_data(file="meters.json"):
    global meters
    try:
        with open(file, "r") as f:
            meters = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        meters = {}

def save_meter_data(file="meters.json"):
    with open(file, "w") as f:
        json.dump(meters, f, indent=4)

def main():
    record_reading("M-01", 120)
    record_reading("M-02", 640)
    h = record_reading("M-03", -50)
    print("Readings stored so far:", len(h))
    
    raise_rates(10)
    rates = [RATE_TIER_1, RATE_TIER_2, RATE_TIER_3]
    print("Bill M-01: %.2f" % compute_bill("M-01", rates))
    print("Bill M-03: %.2f" % compute_bill("M-03", rates))
    print("Spikes:", flag_spikes())
    
    # Safe input handling replacing insecure eval()
    adjustment_input = input("Extra units for M-01 (Enter for 0): ").strip()
    try:
        adjustment = float(adjustment_input) if adjustment_input else 0.0
    except ValueError:
        print("Invalid input entered. Defaulting to 0.")
        adjustment = 0.0
        
    record_reading("M-01", adjustment)
    save_meter_data()
    load_meter_data()
    print("Bill M-01 after reload: %.2f" % compute_bill("M-01", rates))

if __name__ == "__main__":
    main()