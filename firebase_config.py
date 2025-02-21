# # firebase_config.py
# import streamlit as st
# import firebase_admin
# from firebase_admin import credentials, storage
# import os

# def initialize_firebase():
#     if not firebase_admin._apps:
#         try:
#             cred = credentials.Certificate("/Users/loukyaharisha/Desktop/capstone/visionml-flask-firebase-adminsdk-njze6-bb711339e4.json")
#             firebase_admin.initialize_app(cred, {
#                 "storageBucket": "visionml-flask.appspot.com"
#             })
#             return True
#         except Exception as e:
#             st.error(f"Firebase initialization error: {e}")
#             return False
#     return True

# def test_firebase_connection():
#     try:
#         bucket = storage.bucket()
#         # Try to list blobs to verify access
#         blobs = list(bucket.list_blobs(max_results=1))
#         st.success("✅ Successfully connected to Firebase Storage!")
#         return True
#     except Exception as e:
#         st.error(f"Firebase access error: {e}")
#         return False

# def upload_to_firebase(file_path, destination_blob_name):
#     try:
#         bucket = storage.bucket()
#         blob = bucket.blob(destination_blob_name)
#         blob.upload_from_filename(file_path)
#         blob.make_public()
#         return blob.public_url
#     except Exception as e:
#         st.error(f"Failed to upload to Firebase: {e}")
#         return None