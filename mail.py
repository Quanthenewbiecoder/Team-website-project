from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='noreplydivinee@gmail.com',
    MAIL_PASSWORD='axqi urnx zlfx yijc',
    MAIL_DEFAULT_SENDER='noreplydivinee@gmail.com',
)

mail = Mail(app)

with app.app_context():
    msg = Message("Test Email",
                  recipients=["noreplydivinee@gmail.com"],
                  body="This is a test")
    try:
        mail.send(msg)
        print("✅ Email sent successfully")
    except Exception as e:
        import traceback
        traceback.print_exc()
