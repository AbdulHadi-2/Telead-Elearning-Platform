import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate('path/to/your/firebase-key.json')  # Replace with your Firebase key
firebase_admin.initialize_app(cred)