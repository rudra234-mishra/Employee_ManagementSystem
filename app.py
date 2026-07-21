import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Employee Management",
    page_icon="👨‍💼",
    layout="wide"
)

# ─────────────────────────── THEME ───────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
* { font-family: 'Poppins', sans-serif !important; }

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1f3c 40%, #0f2d55 70%, #0a1628 100%);
    min-height: 100vh;
}

/* ── Main card ── */
.block-container {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(0,212,255,0.1);
    border-radius: 24px;
    padding: 2.5rem 3rem !important;
    box-shadow: 0 20px 60px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060d1a 0%, #0a1628 50%, #0d1f3c 100%) !important;
    border-right: 1px solid rgba(0,212,255,0.12) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.4);
}
section[data-testid="stSidebar"] * { color: #c8d8f0 !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    -webkit-text-fill-color: #c8d8f0 !important;
}

/* ── Title ── */
h1 {
    background: linear-gradient(90deg, #00d4ff, #7b61ff, #ff6b9d);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}

/* ── Section headers ── */
h2 {
    background: linear-gradient(90deg, #00d4ff, #7b61ff);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    margin-bottom: 1.5rem !important;
}

/* ── Body text ── */
p, label, span, div, .stCaption {
    color: #a0b4cc !important;
}

/* ── PRIMARY button — electric blue/purple ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #00d4ff 0%, #7b61ff 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.7rem 2rem !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.3px;
    box-shadow: 0 4px 20px rgba(0,212,255,0.4), 0 2px 8px rgba(123,97,255,0.3);
    transition: all 0.25s cubic-bezier(0.34,1.56,0.64,1) !important;
    width: 100%;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-3px) scale(1.04) !important;
    box-shadow: 0 8px 30px rgba(0,212,255,0.6), 0 4px 16px rgba(123,97,255,0.5) !important;
}
.stButton > button[kind="primary"]:active {
    transform: translateY(0) scale(0.97) !important;
}

/* ── SECONDARY button ── */
.stButton > button:not([kind="primary"]) {
    background: rgba(0,212,255,0.08) !important;
    color: #00d4ff !important;
    border: 1px solid rgba(0,212,255,0.3) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: rgba(0,212,255,0.18) !important;
    border-color: rgba(0,212,255,0.7) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 16px rgba(0,212,255,0.25) !important;
}

/* ── Metric cards ── */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(0,212,255,0.07) 0%, rgba(123,97,255,0.07) 100%);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 18px;
    padding: 20px 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05);
    transition: all 0.3s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: rgba(0,212,255,0.5);
    box-shadow: 0 8px 32px rgba(0,212,255,0.2);
}
div[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #00d4ff !important;
}
div[data-testid="stMetricLabel"] {
    color: #7b61ff !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.5px;
}

/* ── Inputs ── */
input, textarea {
    background: rgba(255,255,255,0.05) !important;
    color: #e0eaf8 !important;
    border: 1px solid rgba(0,212,255,0.2) !important;
    border-radius: 12px !important;
    transition: all 0.2s ease !important;
}
input:focus, textarea:focus {
    border-color: rgba(0,212,255,0.6) !important;
    box-shadow: 0 0 0 3px rgba(0,212,255,0.1), 0 0 16px rgba(0,212,255,0.15) !important;
}

/* ── Selectbox ── */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(0,212,255,0.2) !important;
    border-radius: 12px !important;
    color: #e0eaf8 !important;
}

/* ── Dataframe ── */
div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid rgba(0,212,255,0.15);
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

/* ── Alerts / banners ── */
div[data-testid="stAlert"] {
    border-radius: 14px !important;
    border: none !important;
}

/* ── Divider ── */
hr { border-color: rgba(0,212,255,0.1) !important; }

/* ── Number input arrows ── */
button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"] {
    background: rgba(0,212,255,0.1) !important;
    border-radius: 6px !important;
    color: #00d4ff !important;
}

/* ── Sidebar selectbox ── */
div[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: rgba(0,212,255,0.07) !important;
    border: 1px solid rgba(0,212,255,0.2) !important;
    color: #c8d8f0 !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────── HELPERS ───────────────────
def call(method, path, **kwargs):
    try:
        return requests.request(method, f"{BASE_URL}{path}", timeout=10, **kwargs)
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to the API. Make sure FastAPI is running.")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out.")
        return None


