import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate(r"C:\\Users\\joshi\\OneDrive\Desktop\\GDG SOLN\\info.json")  
firebase_admin.initialize_app(cred)

# Firestore Database Connection
db = firestore.client()

# Function to get Firestore instance (dependency for routes)
def get_db():
    return db
