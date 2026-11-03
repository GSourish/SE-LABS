import pytest

from coffee_shop_order import (
    process_order_batch,
    check_espresso_machine
)


# Helper function to create orders
def make_order(
    paid=True,
    size="medium",
    strict_allergy=False,
    is_member=False,
    customizations=None
):
    return {
        "paid": paid,
        "size": size,
        "strict_allergy": strict_allergy,
        "is_member": is_member,
        "customizations": customizations or []
    }


# 1. Basic coffee orders
def test_single_medium_coffee():
    orders = [
        make_order(
            customizations=[{"type": "standard", "cost": 0.5}]
        )
    ]

    result = process_order_batch(orders, 0.1)

    assert result["total"] == 5.5
    assert result["status"] == "COMPLETED"


def test_small_coffee():
    result = process_order_batch(
        [make_order(size="small")], 0
    )

    assert result["total"] == 3.0


def test_large_coffee():
    result = process_order_batch(
        [make_order(size="large")], 0
    )

    assert result["total"] == 6.0


def test_invalid_coffee_size():
    result = process_order_batch(
        [make_order(size="extra_large")], 0
    )

    assert result["status"] == "NO_SALE"


# 2. Payment conditions
def test_unpaid_order():
    result = process_order_batch(
        [make_order(paid=False)], 0
    )

    assert result["status"] == "NO_SALE"


# 3. Customizations
def test_syrup_within_price_limit():
    result = process_order_batch(
        [make_order(customizations=[
            {"type": "syrup", "cost": 1.0}
        ])], 0
    )

    assert result["total"] == 5.5


def test_syrup_above_price_limit():
    result = process_order_batch(
        [make_order(customizations=[
            {"type": "syrup", "cost": 2.5}
        ])], 0
    )

    assert result["total"] == 6.0


def test_standard_customization():
    result = process_order_batch(
        [make_order(customizations=[
            {"type": "standard", "cost": 0.5}
        ])], 0
    )

    assert result["total"] == 5.0


def test_negative_customization_cost():
    result = process_order_batch(
        [make_order(customizations=[
            {"type": "standard", "cost": -1}
        ])], 0
    )

    assert result["total"] == 4.5


# 4. Allergy conditions
def test_strict_allergy():
    result = process_order_batch(
        [make_order(
            strict_allergy=True,
            customizations=[
                {"type": "allergen_alert", "cost": 0}
            ]
        )], 0
    )

    assert result["status"] == "NO_SALE"


def test_non_strict_allergy():
    result = process_order_batch(
        [make_order(
            strict_allergy=False,
            customizations=[
                {"type": "allergen_alert", "cost": 0}
            ]
        )], 0
    )

    assert result["total"] == 4.5
    assert result["status"] == "COMPLETED"


# 5. Membership discount
def test_member_discount():
    result = process_order_batch(
        [make_order(is_member=True)], 0
    )

    assert result["total"] == 4.05


# 6. Invalid input and tax
def test_invalid_orders_input():
    with pytest.raises(ValueError):
        process_order_batch("invalid", 0.1)


def test_negative_tax_rate():
    with pytest.raises(ValueError):
        process_order_batch([], -0.1)


# 7. Rejection threshold
def test_audit_rejected():
    orders = [
        make_order(customizations=[
            {"type": "allergen_alert", "cost": 0}
        ])
        for _ in range(5)
    ]

    result = process_order_batch(orders, 0)

    assert result["status"] == "AUDIT_REJECTED"


# 8. Espresso machine tests
def test_no_temperature_data():
    assert check_espresso_machine([]) == "NO_DATA"


def test_normal_temperature():
    assert check_espresso_machine([
        [90, 92, 94, 95]
    ]) == "OPTIMAL"


def test_single_overheating_temperature():
    assert check_espresso_machine([
        [97, 95, 94]
    ]) == "OPTIMAL"


def test_consecutive_overheating():
    assert check_espresso_machine([
        [97, 98]
    ]) == "SHUTDOWN"


def test_overheating_streak_resets():
    assert check_espresso_machine([
        [97, 95, 97, 98]
    ]) == "SHUTDOWN"