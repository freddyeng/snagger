import pandas as pd

def items_count_equal(json1, json2):
    """Check if 'items' arrays are the same length."""
    return len(json1.get("items", [])) == len(json2.get("items", []))


def items_count_difference(json1, json2):
    """Return the difference in 'items' array lengths."""
    return len(json1.get("items", [])) - len(json2.get("items", []))


def total_price_difference(json1, json2):
    """Return the numeric difference between total_price fields."""
    return json1.get("total_price", 0) - json2.get("total_price", 0)

def largest_grand_total_key(json1, json2):
    """
    Compare the keys of the largest value in grand_totals for each JSON.
    Returns a dict with keys and whether they match.
    """
    def max_key(grand_totals):
        if not grand_totals:
            return None, None
        # find key with max value
        key, value = max(grand_totals.items(), key=lambda kv: kv[1])
        return key, value

    gt1 = json1.get("grand_totals", {})
    gt2 = json2.get("grand_totals", {})

    key1, value1 = max_key(gt1)
    key2, value2 = max_key(gt2)

    return {
        "json1_key": key1,
        "json1_value": value1,
        "json2_key": key2,
        "json2_value": value2,
        "keys_match": value1 == value2
    }

def items_comparison(json1, json2):
    """ Match line items and compare quantities, unit cost and total cost. """

    df1 = pd.DataFrame(json1["items"])
    df2 = pd.DataFrame(json2["items"])

    selected_columns = ["item_code", "quantity", "unit_price", "total_price"]

    df1_key_cols = df1[selected_columns]
    df2_key_cols = df2[selected_columns]
    
    df1_sorted = df1_key_cols.sort_values(by=["unit_price", "quantity"], ascending=[False, False])
    df2_sorted = df2_key_cols.sort_values(by=["unit_price", "quantity"], ascending=[False, False])

    return {
        "json1_items": df1_sorted,
        "json2_items": df2_sorted,
    }