def card(label, value, color="#00d4ff"):
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(0,212,255,0.08),rgba(123,97,255,0.08));
                border:1px solid {color}33;border-radius:16px;padding:20px 16px;
                box-shadow:0 4px 20px rgba(0,0,0,0.3);text-align:center;margin-bottom:8px;">
        <div style="font-size:1.8rem;font-weight:800;color:{color}">{value}</div>
        <div style="font-size:0.8rem;font-weight:600;color:#7b61ff;margin-top:4px;letter-spacing:0.5px">{label}</div>
    </div>""", unsafe_allow_html=True)


# ─────────────────── DELETE DIALOG ───────────────────
@st.dialog("🗑️ Confirm Deletion")
def confirm_delete(emp_id):
    st.markdown(f"""
    <div style='text-align:center;padding:1rem;'>
        <div style='font-size:3rem'>⚠️</div>
        <h3 style='color:#ff6b9d;-webkit-text-fill-color:#ff6b9d'>Delete Employee #{emp_id}?</h3>
        <p style='color:#a0b4cc'>This action is permanent and cannot be undone.</p>
    </div>""", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ Yes, Delete", type="primary", use_container_width=True):
            r = call("DELETE", f"/delete/{int(emp_id)}")
            if r and r.status_code in [200, 203, 204]:
                st.toast(f"Employee #{emp_id} deleted successfully!", icon="🗑️")
            elif r:
                st.error(r.text)
            st.rerun()
    with c2:
        if st.button("❌ Cancel", use_container_width=True):
            st.rerun()


# ─────────────────── HEADER ───────────────────
st.title("👨‍💼 Employee Management System")
st.caption(f"🔗 API: `{BASE_URL}`")
st.divider()

# ─────────────────── SIDEBAR ───────────────────
st.sidebar.markdown("""
<div style='text-align:center;padding:1rem 0;'>
    <div style='font-size:2.5rem'>👨‍💼</div>
    <div style='font-size:1.1rem;font-weight:700;color:#00d4ff;margin-top:6px'>EMS Portal</div>
    <div style='font-size:0.75rem;color:#5a7a9a;margin-top:2px'>Employee Management</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.divider()

menu = st.sidebar.selectbox("📂 Select Operation", (
    "📋 View Employees",
    "🔍 Fetch Employee",
    "➕ Insert Employee",
    "✏️ Update Employee",
    "🗑️ Delete Employee"
))

st.sidebar.divider()
st.sidebar.markdown("<div style='color:#5a7a9a;font-size:0.75rem;text-align:center'>Click a button to call the API</div>",
                    unsafe_allow_html=True)


# ══════════════════════════════════════════
# VIEW  →  GET /view
# ══════════════════════════════════════════
if menu == "📋 View Employees":
    st.markdown("## 📋 View Employees")

    if st.button("📥 Load Employees", type="primary"):
        with st.spinner("Fetching from GET /view …"):
            response = requests.get(f"{BASE_URL}/view")

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and data:
                df = pd.DataFrame(data)

                # Metrics
                m1, m2, m3, m4 = st.columns(4)
                with m1: card("Total Employees", len(df), "#00d4ff")
                with m2: card("Departments",     df["Dept"].nunique()          if "Dept"   in df.columns else "—", "#7b61ff")
                with m3: card("Avg Salary",      f"{df['Salary'].mean():,.0f}" if "Salary" in df.columns else "—", "#00d4ff")
                with m4: card("Max Salary",      f"{df['Salary'].max():,.0f}"  if "Salary" in df.columns else "—", "#ff6b9d")
                st.divider()

                # Filters
                f1, f2 = st.columns([3, 1])
                with f1:
                    q = st.text_input("🔎 Search by name", placeholder="Start typing a name…")
                with f2:
                    depts = ["All"] + sorted(df["Dept"].dropna().unique().tolist()) if "Dept" in df.columns else ["All"]
                    dept_f = st.selectbox("Department", depts)

                fdf = df.copy()
                if q and "Name" in fdf.columns:
                    fdf = fdf[fdf["Name"].str.contains(q, case=False, na=False)]
                if dept_f != "All":
                    fdf = fdf[fdf["Dept"] == dept_f]

                st.caption(f"Showing **{len(fdf)}** of **{len(df)}** records")
                st.divider()

                # Row-by-row table with delete button
                id_col = "Id" if "Id" in fdf.columns else fdf.columns[0]
                hc = st.columns([1, 2, 1, 2, 2, 1])
                for h, t in zip(hc, ["ID", "Name", "Age", "Dept", "Salary", "Delete"]):
                    h.markdown(f"<span style='color:#00d4ff;font-weight:700;font-size:0.82rem;letter-spacing:0.5px'>{t}</span>",
                               unsafe_allow_html=True)
                st.markdown("<hr style='margin:4px 0 10px 0'>", unsafe_allow_html=True)

                for _, row in fdf.iterrows():
                    rid = row.get(id_col)
                    c1, c2, c3, c4, c5, c6 = st.columns([1, 2, 1, 2, 2, 1])
                    c1.markdown(f"<span style='color:#7b61ff;font-weight:700'>#{rid}</span>", unsafe_allow_html=True)
                    c2.write(row.get("Name",   ""))
                    c3.write(row.get("Age",    ""))
                    c4.write(row.get("Dept",   ""))
                    sal = row.get("Salary", 0)
                    c5.write(f"{sal:,.0f}" if isinstance(sal, (int, float)) else sal)
                    if c6.button("🗑️", key=f"del_{rid}", help=f"Delete employee #{rid}"):
                        confirm_delete(rid)

            else:
                st.info("No employees found in the database.")
        else:
            st.error(response.text)


