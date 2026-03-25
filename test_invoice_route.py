from app import create_app
from app.models import User, Order

app = create_app()
with app.app_context():
    users = User.query.filter(User.orders.any()).all()
    for user in users:
        with app.test_client() as client:
            client.post('/login', data={'email': user.email, 'password': 'password'}, follow_redirects=True)
            for order in user.orders:
                print(f"Testing order {order.id} for user {user.email}")
                resp = client.get(f'/user/order/{order.id}/invoice', follow_redirects=True)
                if b'Failed to generate invoice' in resp.data:
                    print(f"FAILED for order {order.id}")
                else:
                    if resp.status_code != 200:
                        print(f"Status {resp.status_code} for order {order.id}")
                    else:
                        print(f"Success for order {order.id}")
