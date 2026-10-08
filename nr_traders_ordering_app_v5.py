import streamlit as st 
import pandas as pd 
import datetime 
import io 
import json

# PAGE CONFIGURATION ---
st.set_page_config( 
    page_title="N R TRADERS - Gas Ordering & CRM", 
    page_icon="🏭", 
    layout="wide", 
    initial_sidebar_state="expanded" 
)

# CUSTOM CSS STYLING ---
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0E2F44 0%, #1E517B 100%);
        color: white;
        padding: 22px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .status-confirmed {
        background-color: #E3F2FD;
        border: 1px solid #2196F3;
        padding: 12px;
        border-radius: 8px;
        color: #0D47A1;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# USER DATABASE (CUSTOM PASSWORDS FOR ADMIN & PARTIES) ---
if "users_db" not in st.session_state: 
    st.session_state.users_db = { 
        "admin": { "password": "admin123", "role": "admin", "name": "Mr. Nitin Sharma", "company": "N R TRADERS" }, 
        "ar_fabtech": { "password": "party123", "role": "party", "name": "AR Fabtech Innovation", "company": "AR Fabtech Innovation", "address": "Sahibabad" }, 
        "shree_ji": { "password": "shree123", "role": "party", "name": "Shree Ji Coil Solution", "company": "SHREE JI COIL SOLUTION", "address": "Duhai" } 
    }

# INITIAL SESSION STATE DATA ---
if "logged_in_user" not in st.session_state: st.session_state.logged_in_user = None
if "orders" not in st.session_state: st.session_state.orders = []
if "bills" not in st.session_state: st.session_state.bills = []
if "grievances" not in st.session_state: st.session_state.grievances = []
if "cart_filled" not in st.session_state: st.session_state.cart_filled = []
if "cart_empty" not in st.session_state: st.session_state.cart_empty = []

# GAS SPECIFICATIONS & COLOUR CODES ---
GAS_SPECS = { 
    "Oxygen (O2)": {"categories": ["Standard (7 m³)"]}, 
    "Carbon Dioxide (CO2)": {"categories": ["Personalised 20kg", "Standard 30kg", "Commercial 45kg"]}, 
    "Argon (Ar)": {"categories": ["7 cubic metres", "10 cubic metres"]}, 
    "Nitrogen (N2)": {"categories": ["Standard (7 m³)"]}, 
    "Dissolved Acetylene (DA)": {"categories": ["Standard DA Cylinder"]}, 
    "Hydrogen (H2)": {"categories": ["Standard (7 m³)"]} 
}

# APP HEADER ---
st.markdown("""
<div class="main-header">
    <h1 style="margin:0;">🏭 N R TRADERS</h1>
    <p style="margin:5px 0 0 0; font-size: 16px; opacity:0.9;">Industrial & Medical Gas Cylinders Ordering, Billing & Cloud Sync Portal</p>
</div>
""", unsafe_allow_html=True)

# LOGIN / AUTHENTICATION SIDEBAR ---
st.sidebar.markdown("### 🔐 User Login")
if st.session_state.logged_in_user is None: 
    with st.sidebar.form("login_form"): 
        login_id = st.text_input("User ID:").strip().lower() 
        login_pass = st.text_input("Password:", type="password") 
        if st.form_submit_button("Login"):
            if login_id in st.session_state.users_db and st.session_state.users_db[login_id]["password"] == login_pass:
                st.session_state.logged_in_user = login_id
                st.rerun()
            else:
                st.sidebar.error("❌ Invalid ID or Password!")
else: 
    u_info = st.session_state.users_db[st.session_state.logged_in_user] 
    st.sidebar.success(f"Logged in as: {u_info['name']}") 
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in_user = None
        st.rerun()

# =========================================================================
# ONLY RUN PORTALS IF A USER IS LOGGED IN
# =========================================================================
if st.session_state.logged_in_user is not None:
    role = st.session_state.users_db[st.session_state.logged_in_user]["role"]
    
    # ---------------------------------------------------------
    # PORTAL 1: CUSTOMER / PARTY DASHBOARD
    # ---------------------------------------------------------
    if role == "party": 
        curr_user_id = st.session_state.logged_in_user 
        curr_user_info = st.session_state.users_db[curr_user_id]
        
        tab1, tab2, tab3, tab4 = st.tabs(["🛒 Cylinder Orders", "📄 View Bills", "💳 Payment Portal", "⚠️ Grievance & Support"])

        # TAB 1: ORDER CYLINDERS
        with tab1:
            st.subheader("📝 Order & Empty Cylinders Tracking")
            c_p1, c_p2 = st.columns(2)
            
            with c_p1:
                st.markdown("### 🟢 FILLED CYLINDERS REQUIRED")
                fgas = st.selectbox("Select Gas Type:", list(GAS_SPECS.keys()), key="f_gas")
                fcat = st.selectbox("Select Size:", GAS_SPECS[fgas]["categories"], key="f_cat")
                fqty = st.number_input("Quantity:", min_value=1, value=5, key="f_qty")
                if st.button("➕ Add Filled Cylinder"):
                    st.session_state.cart_filled.append({"Gas": fgas, "Size": fcat, "Qty": fqty})
                if st.session_state.cart_filled:
                    st.dataframe(pd.DataFrame(st.session_state.cart_filled), use_container_width=True)

            with c_p2:
                st.markdown("### 🔴 EMPTY CYLINDERS AT SITE")
                egas = st.selectbox("Select Gas Type:", list(GAS_SPECS.keys()), key="e_gas")
                ecat = st.selectbox("Select Size:", GAS_SPECS[egas]["categories"], key="e_cat")
                eqty = st.number_input("Quantity:", min_value=0, value=3, key="e_qty")
                if st.button("➕ Add Empty Cylinder"):
                    st.session_state.cart_empty.append({"Gas": egas, "Size": ecat, "Qty": eqty})
                if st.session_state.cart_empty:
                    st.dataframe(pd.DataFrame(st.session_state.cart_empty), use_container_width=True)

            if st.button("🚀 SUBMIT ORDER", type="primary", use_container_width=True):
                if st.session_state.cart_filled or st.session_state.cart_empty:
                    st.session_state.orders.insert(0, {
                        "order_id": f"ORD-{len(st.session_state.orders) + 101}",
                        "party_name": curr_user_info["company"],
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "filled_items": st.session_state.cart_filled.copy(),
                        "empty_items": st.session_state.cart_empty.copy(),
                        "status": "Pending",
                        "eta": "Awaiting Confirmation",
                        "vehicle": "TBA"
                    })
                    st.session_state.cart_filled, st.session_state.cart_empty = [], []
                    st.success("✅ Order Submitted Successfully!")
                    st.rerun()

            st.markdown("---")
            st.subheader("📋 My Order History")
            my_orders = [o for o in st.session_state.orders if o["party_name"] == curr_user_info["company"]]
            for o in my_orders:
                st.markdown(f"**Order {o['order_id']}** | Status: `{o['status']}` | ETA: `{o['eta']}`")

        # TAB 2: BILLS
        with tab2:
            st.subheader("📄 GST Tax Invoices")
            my_bills = [b for b in st.session_state.bills if b["party_name"] == curr_user_info["company"]]
            if my_bills:
                for b in my_bills:
                    st.markdown(f"### Invoice #{b['bill_no']} - ₹{b['amount']}")
            else:
                st.info("No invoices uploaded yet.")

        # TAB 3: PAYMENT PORTAL
        with tab3:
            st.subheader("💳 Secure Payment Portal")
            st.markdown("""
            **🏦 HDFC Bank Details (NEFT/RTGS/IMPS):**
            * **Account Name:** N R TRADERS
            * **Account Number:** 502000XXXXXXX
            * **IFSC Code:** HDFC000XXXX
            * **Branch:** Ghaziabad
            
            **📱 UPI Payment:**
            * **UPI ID / Paytm Business:** `nrtraders.admin@paytm`
            """)
            st.success("Please mention your Company Name in payment remarks for quick ledger updates.")

        # TAB 4: GRIEVANCE PORTAL WITH IMAGE/VIDEO
        with tab4:
            st.subheader("⚠️ Grievance & Issue Reporting")
            st.markdown("Report issues regarding defective cylinders, wrong delivery, or billing. You can upload photos/videos as evidence.")
            
            with st.form("grievance_form"):
                g_type = st.selectbox("Issue Category:", ["Cylinder Leakage/Defect", "Delivery Delay", "Billing/Payment Issue", "Other"])
                g_desc = st.text_area("Describe the issue in detail:")
                g_file = st.file_uploader("Upload Image or Video (Optional):", type=['png', 'jpg', 'jpeg', 'mp4', 'mov'])
                
                if st.form_submit_button("🚨 Submit Grievance"):
                    if g_desc:
                        st.session_state.grievances.append({
                            "party": curr_user_info["company"],
                            "type": g_type,
                            "desc": g_desc,
                            "file": g_file.name if g_file else "No File Attached",
                            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "status": "Pending Review"
                        })
                        st.success("Your grievance has been submitted securely. N R Traders Admin will review it shortly.")
                    else:
                        st.error("Please provide a description of the issue.")

    # ---------------------------------------------------------
    # PORTAL 2: ADMIN & CRM DASHBOARD (OWNER)
    # ---------------------------------------------------------
    elif role == "admin": 
        st.subheader("⚙️ N R TRADERS Owner CRM") 
        ad_tab1, ad_tab2, ad_tab3 = st.tabs(["📥 Live Orders", "📤 Upload Bills", "⚠️ Grievances"])

        with ad_tab1:
            st.markdown("### 📥 Live Party Orders")
            for idx, o in enumerate(st.session_state.orders):
                st.markdown(f"**Order #{o['order_id']} - {o['party_name']}**")
                if o["status"] == "Pending":
                    eta = st.selectbox("Set ETA:", ["30 Mins", "1 Hour", "Custom"], key=f"eta_{idx}")
                    veh = st.selectbox("Vehicle:", ["BOLERO UP14LT6202"], key=f"veh_{idx}")
                    if st.button("Confirm Order", key=f"btn_{idx}"):
                        st.session_state.orders[idx]["status"] = "Accepted"
                        st.session_state.orders[idx]["eta"] = eta
                        st.session_state.orders[idx]["vehicle"] = veh
                        st.rerun()
                else:
                    st.info(f"✅ Confirmed | ETA: {o['eta']} | Vehicle: {o['vehicle']}")
                st.markdown("---")

        with ad_tab2:
            st.markdown("### 📤 Upload Invoice")
            with st.form("bill_form"):
                p_id = st.selectbox("Select Party:", [u for u, d in st.session_state.users_db.items() if d["role"] == "party"])
                amt = st.number_input("Invoice Total (₹):")
                if st.form_submit_button("Upload Invoice"):
                    st.session_state.bills.append({
                        "bill_no": f"2026-27/{len(st.session_state.bills)+1}",
                        "party_name": st.session_state.users_db[p_id]["company"],
                        "amount": amt
                    })
                    st.success("Invoice Uploaded!")
                    
        with ad_tab3:
            st.markdown("### ⚠️ Customer Grievances & Uploaded Files")
            if not st.session_state.grievances:
                st.info("No active grievances.")
            for g in reversed(st.session_state.grievances):
                st.error(f"**Party:** {g['party']} | **Date:** {g['date']}")
                st.markdown(f"**Issue:** {g['type']}")
                st.markdown(f"**Description:** {g['desc']}")
                st.markdown(f"**Attached Evidence:** `{g['file']}`")
                st.markdown("---")
