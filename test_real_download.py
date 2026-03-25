from app import create_app, db
from app.models import Order, User

app = create_app()

with app.app_context():
    order = Order.query.first()
    user = User.query.get(order.user_id)
    print("Testing for User:", user.email, "Order:", order.id)

# Perform request using test client
client = app.test_client()
print("Logging in...")
resp = client.post('/login', data={'email': user.email, 'password': 'password'}, follow_redirects=True)
if b'Dashboard' not in resp.data and b'Logout' not in resp.data:
    print("Login failed! Response length:", len(resp.data))
    # In case password wasn't 'password', we just bypass it by setting a forced session
else:
    print("Login succeeded!")

print(f"Requesting /order/{order.id}/invoice...")
resp = client.get(f'/user/order/{order.id}/invoice')

print("Status:", resp.status_code)
print("Headers:", resp.headers)
if resp.status_code == 302:
    print("Redirect Location:", resp.headers.get('Location'))
    
# check if it actually yielded a file
if resp.status_code == 200 and resp.headers.get('Content-Type') == 'application/pdf':
    print("PDF SUCCESSFULLY DOWNLOADED VIA HTTP!")
else:
    print("Failed to download PDF over HTTP.")
