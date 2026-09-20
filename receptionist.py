import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(page_title="24/7 AI Receptionist", layout="centered")

st.title("🤖 24/7 AI Receptionist")
st.write("Lightning-fast Groq AI customer support bot built for foreign business clients.")

# --- SIDEBAR: API Key & Business Settings ---
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Groq API Key", type="password")

st.sidebar.header("Business Settings")
biz_type = st.sidebar.selectbox("Business Type", ["Gym & Fitness", "Dental Clinic", "Spa & Wellness", "Real Estate"])
biz_name = st.sidebar.text_input("Business Name", "FitZone Gym")
biz_services = st.sidebar.text_area("Services & Pricing", "1. Monthly Gym Membership: $50\n2. Personal Training: $150/month\n3. Day Pass: $10")

# System Prompt in Professional English
system_prompt = f"""
You are an expert, polite, and persuasive virtual receptionist for a {biz_type} named '{biz_name}'.
Your main goals are:
1. Answer customer inquiries professionally using these details: {biz_services}.
2. Always reply in clear, natural, and fluent English.
3. Clear any doubts they have about joining, pricing, or booking.
4. Collect their Full Name and Phone Number to confirm an appointment or free trial booking.
Once you get their details, confirm the booking enthusiastically. Keep your answers concise, helpful, and conversational.
"""

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- QUICK ACTION BUTTONS (In English) ---
st.markdown("---")
st.write("⚡ **Quick Inquiries:** Click any option below to test instantly:")
q_col1, q_col2, q_col3 = st.columns(3)

quick_prompt = None
with q_col1:
    if st.button("💰 View Pricing"):
        quick_prompt = "What are the monthly membership and day pass prices?"
with q_col2:
    if st.button("🏋️‍♂️ Personal Training"):
        quick_prompt = "Can you tell me the personal training details and rates?"
with q_col3:
    if st.button("📅 Book Free Trial"):
        quick_prompt = "I would like to book a free trial session please."

# User Input (Chat box or Quick button)
chat_input = st.chat_input(f"Ask something about {biz_name}...")
user_input = quick_prompt if quick_prompt else chat_input

if user_input:
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar first!")
    else:
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        try:
            # Initialize Groq Client
            client = Groq(api_key=api_key)
            
            # Format messages payload for Groq API
            messages_payload = [{"role": "system", "content": system_prompt}]
            for m in st.session_state.messages:
                messages_payload.append({"role": m["role"], "content": m["content"]})

            # Call Groq Model (Using openai/gpt-oss-120b model)
            completion = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages_payload,
                temperature=0.7
            )
            
            ai_response = completion.choices[0].message.content

            # Append assistant response
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            with st.chat_message("assistant"):
                st.markdown(ai_response)

            # Check if booking was confirmed to trigger simulated manager notification
            if any(keyword in ai_response.lower() for keyword in ["booked", "secures", "confirmed", "noted your details", "lock in"]):
                st.success("📨 [System Notification]: Booking details & lead successfully sent to Gym Manager's WhatsApp & Email!")

        except Exception as e:
            st.error(f"An error occurred: {e}")