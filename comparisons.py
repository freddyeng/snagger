def jsons_equal(json1, json2):
    """Check if the two JSONs are fully equal."""
    return json1 == json2


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

def format_largest_grand_total(gt_result):
    """
    Takes the dict from largest_grand_total_key and returns a single string:
    "<keys_match>, <json1_key>:<json1_value>, <json2_key>:<json2_value>"
    Returns None if input is None.
    """
    if not gt_result:
        return None
    return f'{gt_result["keys_match"]}, {gt_result["json1_key"]}:{gt_result["json1_value"]}, {gt_result["json2_key"]}:{gt_result["json2_value"]}'
