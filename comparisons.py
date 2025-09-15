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
