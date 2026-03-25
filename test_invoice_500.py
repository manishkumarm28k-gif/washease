from app import create_app
from app.models import Order
app = create_app()
app.config['LOGIN_DISABLED'] = True
app.config['TESTING'] = True  # This ensures exceptions bubble up!

with app.app_context():
    order = Order.query.first()
    client = app.test_client()
    try:
        resp = client.get(f'/user/order/{order.id}/invoice')
        print(resp.status_code)
    except Exception as e:
        import traceback
        traceback.print_exc()
