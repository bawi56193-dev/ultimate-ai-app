import streamlit as st
import google.generativeai as genai
from supabase import create_client

# 1. Database & AI Setup
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except Exception as e:
    st.error("System configuration missing. Please check Streamlit Secrets.")

st.set_page_config(page_title="Ultimate AI Agent", layout="centered")

# App Header
st.markdown("<h1 style='text-align: center;'>🚀 Ultimate Business & TikTok AI</h1>", unsafe_allow_html=True)
st.write("---")

# 2. Tracking User (Mockup ID for testing)
user_ip = "guest_user_1" 

# 3. Check Database for usage count
try:
    res = supabase.table("user_usage").select("*").eq("user_ip", user_ip).execute()
    count = res.data[0]['usage_count'] if res.data else 0
except:
    count = 0

st.info(f"📊 You have {5 - count} free credits remaining.")

# 4. Main App Logic
if count < 5:
    user_query = st.text_area("Describe your problem (TikTok views, Business Strategy, etc.)", height=150)
    
    if st.button("Generate 100% Perfect Plan"):
        if user_query:
            with st.spinner('AI Expert is thinking...'):
                model = genai.GenerativeModel('gemini-pro')
                
                master_prompt = f"""
                You are an elite Business and Social Media growth expert. 
                User's Problem: {user_query}
                Provide:
                1. Root Cause Analysis
                2. 30-Day Step-by-Step Strategy
                3. Content/Marketing Secrets
                4. Final bold command to reach success.
                """
                
                response = model.generate_content(master_prompt)
                st.markdown("### 🏆 AI Expert Recommendation")
                st.write(response.text)
                
                # Update Database Count
                if not res.data:
                    supabase.table("user_usage").insert({"user_ip": user_ip, "usage_count": 1}).execute()
                else:
                    supabase.table("user_usage").update({"usage_count": count + 1}).eq("user_ip", user_ip).execute()
        else:
            st.warning("Please enter a question first.")
else:
    st.error("⚠️ Free limit reached!")
    st.markdown("### Upgrade to Pro to continue")
    st.link_button("Unlock Everything ($)", st.secrets.get("LEMON_SQUEEZY_LINK", "https://your-lemonsqueezy-link.com"))

st.write("---")
st.caption("Empowering your growth with AI.")
