# src/priceoye/__init__.py

from flask import Flask
from priceoye.config import llm
from priceoye.agents_ import (
    orchestrator_agent,
    order_agent,
    return_agent,
    product_agent,
    warranty_agent,
    proactive_agent
)
from priceoye.tools import (
    get_faq_answer,
    get_order_status,
    process_return,
    get_product_info,
    compare_products,
    check_warranty,
    check_cart_status,
    send_proactive_message,
    get_customer_sentiment
)
from priceoye.data import (
    faq_db,
    order_db,
    product_db,
    cart_status
)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'priceoye-secret-key'  # For session management
    from priceoye.routes import bp
    app.register_blueprint(bp)
    return app