import plotly.graph_objects as go
import plotly.io as pio
import re

def clean_price(price_str):
    """Clean price string by removing commas and non-numeric characters."""
    cleaned_price = re.sub(r"[^\d.]", "", price_str)  # Remove everything except numbers and decimal
    return float(cleaned_price) if cleaned_price else 0  # Convert to float

def generate_bar_chart(products):
    # Extract product names and cleaned prices
    product_names = [product["product_name"] for product in products]
    product_prices = [clean_price(product["price"]) for product in products]

    # Create bar chart
    fig = go.Figure(data=[go.Bar(x=product_names, y=product_prices, marker_color=['#4e79a7', '#f28e2b'])])
    
    # Update layout
    fig.update_layout(title="Price Comparison",
                      xaxis_title="Products",
                      yaxis_title="Price (₹)",
                      template="plotly_white")

    # Save chart as HTML
    pio.write_html(fig, "static/barchart.html")

# Test with dummy data
if __name__ == "__main__":
    sample_data = [
        {"product_name": "Product A", "price": "32,990."},
        {"product_name": "Product B", "price": "25,500"}
    ]
    generate_bar_chart(sample_data)
