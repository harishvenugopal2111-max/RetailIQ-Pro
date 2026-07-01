import streamlit as st
import sqlite3
import bcrypt

st.set_page_config(
    page_title="RetailIQ Pro",
    page_icon="🔐",
    layout="centered"
)

# ---------- DATABASE ----------
conn = sqlite3.connect("database/users.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT
)
""")
conn.commit()

# ---------- FUNCTIONS ----------
def register(username, password):

    if username == "" or password == "":
        return False, "Enter Username & Password"

    cur.execute("SELECT * FROM users WHERE username=?",(username,))
    if cur.fetchone():
        return False,"Username already exists"

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    cur.execute(
        "INSERT INTO users(username,password) VALUES(?,?)",
        (username,hashed)
    )

    conn.commit()

    return True,"Registration Successful"

def login(username,password):

    cur.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    row = cur.fetchone()

    if row:

        if bcrypt.checkpw(
            password.encode(),
            row[0]
        ):
            return True

    return False

# ---------- SESSION ----------
if "login" not in st.session_state:
    st.session_state.login=False

# ---------- UI ----------
st.markdown(
"""
<h1 style='text-align:center'>
RetailIQ Pro
</h1>
""",
unsafe_allow_html=True
)

tab1,tab2 = st.tabs(["🔐 Login","📝 Register"])

# ---------- LOGIN ----------
with tab1:

    st.subheader("Welcome Back")

    u = st.text_input("Username",key="l1")
    p = st.text_input("Password",type="password",key="l2")

    if st.button("Login",use_container_width=True):

        if login(u,p):

            st.session_state.login=True

            st.success("Login Successful")

            st.balloons()

        else:

            st.error("Invalid Username or Password")

# ---------- REGISTER ----------
with tab2:

    st.subheader("Create Account")

    ru = st.text_input("New Username")

    rp = st.text_input(
        "New Password",
        type="password"
    )

    cp = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button(
        "Register",
        use_container_width=True
    ):

        if rp!=cp:

            st.error("Passwords do not match")

        else:

            ok,msg = register(ru,rp)

            if ok:

                st.success(msg)

            else:

                st.error(msg)

# ---------- HOME ----------
if st.session_state.login:

    st.success("Welcome to RetailIQ Pro")

    st.write("Dashboard Ready 🚀")