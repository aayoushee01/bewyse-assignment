import firebase_admin
from firebase_admin import credentials

# Path to your Firebase service account key JSON file
FIREBASE_SERVICE_ACCOUNT_KEY = 'myapp/bewyseass-firebase-adminsdk-rzqw8-4453e24912.json'

# Initialize Firebase Admin SDK
cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_KEY)
firebase_admin.initialize_app(cred)