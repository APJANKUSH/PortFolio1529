import streamlit as st
import sqlite3

# Function to get user details
def get_user_details(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, email FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please log in first!")
    st.switch_page("login.py")  # Redirect to Login Page

# Home Page Content
st.sidebar.success("✅ Logged in as " + st.session_state.current_user)

tab1, tab2 = st.tabs(["🏠 Dashboard", "👤 Profile"])

# Dashboard Tab
with tab1:
    st.title("🏠 Welcome to Your Dashboard!")
    st.write("You have successfully logged in.")

# Profile Tab
with tab2:
    st.title("👤 Your Profile")
    user_details = get_user_details(st.session_state.current_user)
    if user_details:
        st.write(f"**Username:** {user_details[0]}")
        st.write(f"**Email:** {user_details[1]}")
    else:
        st.error("Error fetching profile details.")

# Logout Button
if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.success("🔒 Logged out successfully!")
    st.switch_page("login.py")  # Redirect to Login Page
