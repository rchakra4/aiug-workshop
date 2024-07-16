
import hmac
import streamlit as st

st.set_page_config(layout="wide")

def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    return False


# Header
title = "myfitnessagent"
logo_path = "../../../logo.png"

col1_header, col2_header = st.columns([1, 10])

with col1_header:
    st.image(logo_path, width=100)

# Display the title in the second column
with col2_header:
    st.title(title)

st.write("")

# Set up the main app page
st.subheader("Welcome to myfitnessagent")

col1_auth, col2_auth = st.columns([1, 2])

with col1_auth:
    if not check_password():
        st.stop()

# Display the title in the second column
with col2_auth:
    st.write("")


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# User is already logged in, show the authenticated message
st.write(f"You have been authenticated.")
st.write("Select your agent from the sidebar to begin.")

st.subheader("Agents available:")
st.write("1. Onboarding Agent [ReAct]")
st.write("2. Training Agent [CoT FSP]")
st.write("3. Nutrition Agent [RAG]")

# Add a logout button
if st.button('Logout'):
    st.session_state["password_correct"] = False
    st.rerun()