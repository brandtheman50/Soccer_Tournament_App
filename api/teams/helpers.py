# utils/qr.py
from io import BytesIO
from qrcode.constants import ERROR_CORRECT_M
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import qrcode
import uuid

def make_qr_png_bytes(data: str) -> bytes:
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=8, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()

def send_qr_email(to_email: str, payload: str):
    """
    payload: the content your QR should encode
            (e.g., a URL, token, or short code)
    """
    # 1) Generate QR image bytes
    qr_png = make_qr_png_bytes(payload)

    # 2) Generate a unique CID (no angle brackets here)
    qr_cid = uuid.uuid4().hex

    # 3) Render your HTML with the CID
    #    Your template file should be at: templates/emails/qr_email.html
    html = render_to_string("emails/qr_code_email.html", {"qr_cid": qr_cid})
    text = strip_tags(html)

    # 4) Build the email
    msg = EmailMultiAlternatives(
        subject="Your QR Code",
        body=text,
        from_email="no-reply@example.test",
        to=[to_email],
    )
    msg.attach_alternative(html, "text/html")

    # 5) Attach the image inline; header **must** wrap CID in <>
    img = MIMEImage(qr_png, _subtype="png")
    img.add_header("Content-ID", f"<{qr_cid}>")
    img.add_header("Content-Disposition", "inline", filename="qr.png")
    msg.attach(img)

    # 6) Send
    msg.send()

def process_and_store(photo_data):
    return
