import pandas as pd

def largest_grand_total_key(json):
    """Return the key and value of the largest entry in grand_totals."""
    gt = json.get("grand_totals", {})
    if not gt:
        return {"json_key": None, "json_value": None}

    key, value = max(gt.items(), key=lambda kv: kv[1])
    return {"json_key": key, "json_value": value}

def items_comparison(json):
    """ Match line items and compare quantities, unit cost and total cost. """

    df = pd.DataFrame(json["items"])

    selected_columns = ["item_code", "quantity", "unit_price", "total_price"]

    df_key_cols = df[selected_columns]
    df_sorted = df_key_cols.sort_values(by=["unit_price", "quantity"], ascending=[False, False])

    return df_sorted