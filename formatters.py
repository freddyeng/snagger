from flask import Markup

def format_items_tables(df, table_classes="dataframe"):
    html = df.to_html(index=False, classes=f"{table_classes} table-json")

    combined_html = f"""
    <div class="table-wrapper">
        {html}
    </div>
    """
    return Markup(combined_html)  # ensures Jinja renders HTML, not raw text
