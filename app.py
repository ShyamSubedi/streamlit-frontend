import streamlit as st
import requests
import pandas as pd
from supabase import create_client

# Supabase setup
SUPABASE_URL = "https://oehpyaughmlhynmuhzrk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9laHB5YXVnaG1saHlubXVoenJrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMwMTYxOTUsImV4cCI6MjA1ODU5MjE5NX0.CPMU5-sEy2krskO27pwXB_85XaX6vtC75WxjKhGr3gk"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# API endpoint (your deployed Render API)
API_URL = "https://mlops-roadmape.onrender.com/predict/"

# Streamlit UI setup
st.set_page_config(page_title="Fraud Detection", layout="centered")
st.title("🛡️ Fraud Detection App")
st.write("Enter a transaction amount to check if it's fraudulent.")

# Input as free text and validate
amount_input = st.text_input("💰 Enter Transaction Amount")
valid = False

try:
    amount = float(amount_input)
    valid = True
except ValueError:
    if amount_input != "":
        st.warning("⚠️ Please enter a valid numeric amount (e.g. 1000.50)")

# Predict button
if st.button("🔍 Predict") and valid:
    with st.spinner("Sending to API..."):
        try:
            response = requests.post(API_URL, json={"amount": amount})
            st.text(f"🔁 Status code: {response.status_code}")
            st.text(f"📦 Raw response: {response.text}")
            result = response.json()
            st.success("✅ Prediction received!")
            st.metric("Fraud Prediction", result["fraud_prediction"])
            st.metric("Fraud Probability", round(result["fraud_probability"], 6))
        except Exception as e:
            st.error(f"❌ Error: {e}")

# Logs section from Supabase
st.divider()
st.subheader("📊 Recent Predictions (from Supabase Logs)")

try:
    data = supabase.table("new_logs").select("*").order("timestamp", desc=True).limit(10).execute()
    df = pd.DataFrame(data.data)
    st.dataframe(df)
except Exception as e:
    st.warning(f"⚠️ Could not fetch logs: {e}")
