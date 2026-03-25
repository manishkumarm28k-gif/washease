from app import create_app, db
from app.models import Order
import json
import traceback
from app.utils.pdf_generator import generate_invoice_pdf

app = create_app()
with app.app_context():
    orders = Order.query.all()
    print(f"Testing {len(orders)} orders...")
    success_count = 0
    for order in orders:
        if not order.items_json:
            continue
        items = json.loads(order.items_json)
        try:
            pdf_buffer = generate_invoice_pdf(order, items)
            success_count += 1
        except Exception as e:
            print(f"Error generating invoice for Order {order.id}:")
            traceback.print_exc()
    
    print(f"Successfully generated {success_count} invoices out of {len(orders)} total orders.")
