import streamlit as st 
import pandas as pd 
import datetime 
import io 
import json
import os

# --- PERMANENT DRIVE STORAGE SETTINGS ---
USERS_FILE = "nrt_users.json"
ORDERS_FILE = "nrt_orders.json"
BILLS_FILE = "nrt_bills.json"

DEFAULT_USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin",
        "name": "Mr. Nitin Sharma (Owner)",
        "company": "N R TRADERS",
        "address": "Duhai Industrial Area, Ghaziabad",
        "email": "nrtraders.gases@gmail.com"
    }
}

def load_data(file_path, default_data):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default_data
    else:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4)
        return default_data

def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

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
    .gas-card {
        border-radius: 10px;
        padding: 15px;
        color: white;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .card-filled {
        background-color: #E8F5E9;
        border-left: 6px solid #2E7D32;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .card-empty {
        background-color: #FFEBEE;
        border-left: 6px solid #C62828;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .status-confirmed {
        background-color: #E3F2FD;
        border: 1px solid #2196F3;
        padding: 12px;
        border-radius: 8px;
        color: #0D47A1;
        font-weight: bold;
    }
    .bill-box {
        background-color: #FAFAFA;
        border: 1px solid #E0E0E0;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# LOAD PERSISTENT DATA INTO SESSION STATE ---
if "users_db" not in st.session_state:
    st.session_state.users_db = load_data(USERS_FILE, DEFAULT_USERS)

if "orders" not in st.session_state:
    st.session_state.orders = load_data(ORDERS_FILE, [])

if "bills" not in st.session_state:
    st.session_state.bills = load_data(BILLS_FILE, [])

if "logged_in_user" not in st.session_state: 
    st.session_state.logged_in_user = None

if "cart_filled" not in st.session_state: 
    st.session_state.cart_filled = []

if "cart_empty" not in st.session_state: 
    st.session_state.cart_empty = []

# APP HEADER ---
st.markdown("""
<div class="main-header">
    <h1 style="margin:0;">🏭 N R TRADERS</h1>
    <p style="margin:5px 0 0 0; font-size: 16px; opacity:0.9;">Industrial & Medical Gas Cylinders Ordering, Billing & CRM Portal</p>
    <p style="margin:2px 0 0 0; font-size: 13px; opacity:0.75;">GSTIN: 09MHSPS5749H1Z3 | MSME: UDYAM-UP-29-0162343</p>
</div>
""", unsafe_allow_html=True)

# GAS SPECIFICATIONS ---
GAS_SPECS = { 
    "Oxygen (O2)": {"bg_color": "#1A1A1A", "border_color": "#FFFFFF", "neck_color": "⬜ White Neck", "body_color": "⬛ Black Body", "text_color": "#FFFFFF", "categories": ["Standard (7 m³)"], "desc": "Industrial Metal Cutting, Welding & Medical Breath Support"}, 
    "Carbon Dioxide (CO2)": {"bg_color": "#212121", "border_color": "#757575", "neck_color": "⬛ Black Neck", "body_color": "⬛ Black Body", "text_color": "#FFFFFF", "categories": ["Personalised 20kg", "Standard 30kg", "Commercial 45kg"], "desc": "MIG Welding Shielding, Beverage Carbonation & Fire Fighting"}, 
    "Argon (Ar)": {"bg_color": "#0D47A1", "border_color": "#42A5F5", "neck_color": "🟦 Navy Blue Neck", "body_color": "🟦 Navy Blue Body", "text_color": "#FFFFFF", "categories": ["7 cubic metres", "10 cubic metres"], "desc": "TIG Welding Shielding, Stainless Steel Fabrication & Precision Alloys"}, 
    "Nitrogen (N2)": {"bg_color": "#78909C", "border_color": "#212121", "neck_color": "⬛ Black Neck", "body_color": "🌫️ French Grey Body", "text_color": "#FFFFFF", "categories": ["Standard (7 m³)"], "desc": "Laser Cutting Inerting, Pressure Testing, Purging & Chemical Processing"}, 
    "Dissolved Acetylene (DA)": {"bg_color": "#8D6E63", "border_color": "#3E2723", "neck_color": "🟫 Brownish Red Neck", "body_color": "🟫 Brownish Red Body", "text_color": "#FFFFFF", "categories": ["Standard DA Cylinder"], "desc": "Oxy-Acetylene High-Temperature Heavy Metal Cutting & Brazing"}, 
    "Hydrogen (H2)": {"bg_color": "#D32F2F", "border_color": "#FF8A80", "neck_color": "🟥 Scarlet Red Neck", "body_color": "🟥 Scarlet Red Body", "text_color": "#FFFFFF", "categories": ["Standard (7 m³)"], "desc": "High-Precision Cutting, Heat Treatment & Special Laboratory Atmospheres"} 
}

# LOGIN / AUTHENTICATION SIDEBAR ---
st.sidebar.markdown("### 🔐 User Login")

if st.session_state.logged_in_user is None: 
    st.sidebar.info("Please login to access your confidential dashboard.") 
    
    with st.sidebar.form("login_form"): 
        login_id = st.text_input("User ID / Party ID:").strip().lower() 
        login_pass = st.text_input("Password:", type="password") 
        submit_login = st.form_submit_button("Login")

    if submit_login:
        users = st.session_state.users_db
        if login_id in users and users[login_id]["password"] == login_pass:
            st.session_state.logged_in_user = login_id
            st.sidebar.success(f"Welcome, {users[login_id]['name']}!")
            st.rerun()
        else:
            st.sidebar.error("❌ Invalid User ID or Password! Please verify your credentials.")
else: 
    u_info = st.session_state.users_db[st.session_state.logged_in_user] 
    st.sidebar.success(f"Logged in as: {u_info['name']}") 
    st.sidebar.caption(f"Role: {u_info['role'].upper()} | Company: {u_info['company']}")
    if u_info.get('email'):
        st.sidebar.caption(f"📧 Gmail: {u_info['email']}")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in_user = None
        st.rerun()

st.sidebar.markdown("---") 
st.sidebar.markdown("### 🏢 N R TRADERS Contact Info") 
st.sidebar.markdown("📞 Call: +91 9999734204") 
st.sidebar.markdown("📞 Call: +91 8130853589") 
st.sidebar.markdown("✉️ Email: nrtraders.gases@gmail.com") 
st.sidebar.markdown("📍 Office & Godown: Duhai Industrial Area, Ghaziabad, UP") 

# PUBLIC VIEW (CATALOG) ---
if st.session_state.logged_in_user is None: 
    st.subheader("🏭 Gas Cylinder Catalog") 
    st.markdown("Please log in from the sidebar to place orders and manage your invoices.")

    st.markdown("---")
    cols = st.columns(3)
    for idx, (gas_name, spec) in enumerate(GAS_SPECS.items()):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="gas-card" style="background-color: {spec['bg_color']}; border: 2px solid {spec['border_color']}; color: {spec['text_color']};">
                <h3 style="margin:0;">🛢️ {gas_name}</h3>
                <p style="margin:5px 0;"><b>Neck Color:</b> {spec['neck_color']}</p>
                <p style="margin:5px 0;"><b>Body Color:</b> {spec['body_color']}</p>
                <p style="margin:5px 0;"><b>Available Sizes:</b> {', '.join(spec['categories'])}</p>
                <hr style="margin:8px 0; border-color: rgba(255,255,255,0.2);">
                <p style="margin:0; font-size:12px; opacity:0.9;"><i>{spec['desc']}</i></p>
            </div>
            """, unsafe_allow_html=True)

# AUTHENTICATED PORTALS ---
if st.session_state.logged_in_user is not None:

    # 1. CUSTOMER / PARTY PORTAL
    if st.session_state.users_db[st.session_state.logged_in_user]["role"] == "party": 
        curr_user_id = st.session_state.logged_in_user 
        curr_user_info = st.session_state.users_db[curr_user_id]
        user_email = curr_user_info.get("email", "Not Provided")

        party_bills = [b for b in st.session_state.bills if b.get("party_id") == curr_user_id]
        unread_bills_count = sum(1 for b in party_bills if b.get("unread", False))
        bill_tab_label = f"📄 View Bills (🔴 {unread_bills_count} New)" if unread_bills_count > 0 else "📄 View Bills"

        tab1, tab2, tab3 = st.tabs(["🛒 Place Cylinder Order", bill_tab_label, "📞 Help & Support"])

        with tab1:
            st.subheader("📝 Order Gas Cylinders & Report Empty Cylinders")
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                st.text_input("🏢 Party / Customer Name:", value=curr_user_info["company"], disabled=True)
            with c_p2:
                st.text_input("📍 Delivery Address:", value=curr_user_info.get("address", ""), disabled=True)
                
            st.markdown("---")
            col_filled, col_empty = st.columns(2)
            
            with col_filled:
                st.markdown("<div class='card-filled'><h3>🟢 FILLED CYLINDERS REQUIRED</h3></div>", unsafe_allow_html=True)
                fgas = st.selectbox("Select Gas Type (Filled):", list(GAS_SPECS.keys()), key="f_gas_sel")
                fcat = st.selectbox("Select Category / Size:", GAS_SPECS[fgas]["categories"], key="f_cat_sel")
                fqty = st.number_input("Number of Cylinders:", min_value=1, max_value=500, value=5, step=1, key="f_qty_sel")
                
                if st.button("➕ Add Filled Cylinder Item"):
                    st.session_state.cart_filled.append({"Gas Type": fgas, "Category / Size": fcat, "Quantity": fqty})
                    st.success(f"Added {fqty} x {fgas} ({fcat})!")
                    
                if st.session_state.cart_filled:
                    st.dataframe(pd.DataFrame(st.session_state.cart_filled), use_container_width=True)
                    if st.button("🗑️ Clear Filled List"):
                        st.session_state.cart_filled = []
                        st.rerun()

            with col_empty:
                st.markdown("<div class='card-empty'><h3>🔴 EMPTY CYLINDERS AT SITE</h3></div>", unsafe_allow_html=True)
                egas = st.selectbox("Select Gas Type (Empty):", list(GAS_SPECS.keys()), key="e_gas_sel")
                ecat = st.selectbox("Select Category / Size (Empty):", GAS_SPECS[egas]["categories"], key="e_cat_sel")
                eqty = st.number_input("Number of Empty Cylinders:", min_value=0, max_value=500, value=0, step=1, key="e_qty_sel")
                
                if st.button("➕ Add Empty Cylinder Item"):
                    st.session_state.cart_empty.append({"Gas Type": egas, "Category / Size": ecat, "Quantity": eqty})
                    st.success(f"Reported {eqty} x {egas} ({ecat})!")
                    
                if st.session_state.cart_empty:
                    st.dataframe(pd.DataFrame(st.session_state.cart_empty), use_container_width=True)
                    if st.button("🗑️ Clear Empty List"):
                        st.session_state.cart_empty = []
                        st.rerun()

            st.markdown("---")
            if st.button("🚀 SUBMIT ORDER", type="primary", use_container_width=True):
                if not st.session_state.cart_filled and not st.session_state.cart_empty:
                    st.error("Please add at least one item before submitting!")
                else:
                    new_ord_id = f"NRT-ORD-{len(st.session_state.orders) + 101}"
                    new_order = {
                        "order_id": new_ord_id,
                        "party_id": curr_user_id,
                        "party_name": curr_user_info["company"],
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "filled_items": st.session_state.cart_filled.copy(),
                        "empty_items": st.session_state.cart_empty.copy(),
                        "status": "Pending Confirmation",
                        "eta": "Awaiting Confirmation",
                        "vehicle": "To be assigned",
                        "email_sync": user_email
                    }
                    st.session_state.orders.insert(0, new_order)
                    save_data(ORDERS_FILE, st.session_state.orders)
                    st.session_state.cart_filled = []
                    st.session_state.cart_empty = []
                    st.balloons()
                    st.success(f"✅ Order #{new_ord_id} Submitted Successfully!")
                    if user_email != "Not Provided":
                        st.info(f"📧 Order receipt details auto-synced to your Gmail: **{user_email}**")

            st.markdown("---")
            st.subheader("📋 Order History")
            my_orders = [o for o in st.session_state.orders if o.get("party_id") == curr_user_id]
            if my_orders:
                for ord_item in my_orders:
                    st.markdown(f"#### 📦 Order #{ord_item['order_id']} ({ord_item['timestamp']})")
                    st.markdown(f"**Status:** `{ord_item['status']}` | **ETA:** `{ord_item['eta']}` | **Vehicle:** `{ord_item['vehicle']}`")
                    st.markdown("---")
            else:
                st.write("No previous orders found.")

        with tab2:
            st.subheader("📄 GST Invoices")
            if party_bills:
                for b_idx, bill in enumerate(party_bills):
                    if bill.get("unread", False):
                        bill["unread"] = False
                        save_data(BILLS_FILE, st.session_state.bills)
                        
                    st.markdown(f"""
                    <div class="bill-box">
                        <h3 style="margin:0; color:#0E2F44;">🧾 Tax Invoice #{bill['bill_no']}</h3>
                        <p style="margin:3px 0;"><b>Date:</b> {bill['date']} | <b>Grand Total:</b> ₹{bill['amount']:,.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No tax invoices issued yet.")

        with tab3:
            st.subheader("📞 Help & Support")
            st.markdown("Call: +91 9999734204 / +91 8130853589")

    # 2. ADMIN PORTAL (CRM)
    elif st.session_state.users_db[st.session_state.logged_in_user]["role"] == "admin": 
        st.subheader("⚙️ N R TRADERS Admin CRM") 

        admin_tab1, admin_tab2, admin_tab3 = st.tabs(["📥 Orders Queue", "📤 Upload Invoices", "🔐 Party User Management"])

        with admin_tab1:
            st.markdown("### 📥 Live Party Orders")
            if not st.session_state.orders:
                st.info("No orders received yet.")
            for idx, ord_item in enumerate(st.session_state.orders):
                st.markdown(f"#### 📦 Order #{ord_item['order_id']} - {ord_item['party_name']} ({ord_item['timestamp']})")
                
                ca, cb = st.columns(2)
                with ca:
                    st.markdown("**🟢 FILLED:**")
                    if ord_item["filled_items"]:
                        st.dataframe(pd.DataFrame(ord_item["filled_items"]), use_container_width=True)
                with cb:
                    st.markdown("**🔴 EMPTY:**")
                    if ord_item["empty_items"]:
                        st.dataframe(pd.DataFrame(ord_item["empty_items"]), use_container_width=True)

                if ord_item["status"] == "Pending Confirmation":
                    e1, e2 = st.columns(2)
                    with e1:
                        final_eta = st.selectbox("ETA:", ["30 Mins", "45 Mins", "1 Hour", "2 Hours"], key=f"eta_{ord_item['order_id']}")
                    with e2:
                        final_veh = st.selectbox("Vehicle:", ["BOLERO UP14LT6202", "TEMPO UP14AT1122", "GODOWN PICKUP"], key=f"veh_{ord_item['order_id']}")
                    if st.button(f"✅ Confirm Order #{ord_item['order_id']}", key=f"btn_{ord_item['order_id']}"):
                        st.session_state.orders[idx]["status"] = "Accepted"
                        st.session_state.orders[idx]["eta"] = final_eta
                        st.session_state.orders[idx]["vehicle"] = final_veh
                        save_data(ORDERS_FILE, st.session_state.orders)
                        st.rerun()
                else:
                    st.markdown(f"<div class='status-confirmed'>✅ Confirmed | ETA: {ord_item['eta']} | Vehicle: {ord_item['vehicle']}</div>", unsafe_allow_html=True)
                st.markdown("---")

        with admin_tab2:
            st.markdown("### 📤 Upload GST Invoice")
            parties = [uid for uid, uinfo in st.session_state.users_db.items() if uinfo["role"] == "party"]
            if not parties:
                st.warning("Please create a party account first in the User Management tab.")
            else:
                with st.form("crm_upload_invoice_form"):
                    u_party_id = st.selectbox("Select Party:", parties)
                    u_inv_no = st.text_input("Invoice No:", value=f"2026-27/{len(st.session_state.bills) + 1}")
                    u_amount = st.number_input("Total Amount (₹):", value=1000.0)
                    submit_invoice = st.form_submit_button("Upload Invoice to Client Profile")
                    
                    if submit_invoice:
                        party_comp_name = st.session_state.users_db[u_party_id]["company"]
                        party_email = st.session_state.users_db[u_party_id].get("email", "Not Provided")
                        new_bill = {
                            "bill_no": u_inv_no,
                            "party_id": u_party_id,
                            "party_name": party_comp_name,
                            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                            "amount": u_amount,
                            "unread": True
                        }
                        st.session_state.bills.insert(0, new_bill)
                        save_data(BILLS_FILE, st.session_state.bills)
                        st.success(f"Invoice uploaded for {party_comp_name}!")
                        if party_email != "Not Provided":
                            st.info(f"📧 Notification and Invoice data synced to client Gmail: **{party_email}**")

        with admin_tab3:
            st.markdown("### 🔐 Party Management (CRM Center)")
            
            with st.form("create_user_form"):
                st.markdown("#### ➕ Create New Client Profile")
                nu_id = st.text_input("Party Username / ID (lowercase, no spaces, e.g. 'ar_fabtech'):").strip().lower()
                nu_comp = st.text_input("Company / Firm Name:")
                nu_name = st.text_input("Contact Person Name:")
                nu_email = st.text_input("Client Gmail / Email Address:")
                nu_pass = st.text_input("Assign Secure Password:")
                nu_addr = st.text_input("Delivery Address:")
                submit_new_user = st.form_submit_button("🔑 Save Party Account")

                if submit_new_user:
                    if nu_id in st.session_state.users_db:
                        st.error("User ID already exists! Please choose a unique ID.")
                    elif not nu_id or not nu_pass or not nu_comp:
                        st.error("Please fill in Username, Company, and Password fields.")
                    else:
                        st.session_state.users_db[nu_id] = {
                            "password": nu_pass,
                            "role": "party",
                            "name": nu_name if nu_name else nu_comp,
                            "company": nu_comp,
                            "email": nu_email,
                            "address": nu_addr
                        }
                        save_data(USERS_FILE, st.session_state.users_db)
                        st.success(f"Profile for `{nu_id}` saved successfully! The client can now log in.")
                        st.rerun()

            st.markdown("---")
            st.markdown("#### 📋 Existing Active Profiles")
            party_rows = []
            for uid, udata in st.session_state.users_db.items():
                if udata["role"] == "party":
                    party_rows.append({
                        "Login ID": uid,
                        "Company Name": udata["company"],
                        "Gmail Address": udata.get("email", "Not Provided"),
                        "Contact Person": udata["name"],
                        "Password": "••••••••", 
                        "Address": udata.get("address", "")
                    })
            if party_rows:
                st.dataframe(pd.DataFrame(party_rows), use_container_width=True)
                
                del_party_id = st.selectbox("Select Profile to Remove:", [p["Login ID"] for p in party_rows])
                if st.button("❌ Remove Selected Party"):
                    del st.session_state.users_db[del_party_id]
                    save_data(USERS_FILE, st.session_state.users_db)
                    st.success(f"Profile `{del_party_id}` has been permanently removed.")
                    st.rerun()
            else:
                st.info("No client profiles registered yet.")
