from app import create_app, db, bcrypt
from app.models import User, Order

app = create_app()
with app.app_context():
    order = Order.query.first()
    user = User.query.get(order.user_id)
    # temporarily force password
    user.password = bcrypt.generate_password_hash('password').decode('utf-8')
    db.session.commit()
    print("Testing for User:", user.email, "Order:", order.id)

client = app.test_client()
client.post('/login', data={'email': user.email, 'password': 'password'}, follow_redirects=True)

resp = client.get(f'/user/order/{order.id}/invoice', follow_redirects=True)
import re
m = re.search(r'Failed to generate invoice:[^<]*', resp.data.decode('utf-8'))
if m:
    print("FLASH ERROR FOUND:", m.group(0))
else:
    print("No flash error found. Status:", resp.status_code)
    if resp.headers.get('Content-Type') == 'application/pdf':
        print("Wait, it succeeded???")
