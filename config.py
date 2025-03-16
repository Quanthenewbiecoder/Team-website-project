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
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "images")

    # Ensure the upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
