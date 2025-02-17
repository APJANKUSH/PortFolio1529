import streamlit as st
import hashlib
import sqlite3
import re  # For email validation

# 🔒 Function to hash passwords securely
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 🗄️ Initialize SQLite database
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()

# 🔑 Function to add a new user
def add_user(username, password, email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "invalid_email"  # Email validation
    if len(password) < 6:
        return "weak_password"  # Simple password strength check
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    hashed_pass = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                       (username, hashed_pass, email))
        conn.commit()
        return "success"
    except sqlite3.IntegrityError:
        return "user_exists"  # Username or email already exists
    finally:
        conn.close()

# ✅ Function to verify user login
def verify_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    hashed_pass = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_pass))
    user = cursor.fetchone()
    conn.close()
    return user

# 📌 Function to get user details
def get_user_details(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, email FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# 🏁 Initialize database
init_db()

# 🔄 Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# 📌 Sidebar Navigation
menu = st.sidebar.selectbox(
    "Navigation", 
    ["Home", "Profile", "Logout"] if st.session_state.logged_in else ["Login", "Signup"]
)

# 🏠 HOME PAGE (Only visible after login)
if menu == "Home":
    if not st.session_state.logged_in:
        st.warning("⚠️ You are not logged in. Redirecting to login page...")
        st.experimental_rerun()
    
    st.sidebar.success(f"✅ Logged in as: {st.session_state.current_user}")
    st.title("🏠 Welcome to Your Dashboard!")
    st.write("You have successfully logged in.")

# 👤 PROFILE PAGE
elif menu == "Profile":
    if not st.session_state.logged_in:
        st.warning("⚠️ You need to log in first.")
        st.experimental_rerun()
    
    st.title("👤 Your Profile")
    user_details = get_user_details(st.session_state.current_user)
    if user_details:
        st.write(f"**Username:** {user_details[0]}")
        st.write(f"**Email:** {user_details[1]}")
    else:
        st.error("⚠️ Unable to fetch profile details.")

# 🔑 LOGIN PAGE
elif menu == "Login":
    st.title("🔑 Login Page")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        user = verify_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success(f"✅ Welcome, {username}!")
            st.experimental_rerun()
        else:
            st.error("❌ Incorrect username or password.")

# 📝 SIGNUP PAGE
elif menu == "Signup":
    st.title("📝 Signup Page")

    new_username = st.text_input("Create Username")
    new_email = st.text_input("Enter Email")
    new_password = st.text_input("Create Password", type="password")
    signup_button = st.button("Signup")

    if signup_button:
        status = add_user(new_username, new_password, new_email)
        if status == "success":
            st.success("✅ Signup successful! You can now log in.")
        elif status == "user_exists":
            st.warning("⚠️ Username or email already exists. Try another!")
        elif status == "invalid_email":
            st.warning("⚠️ Please enter a valid email address!")
        elif status == "weak_password":
            st.warning("⚠️ Password must be at least 6 characters long.")

# 🔒 LOGOUT PAGE
elif menu == "Logout":
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.success("🔒 Logged out successfully! Redirecting to login page...")
    st.experimental_rerun()
