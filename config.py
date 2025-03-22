import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')

    # MongoDB Atlas connection string
    MONGO_URI = os.environ.get(
        'MONGO_URI',
        'mongodb+srv://anhquanduong05:Database8080@cluster0.d982y.mongodb.net/divine?retryWrites=true&w=majority&appName=Cluster0'
    )

    # Get the base directory dynamically
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Dynamically set the upload folder path
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "images")

    # Ensure the upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

     # Flask-Mail configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'noreplydivinee@gmail.com')  # Replace with your Gmail
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'axqi urnx zlfx yijc')     # Replace with your app password
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreplydivinee@gmail.com')
