from app import create_app
from flask import send_file
import io

app = create_app()

with app.app_context():
    with app.test_request_context():
        try:
            buffer = io.BytesIO(b"dummy pdf content")
            response = send_file(
                buffer,
                as_attachment=True,
                download_name="WashEase_Invoice_INV-1.pdf",
                mimetype="application/pdf"
            )
            print("send_file success:", response)
        except Exception as e:
            import traceback
            traceback.print_exc()