# ══════════════════════════════════════════
# FETCH  →  GET /fetch/{id}
# ══════════════════════════════════════════
elif menu == "🔍 Fetch Employee":
    st.markdown("## 🔍 Fetch Employee")
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns([3, 1])
    with c1:
        emp_id = st.number_input("Employee ID", min_value=1, step=1)
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        fetch_btn = st.button("🔍 Fetch", type="primary", use_container_width=True)

    if fetch_btn:
        with st.spinner(f"Calling GET /fetch/{int(emp_id)} …"):
            response = requests.get(f"{BASE_URL}/fetch/{emp_id}")

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and data:
                rec = data[0]
                st.success(f"✅ Employee #{int(emp_id)} found!")
                st.divider()
                c1, c2, c3, c4, c5 = st.columns(5)
                with c1: card("ID",     rec.get("Id",     "—"), "#00d4ff")
                with c2: card("Name",   rec.get("Name",   "—"), "#7b61ff")
                with c3: card("Age",    rec.get("Age",    "—"), "#00d4ff")
                with c4: card("Dept",   rec.get("Dept",   "—"), "#7b61ff")
                sal = rec.get("Salary", 0)
                with c5: card("Salary", f"{sal:,.0f}" if isinstance(sal, (int, float)) else sal, "#ff6b9d")
            else:
                st.dataframe(pd.DataFrame(response.json()), use_container_width=True)
        else:
            st.error(response.json().get("detail", response.text))


# ══════════════════════════════════════════
# INSERT  →  POST /insert
# fields: id, name, age, dept, salary
# ══════════════════════════════════════════
elif menu == "➕ Insert Employee":
    st.markdown("## ➕ Insert Employee")
    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("insert_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            emp_id = st.number_input("🆔 ID",     min_value=1,  step=1)
            name   = st.text_input ("👤 Name")
            age    = st.number_input("🎂 Age",    min_value=18, step=1)
        with c2:
            dept   = st.text_input ("🏢 Department")
            salary = st.number_input("💰 Salary", min_value=0.0, step=1000.0)

        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("✅ Insert Employee", type="primary", use_container_width=True)

    if submit:
        if not name.strip() or not dept.strip():
            st.warning("⚠️ Name and Department cannot be empty.")
        else:
            payload = {
                "id":     int(emp_id),
                "name":   name,
                "age":    int(age),
                "dept":   dept,
                "salary": float(salary)
            }
            with st.spinner("Calling POST /insert …"):
                response = requests.post(f"{BASE_URL}/insert", json=payload)

            if response.status_code in [200, 201]:
                st.success("🎉 Employee Inserted Successfully!")
                st.balloons()
            else:
                st.error(response.text)


# ══════════════════════════════════════════
# UPDATE  →  PUT /update/{id}
# fields: name, age, dept, salary (optional)
# ══════════════════════════════════════════
elif menu == "✏️ Update Employee":
    st.markdown("## ✏️ Update Employee")
    st.caption("Leave any field blank to keep its existing value.")
    st.markdown("<br>", unsafe_allow_html=True)

    emp_id = st.number_input("🆔 Employee ID", min_value=1, step=1)
    st.divider()

    with st.form("update_form"):
        c1, c2 = st.columns(2)
        with c1:
            name   = st.text_input("👤 New Name")
            age    = st.text_input("🎂 New Age")
        with c2:
            dept   = st.text_input("🏢 New Department")
            salary = st.text_input("💰 New Salary")

        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("💾 Update Employee", type="primary", use_container_width=True)

    if submit:
        payload = {}
        if name.strip():   payload["name"]   = name.strip()
        if age.strip():
            try:            payload["age"]    = int(age.strip())
            except ValueError:
                st.warning("⚠️ Age must be a whole number."); st.stop()
        if dept.strip():   payload["dept"]   = dept.strip()
        if salary.strip():
            try:            payload["salary"] = float(salary.strip())
            except ValueError:
                st.warning("⚠️ Salary must be a number."); st.stop()

        if not payload:
            st.warning("⚠️ Fill in at least one field to update.")
        else:
            with st.spinner(f"Calling PUT /update/{int(emp_id)} …"):
                response = requests.put(f"{BASE_URL}/update/{emp_id}", json=payload)

            if response.status_code == 200:
                st.success(str(response.json()))
            else:
                st.error(response.text)


# ══════════════════════════════════════════
# DELETE  →  DELETE /delete/{id}
# ══════════════════════════════════════════
elif menu == "🗑️ Delete Employee":
    st.markdown("## 🗑️ Delete Employee")
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns([3, 1])
    with c1:
        emp_id = st.number_input("🆔 Employee ID", min_value=1, step=1)
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Delete Employee", type="primary", use_container_width=True):
            confirm_delete(int(emp_id))