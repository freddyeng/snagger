from flask import Markup

def format_largest_grand_total(gt_result):
    if not gt_result:
        return None
    return f'{gt_result["keys_match"]}, {gt_result["json1_key"]}:{gt_result["json1_value"]}, {gt_result["json2_key"]}:{gt_result["json2_value"]}'

def format_items_tables(df1, df2, table_classes="dataframe"):
    """Return two DataFrames as side-by-side HTML tables."""
    html1 = df1.to_html(index=False, classes=f"{table_classes} table-json1")
    html2 = df2.to_html(index=False, classes=f"{table_classes} table-json2")

    combined_html = f"""
    <div class="items-comparison-side-by-side">
        <div class="table-wrapper">
            <h4>File A Items</h4>
            {html1}
        </div>
        <div class="table-wrapper">
            <h4>File B Items</h4>
            {html2}
        </div>
    </div>
    """
    return Markup(combined_html)  # ensures Jinja renders HTML, not raw text
