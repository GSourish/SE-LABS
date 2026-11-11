def lookup_drink_code(code):
    if not isinstance(code, str) or not code.strip():
        print("Error: Invalid or empty drink code provided.")
        return None
    menu = {"LAT": 4.0, "CAP": 3.5, "ESP": 3.0}
    cleaned_code = code.strip().upper()
    price = menu.get(cleaned_code)
    if price is not None:
        print(f"Base Price: $ {price}")
    else:
        print(f"Unknown drink code: {cleaned_code}")
    return price

def calculate_average_shot_cost(csv_prices):
    if not isinstance(csv_prices, str) or not csv_prices.strip():
        print("Error: Invalid or empty price list provided.")
        return 0.0
    try:
        prices = [float(x.strip()) for x in csv_prices.split(',') if x.strip()]
        if not prices:
            print("Error: No valid prices found.")
            return 0.0
        avg = sum(prices) / len(prices)
        print(f"Average Shot Price: $ {avg}")
        return avg
    except (ValueError, TypeError):
        print("Error: Malformed price format.")
        return 0.0

def parse_order_modifiers(modifiers):
    if not isinstance(modifiers, str) or not modifiers.strip():
        print("Error: Invalid or empty modifiers provided.")
        return {}
    result = {}
    items = modifiers.split(';')
    for item in items:
        if ':' in item:
            parts = item.split(':', 1)
            if len(parts) == 2:
                k, v = parts[0].strip(), parts[1].strip()
                if k:
                    result[k] = v
    print(f"Parsed Modifiers: {result}")
    return result

if __name__ == "__main__":
    print("==== Running lookup_drink_code ====")
    code_input = input("Enter drink code prefix (e.g. LAT, CAP, ESP): ")
    lookup_drink_code(code_input)

    print("\n==== Running calculate_average_shot_cost ====")
    prices_input = input("Enter CSV of shot prices (e.g. 1.0, 1.5, 2.0): ")
    calculate_average_shot_cost(prices_input)

    print("\n==== Running parse_order_modifiers ====")
    mods_input = input("Enter modifiers (e.g. milk:oat;syrup:vanilla): ")
    parse_order_modifiers(mods_input)