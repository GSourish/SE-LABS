from hypothesis import given, strategies as st
from processor import lookup_drink_code, calculate_average_shot_cost, parse_order_modifiers

@given(st.text() | st.none())
def test_lookup_drink_code(code):
    lookup_drink_code(code)

@given(st.text() | st.none())
def test_calculate_average_shot_cost(csv_prices):
    calculate_average_shot_cost(csv_prices)

@given(st.text() | st.none())
def test_parse_order_modifiers(modifiers):
    parse_order_modifiers(modifiers)