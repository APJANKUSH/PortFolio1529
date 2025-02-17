import streamlit as st
# import pandas as pd
# import numpy as np
import hashlib
import sqlite3

from streamlit_option_menu import option_menu

selected2 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
selected2


if selected2 == "Home":
    with st.form("My Form"):
        name = st.text_input("Enter Your Name :")
        email = st.text_input("Enter Your Email")
        submit= st.form_submit_button("Submit")
    if submit:
        st.write(f"Your Name is {name} & Email is {email}")

elif selected2 == "Upload":
    st.title("Upload Page")
    st.write("Upload your files here.")
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "csv", "png", "jpg", "pdf"])


    if uploaded_file is not None:
        st.write("### File Details:")
        st.write(f"📂 **Filename:** {uploaded_file.name}")
        st.write(f"📏 **File Size:** {uploaded_file.size / 1024:.2f} KB")
        file_type = uploaded_file.type
        if file_type == "text/plain":
            # Read and display text files
            file_contents = uploaded_file.read().decode("utf-8")
            st.text_area("📜 File Content:", file_contents, height=200)

        elif file_type in ["image/png", "image/jpeg"]:
            # Display image files
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        elif file_type == "application/pdf":
            st.write("📄 PDF Uploaded. Preview not supported.")

        else:
            st.write("✅ File uploaded successfully!")

    else:
        st.warning("⚠️ Please upload a file to proceed.")
    
elif selected2 == "Tasks":
    st.title("Tasks Page")
    st.write("View your tasks here.")
    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    with st.form("new_task_form"):
        new_task = st.text_input("📝 Enter a new task:")
        submitted = st.form_submit_button("Add Task")
    
    if submitted and new_task:
        st.session_state.tasks.append({"task": new_task, "completed": False})
        st.success("✅ Task Added!")

# Display Tasks
    st.subheader("📌 Your Tasks")

    if st.session_state.tasks:
        for i, task in enumerate(st.session_state.tasks):
            col1, col2 = st.columns([0.8, 0.2])
            
            # Display task with checkbox
            checked = col1.checkbox(task["task"], value=task["completed"], key=i)
            
            # Update task status
            st.session_state.tasks[i]["completed"] = checked
            
            # Delete button
            if col2.button("❌", key=f"del_{i}"):
                st.session_state.tasks.pop(i)
                st.experimental_rerun()

    else:
        st.info("No tasks added yet. Add a new task above! 🚀")

elif selected2 == "Settings":
    st.title("Settings Page")
    st.write("Change your settings here.")
    theme = st.selectbox("🎨 Select Theme:", ["Light", "Dark", "Blue", "Green"])
    st.write(f"🖌 Selected Theme: **{theme}**")

    # Notification toggle
    notifications = st.checkbox("🔔 Enable Notifications")
    if notifications:
        st.success("✅ Notifications Enabled!")
    else:
        st.warning("❌ Notifications Disabled!")

    # Account settings
    st.subheader("👤 Account Settings")
    username = st.text_input("Change Username", placeholder="Enter new username")
    password = st.text_input("Change Password", type="password", placeholder="Enter new password")

    if st.button("Save Changes"):
        st.success("✅ Settings Updated Successfully!")

