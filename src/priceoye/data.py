# src/priceoye/data.py

# Dummy Data for PriceOye
faq_db = {
    "What is the warranty period?": "All mobiles come with a 1-year brand warranty.",
    "How do I track my order?": "Check your order status in your account or use the tracking ID sent via SMS.",
    "Do you offer open box deliveries?": "Open-box delivery is available in Islamabad, Lahore, and Karachi for PKR 300.",
    "What are the charges for home delivery?": "Standard home delivery is PKR 200. Free delivery on orders above PKR 20,000.",
    "What is the process for installment?": "Installments are available via partnered banks. Log into your account, select installment at checkout, and follow the bank’s approval process."
}
order_db = {
    "order1001": {"status": "shipped", "tracking": "PK123456789", "delivery_date": "2025-05-01"},
    "order1002": {"status": "processing", "tracking": None}
}
product_db = {
    "Samsung Galaxy A54": {"price": 79999, "ram": "8GB", "storage": "128GB", "camera": "50MP"},
    "Infinix Note 30": {"price": 49999, "ram": "6GB", "storage": "64GB", "camera": "48MP"}
}
cart_status = {
    "cart001": "abandoned",
    "cart002": "active"
}