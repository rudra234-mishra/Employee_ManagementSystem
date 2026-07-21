import streamlit as st
import requests
import pandas as pd

BASE_URL = "https://employee-managementsystem-inxi.onrender.com"

st.set_page_config(
    page_title="Employee Management",
    page_icon="👨‍💼",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background: #000000;
    }

    section[data-testid="stSidebar"] {
        background: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: #f9fafb !important;
    }

    .main-title {
        color: #f9fafb;
        font-size: 2.1rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .sub-title {
        color: #9ca3af;
        font-size: 0.98rem;
        margin-bottom: 1.2rem;
    }

    .card {
        background: #0f172a;
        padding: 1.3rem;
        border-radius: 16px;
        border: 1px solid #1f2937;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35);
        margin-bottom: 1rem;
    }

    .stButton > button {
        background: #22c55e;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.55rem 1rem;
        font-weight: 600;
    }

    .stButton > button:hover {
        background: #16a34a;
    }

    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    div[data-baseweb="input"] input {
        color: white;
    }

    label, .stCaption, .stMarkdown {
        color: #f9fafb;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">👨‍💼 Employee Management System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Simple employee CRUD interface</div>', unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Menu",
    ["View Employees", "Fetch Employee", "Insert Employee", "Update Employee", "Delete Employee"]
)

def show_table(data):
    if isinstance(data, list):
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    elif isinstance(data, dict):
        st.dataframe(pd.DataFrame([data]), use_container_width=True, hide_index=True)
    else:
        st.write(data)

# ---------------- VIEW ---------------- #
if menu == "View Employees":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("View Employees")

    if st.button("Load Employees"):
        try:
            response = requests.get(f"{BASE_URL}/view", timeout=10)
            if response.status_code == 200:
                show_table(response.json())
            else:
                st.error(response.text)
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FETCH ---------------- #
elif menu == "Fetch Employee":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Fetch Employee")

    emp_id = st.number_input("Employee ID", min_value=1, step=1)

    if st.button("Fetch"):
        try:
            response = requests.get(f"{BASE_URL}/fetch/{int(emp_id)}", timeout=10)
            if response.status_code == 200:
                show_table(response.json())
            else:
                try:
                    st.error(response.json().get("detail", response.text))
                except Exception:
                    st.error(response.text)
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- INSERT ---------------- #
elif menu == "Insert Employee":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("➕ Insert New Employee")
    st.caption("Only Employee ID is required. Name, Age, Department, and Salary are optional.")

    with st.form("insert_form", clear_on_submit=True):
        st.markdown("### Employee Details")

        col1, col2 = st.columns(2)

        with col1:
            emp_id = st.number_input(
                "Employee ID *",
                min_value=1,
                step=1,
                help="Required field"
            )
            name = st.text_input(
                "Full Name",
                placeholder="Enter employee name",
                help="Optional"
            )
            dept = st.text_input(
                "Department",
                placeholder="Enter department",
                help="Optional"
            )

        with col2:
            age = st.text_input(
                "Age",
                placeholder="Optional",
                help="Optional"
            )
            salary = st.text_input(
                "Salary",
                placeholder="Optional",
                help="Optional"
            )
            st.write("")

        submitted = st.form_submit_button("Insert Employee")

    if submitted:
        payload = {"id": int(emp_id)}

        if name.strip():
            payload["name"] = name.strip()
        if dept.strip():
            payload["dept"] = dept.strip()
        if age.strip():
            payload["age"] = int(age.strip())
        if salary.strip():
            payload["salary"] = float(salary.strip())

        try:
            response = requests.post(f"{BASE_URL}/insert", json=payload, timeout=10)
            if response.status_code in [200, 201]:
                st.success("Employee inserted successfully")
            else:
                st.error(response.text)
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- UPDATE ---------------- #
elif menu == "Update Employee":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Update Employee")
    st.caption("Leave fields blank if you do not want to update them.")

    with st.form("update_form"):
        col1, col2 = st.columns(2)

        with col1:
            emp_id = st.number_input("Employee ID", min_value=1, step=1)
            name = st.text_input("New Name", placeholder="Optional")
            dept = st.text_input("New Department", placeholder="Optional")

        with col2:
            age = st.text_input("New Age", placeholder="Optional")
            salary = st.text_input("New Salary", placeholder="Optional")

        submitted = st.form_submit_button("Update Employee")

    if submitted:
        payload = {}
        try:
            if name.strip():
                payload["name"] = name.strip()
            if age.strip():
                payload["age"] = int(age.strip())
            if dept.strip():
                payload["dept"] = dept.strip()
            if salary.strip():
                payload["salary"] = float(salary.strip())
        except ValueError:
            st.error("Age must be an integer and Salary must be a number.")
        else:
            if not payload:
                st.warning("Please provide at least one field to update.")
            else:
                try:
                    response = requests.put(f"{BASE_URL}/update/{int(emp_id)}", json=payload, timeout=10)
                    if response.status_code == 200:
                        st.success("Employee updated successfully")
                    else:
                        st.error(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DELETE ---------------- #
elif menu == "Delete Employee":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Delete Employee")
    st.warning("This action is permanent.")

    with st.form("delete_form"):
        emp_id = st.number_input("Employee ID", min_value=1, step=1)
        submitted = st.form_submit_button("Delete Employee")

    if submitted:
        try:
            response = requests.delete(f"{BASE_URL}/delete/{int(emp_id)}", timeout=10)
            if response.status_code in [200, 204]:
                st.success("Employee deleted successfully")
            else:
                st.error(response.text)
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)
