import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')

    # MongoDB Atlas connection string (Replace <your_password> with actual password)
    MONGO_URI = os.environ.get(
        'MONGO_URI',
        'mongodb+srv://anhquanduong05:Database8080@cluster0.d982y.mongodb.net/divine?retryWrites=true&w=majority&appName=Cluster0'
    )