# src/priceoye/tools.py

from agents import function_tool
from priceoye.data import faq_db, order_db, product_db, cart_status

@function_tool
def get_faq_answer(question: str) -> str:
    """Fetch answer from FAQ database."""
    return faq_db.get(question, "Please contact support at 051-111-693-693.")

@function_tool
def get_order_status(order_id: str) -> str:
    """Fetch order status from the order database."""
    order = order_db.get(order_id)
    if order:
        status = order.get("status", "unknown")
        tracking = order.get("tracking", "N/A")
        delivery = order.get("delivery_date", "TBD")
        return f"Order {order_id} is {status}. Tracking: {tracking}. Expected delivery: {delivery}."
    return "Order not found."

@function_tool
def process_return(order_id: str) -> str:
    """Guide the customer through the return process."""
    return f"For order {order_id}, log into your account, file a complaint with unboxing and issue videos, and ship via Leopards Courier within 3 days."

@function_tool
def get_product_info(product_name: str) -> str:
    """Fetch product details from the product database."""
    product = product_db.get(product_name)
    if product:
        return f"{product_name}: Price PKR {product['price']}, RAM {product['ram']}, Storage {product['storage']}, Camera {product['camera']}."
    return "Product not found."

@function_tool
def compare_products(product1: str, product2: str) -> str:
    """Compare two products based on specs."""
    p1 = product_db.get(product1, {})
    p2 = product_db.get(product2, {})
    if p1 and p2:
        return f"Comparing {product1} (Price: PKR {p1['price']}, RAM: {p1['ram']}) vs {product2} (Price: PKR {p2['price']}, RAM: {p2['ram']})."
    return "One or both products not found."

@function_tool
def check_warranty(order_id: str) -> str:
    """Check warranty status for an order."""
    return f"Order {order_id} has a 1-year brand warranty. Visit an authorized service center for claims."

@function_tool
def check_cart_status(cart_id: str) -> str:
    """Check the status of the given cart ID."""
    status = cart_status.get(cart_id, "unknown")
    return f"Cart {cart_id} is {status}."

@function_tool
def send_proactive_message(customer_id: str, message: str) -> str:
    """Send a proactive message to the customer."""
    return f"Message sent to customer {customer_id}: {message}"

@function_tool
def get_customer_sentiment(customer_message: str) -> str:
    """Detect the sentiment of the customer's message."""
    positive_words = ["happy", "great", "satisfied"]
    negative_words = ["frustrated", "angry", "upset"]
    for word in customer_message.lower().split():
        if word in positive_words:
            return "positive"
        if word in negative_words:
            return "negative"
    return "neutral"