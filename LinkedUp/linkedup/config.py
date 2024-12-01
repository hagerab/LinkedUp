import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'linkedup2024')
    # Update DATABASE_URI to connect to MySQL instead of SQLite
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'mysql://root:Linkedup-012@127.0.0.1/linkedup_dp')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secretkey')
