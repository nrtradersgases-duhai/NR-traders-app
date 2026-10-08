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
        background: linear-gradient(135deg, #8B0000 0%, #B71C1C 100%);
        color: white;
        padding: 24px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .login-container {
        max-width: 550px;
        margin: 0 auto 30px auto;
        padding: 28px;
        background-color: #FFFFFF;
        border: 2px solid #B71C1C;
        border-radius: 14px;
        box-shadow: 0 6px 16px rgba(183, 28, 28, 0.12);
    }
    .gas-card {
        border-radius: 10px;
        padding: 12px;
        color: white;
        margin-bottom: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.15);
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
    .cloud-sync-banner {
        background-color: #FFEBEE;
        border: 1px solid #E57373;
        padding: 10px 15px;
        border-radius: 8px;
        color: #B71C1C;
        font-weight: bold;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
</style>
""", unsafe_allow_html=True)

# USER DATABASE (ONLY ADMIN - NO DUMMY PARTIES) ---
if "users_db" not in st.session_state: 
    st.session_state.users_db = { 
        "admin": { 
            "password": "admin", 
            "role": "admin", 
            "name": "Mr. Nitin Sharma (Owner)", 
            "company": "N R TRADERS" 
        }
    }

# INITIAL DATA (CLEAN LISTS - NO DUMMY ORDERS OR BILLS) ---
if "logged_in_user" not in st.session_state: 
    st.session_state.logged_in_user = None

if "orders" not in st.session_state: 
    st.session_state.orders = []

if "bills" not in st.session_state: 
    st.session_state.bills = []

if "cart_filled" not in st.session_state: 
    st.session_state.cart_filled = []

if "cart_empty" not in st.session_state: 
    st.session_state.cart_empty = []

# GAS SPECIFICATIONS ---
GAS_SPECS = { 
    "Oxygen (O2)": { 
        "bg_color": "#1A1A1A", 
        "border_color": "#FFFFFF", 
        "neck_color": "⬜ White Neck", 
        "body_color": "⬛ Black Body", 
        "categories": ["Standard (7 m³)"], 
        "desc": "Industrial Metal Cutting, Welding & Medical Breath Support" 
    }, 
    "Nitrogen (N2)": { 
        "bg_color": "#455A64", 
        "border_color": "#90A4AE", 
        "neck_color": "⬛ Black Neck", 
        "body_color": "🌫️ French Grey Body", 
        "categories": ["Standard (7 m³)"], 
        "desc": "Laser Cutting Inerting, Pressure Testing, Purging & Chemical Processing" 
    },
    "Carbon Dioxide (CO2)": { 
        "bg_color": "#212121", 
        "border_color": "#757575", 
        "neck_color": "⬛ Black Neck", 
        "body_color": "⬛ Black Body", 
        "categories": ["Personalised 20kg", "Standard 30kg", "Commercial 45kg"], 
        "desc": "MIG Welding Shielding, Beverage Carbonation & Fire Fighting" 
    }, 
    "Dissolved Acetylene (DA)": { 
        "bg_color": "#5D4037", 
        "border_color": "#8D6E63", 
        "neck_color": "🟫 Brownish Red Neck", 
        "body_color": "🟫 Brownish Red Body", 
        "categories": ["Standard DA Cylinder"], 
        "desc": "Oxy-Acetylene High-Temperature Heavy Metal Cutting & Brazing" 
    },
    "Argon (Ar)": { 
        "bg_color": "#0D47A1", 
        "border_color": "#42A5F5", 
        "neck_color": "🟦 Navy Blue Neck", 
        "body_color": "🟦 Navy Blue Body", 
        "categories": ["7 cubic metres", "10 cubic metres"], 
        "desc": "TIG Welding Shielding, Stainless Steel Fabrication & Precision Alloys" 
    }, 
    "Hydrogen (H2)": { 
        "bg_color": "#B71C1C", 
        "border_color": "#FF8A80", 
        "neck_color": "🟥 Scarlet Red Neck", 
        "body_color": "🟥 Scarlet Red Body", 
        "categories": ["Standard (7 m³)"], 
        "desc": "High-Precision Cutting, Heat Treatment & Special Laboratory Atmospheres" 
    } 
}

# SIDEBAR ---
if st.session_state.logged_in_user is not None:
    u_info = st.session_state.users_db[st.session_state.logged_in_user] 
    st.sidebar.success(f"Logged in as: {u_info['name']}") 
    st.sidebar.caption(f"Role: {u_info['role'].upper()} | Company: {u_info['company']}")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in_user = None
        st.rerun()
    st.sidebar.markdown("---")

st.sidebar.markdown("### 🏢 N R TRADERS Contact Info") 
st.sidebar.markdown("📞 **Call:** +91 9999734204") 
st.sidebar.markdown("📞 **Call:** +91 8130853589") 
st.sidebar.markdown("✉️ **Email:** nrtraders.gases@gmail.com") 
st.sidebar.markdown("📍 **Office & Godown:** Panchal Market, Duhai Industrial Area, Duhai, Ghaziabad, UP - 201206") 
st.sidebar.markdown("👤 **Owner:** Mr. Nitin Sharma")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛢️ Cylinder Catalog & Specs")
for gas_name, spec in GAS_SPECS.items():
    st.sidebar.markdown(f"""
    <div class="gas-card" style="background-color: {spec['bg_color']}; border: 1px solid {spec['border_color']};">
        <b style="font-size:14px;">🛢️ {gas_name}</b><br>
        <span style="font-size:12px;">• Neck: {spec['neck_color']}<br>
        • Body: {spec['body_color']}<br>
        • Sizes: {', '.join(spec['categories'])}</span>
    </div>
    """, unsafe_allow_html=True)

# MAIN DISPLAY ---
if st.session_state.logged_in_user is None:
    # PUBLIC VIEW: CENTERED RED HEADER & LOGIN
    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; font-size: 36px; letter-spacing: 1px;">🏭 N R TRADERS</h1>
        <p style="margin:8px 0 4px 0; font-size: 17px; font-weight: 500;">Deals in: All Type of Oxygen, CO2, Nitrogen, Argon, DA & H2 Gas Cylinders</p>
        <p style="margin:4px 0; font-size: 14px; opacity:0.95;">📍 Office & Godown: Panchal Market, Duhai Industrial Area, Duhai - 201206, Ghaziabad (U.P.)</p>
        <p style="margin:2px 0 0 0; font-size: 13px; opacity:0.9;"><b>GSTIN:</b> 09MHSPS5749H1Z3 | <b>MSME Reg:</b> UDYAM-UP-29-0162343</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="cloud-sync-banner">
        ☁️ <b>Google Drive & Google Sheets Connected:</b> <code>nrtraders.gases@gmail.com</code> | Real-time Auto-Backup Active
    </div>
    """, unsafe_allow_html=True)

    col_l1, col_center, col_l2 = st.columns([1, 2, 1])
    with col_center:
        st.markdown("<h3 style='text-align: center; color: #8B0000;'>🔐 User Login & Authentication</h3>", unsafe_allow_html=True)
        st.caption("<div style='text-align: center;'>Select role and enter credentials to access portal.</div>", unsafe_allow_html=True)
        
        with st.form("centered_login_form"):
            login_role = st.selectbox("Account Role:", ["Admin / Owner Login", "Party / Customer Login"])
            login_id = st.text_input("User ID / Party ID:").strip().lower()
            login_pass = st.text_input("Password:", type="password")
            submit_login = st.form_submit_button("🔑 Login to Portal", use_container_width=True)

            if submit_login:
                if login_id in st.session_state.users_db:
                    user_record = st.session_state.users_db[login_id]
                    expected_role = "admin" if login_role == "Admin / Owner Login" else "party"
                    
                    if user_record["role"] != expected_role:
                        st.error(f"❌ Role mismatch: This account belongs to {user_record['role'].upper()}!")
                    elif user_record["password"] == login_pass:
                        st.session_state.logged_in_user = login_id
                        st.success(f"Welcome, {user_record['name']}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid Password!")
                else:
                    st.error("❌ User ID not found!")

    st.markdown("---")
    st.info("🔒 **Confidentiality Notice:** Every party's orders, ledger, and tax invoices are strictly isolated and password-protected.")

else:
    # LOGGED IN PORTALS
    st.markdown("""
    <div class="main-header" style="padding: 16px;">
        <h2 style="margin:0;">🏭 N R TRADERS - Portal</h2>
        <p style="margin:3px 0 0 0; font-size: 13px; opacity:0.9;">GSTIN: 09MHSPS5749H1Z3 | Panchal Market, Duhai Industrial Area, Ghaziabad</p>
    </div>
    """, unsafe_allow_html=True)

    # 1. PARTY VIEW
    if st.session_state.users_db[st.session_state.logged_in_user]["role"] == "party":
        curr_user_id = st.session_state.logged_in_user 
        curr_user_info = st.session_state.users_db[curr_user_id]

        party_bills = [b for b in st.session_state.bills if b.get("party_id") == curr_user_id]
        unread_bills_count = sum(1 for b in party_bills if b.get("unread", False))
        bill_tab_label = f"📄 View Bills & Download Invoices (🔴 {unread_bills_count} New)" if unread_bills_count > 0 else "📄 View Bills & Download Invoices"

        tab1, tab2, tab3 = st.tabs(["🛒 Place Cylinder Order", bill_tab_label, "📞 Help & Support"])

        with tab1:
            st.subheader("📝 Order Gas Cylinders & Report Empty Cylinders")
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                st.text_input("🏢 Party / Customer Name:", value=curr_user_info["company"], disabled=True)
            with c_p2:
                party_address = st.text_input("📍 Delivery Address / Location:", value=curr_user_info.get("address", ""))
                
            st.markdown("---")
            col_filled, col_empty = st.columns(2)
            
            with col_filled:
                st.markdown("<div class='card-filled'><h3>🟢 FILLED CYLINDERS REQUIRED</h3></div>", unsafe_allow_html=True)
                fgas = st.selectbox("Select Gas Type (Filled):", list(GAS_SPECS.keys()), key="f_gas_sel")
                fcat = st.selectbox("Select Category / Size:", GAS_SPECS[fgas]["categories"], key="f_cat_sel")
                fqty = st.number_input("Enter Number of Cylinders:", min_value=1, max_value=500, value=1, step=1, key="f_qty_sel")
                
                if st.button("➕ Add Filled Cylinder Item"):
                    st.session_state.cart_filled.append({
                        "Gas Type": fgas,
                        "Category / Size": fcat,
                        "Quantity": fqty
                    })
                    st.success(f"Added {fqty} x {fgas} to List!")
                    
                if st.session_state.cart_filled:
                    st.markdown("**🛒 Current Filled Cylinders List:**")
                    st.dataframe(pd.DataFrame(st.session_state.cart_filled), use_container_width=True)
                    if st.button("🗑️ Clear Filled List"):
                        st.session_state.cart_filled = []
                        st.rerun()

            with col_empty:
                st.markdown("<div class='card-empty'><h3>🔴 EMPTY CYLINDERS AT SITE</h3></div>", unsafe_allow_html=True)
                egas = st.selectbox("Select Gas Type (Empty):", list(GAS_SPECS.keys()), key="e_gas_sel")
                ecat = st.selectbox("Select Category / Size (Empty):", GAS_SPECS[egas]["categories"], key="e_cat_sel")
                eqty = st.number_input("Enter Number of Empty Cylinders:", min_value=0, max_value=500, value=1, step=1, key="e_qty_sel")
                
                if st.button("➕ Add Empty Cylinder Item"):
                    st.session_state.cart_empty.append({
                        "Gas Type": egas,
                        "Category / Size": ecat,
                        "Quantity": eqty
                    })
                    st.success(f"Reported {eqty} x {egas} empty cylinders!")
                    
                if st.session_state.cart_empty:
                    st.markdown("**📦 Current Empty Cylinders List:**")
                    st.dataframe(pd.DataFrame(st.session_state.cart_empty), use_container_width=True)
                    if st.button("🗑️ Clear Empty List"):
                        st.session_state.cart_empty = []
                        st.rerun()

            st.markdown("---")
            if st.button("🚀 SUBMIT ORDER & SEND INSTANT ALERT TO N R TRADERS", type="primary", use_container_width=True):
                if not st.session_state.cart_filled and not st.session_state.cart_empty:
                    st.error("Please add at least one filled cylinder or empty cylinder item before submitting!")
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
                        "vehicle": "To be assigned"
                    }
                    st.session_state.orders.insert(0, new_order)
                    st.session_state.cart_filled = []
                    st.session_state.cart_empty = []
                    st.balloons()
                    st.success(f"✅ Order #{new_ord_id} Submitted Successfully!")

            st.markdown("---")
            st.subheader("📋 Order History")
            my_orders = [o for o in st.session_state.orders if o.get("party_id") == curr_user_id]
            if my_orders:
                for ord_item in my_orders:
                    st.markdown(f"#### 📦 Order #{ord_item['order_id']} ({ord_item['timestamp']})")
                    st.markdown(f"**Status:** `{ord_item['status']}` | **ETA:** `{ord_item['eta']}`")
                    b1, b2 = st.columns(2)
                    with b1:
                        if ord_item['filled_items']:
                            st.write("🟢 **Filled Cylinders:**")
                            st.dataframe(pd.DataFrame(ord_item['filled_items']), use_container_width=True)
                    with b2:
                        if ord_item['empty_items']:
                            st.write("🔴 **Empty Cylinders:**")
                            st.dataframe(pd.DataFrame(ord_item['empty_items']), use_container_width=True)
                    st.markdown("---")
            else:
                st.info("No orders placed yet.")

        with tab2:
            st.subheader("📄 GST Tax Invoices")
            if party_bills:
                for b_idx, bill in enumerate(party_bills):
                    if bill.get("unread", False):
                        st.session_state.bills[b_idx]["unread"] = False
                    st.markdown(f"""
                    <div class="bill-box">
                        <h3 style="margin:0; color:#8B0000;">🧾 Tax Invoice #{bill['bill_no']}</h3>
                        <p style="margin:3px 0;"><b>Date:</b> {bill['date']} | <b>Grand Total:</b> ₹{bill['amount']:,.2f} | <b>Vehicle:</b> {bill['vehicle']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No tax invoices issued yet.")

        with tab3:
            st.subheader("📞 Help & Support")
            st.markdown("""
            * **Call:** +91 9999734204 / +91 8130853589
            * **Email:** nrtraders.gases@gmail.com
            * **Godown Address:** Panchal Market, Duhai Industrial Area, Ghaziabad
            """)

    # 2. ADMIN VIEW
    elif st.session_state.users_db[st.session_state.logged_in_user]["role"] == "admin":
        st.subheader("⚙️ N R TRADERS Owner CRM & Management Dashboard")

        admin_tab1, admin_tab2, admin_tab3 = st.tabs([
            "📥 Live Orders Queue", 
            "📤 Upload Tax Invoices", 
            "🔐 Party Account & Password Management"
        ])

        with admin_tab1:
            st.markdown("### 📥 Live Party Orders Queue")
            if not st.session_state.orders:
                st.info("No live orders in the queue. Everything is clean.")
            else:
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
                        e1, e2, e3 = st.columns([2, 2, 2])
                        with e1:
                            selected_eta_opt = st.selectbox("Estimated Delivery Time:", ["30 Mins", "45 Mins", "1 Hour", "2 Hours", "Custom Time"], key=f"eta_{ord_item['order_id']}")
                        with e2:
                            final_eta = st.text_input("Confirm ETA:", value=selected_eta_opt, key=f"feta_{ord_item['order_id']}")
                        with e3:
                            assigned_veh = st.text_input("Vehicle:", value="BOLERO UP14LT6202", key=f"veh_{ord_item['order_id']}")
                            
                        if st.button(f"✅ Confirm Order #{ord_item['order_id']}", key=f"btn_{ord_item['order_id']}"):
                            st.session_state.orders[idx]["status"] = "Accepted"
                            st.session_state.orders[idx]["eta"] = final_eta
                            st.session_state.orders[idx]["vehicle"] = assigned_veh
                            st.success(f"Order #{ord_item['order_id']} Confirmed!")
                            st.rerun()
                    else:
                        st.markdown(f"<div class='status-confirmed'>✅ Accepted | ETA: {ord_item['eta']} | Vehicle: {ord_item['vehicle']}</div>", unsafe_allow_html=True)
                    st.markdown("---")

        with admin_tab2:
            st.markdown("### 📤 Create / Upload Tax Invoice")
            party_users = [uid for uid, uinfo in st.session_state.users_db.items() if uinfo["role"] == "party"]
            
            if not party_users:
                st.warning("No Party accounts found. Create a Party Account in tab 3 first.")
            else:
                with st.form("admin_invoice_form", clear_on_submit=True):
                    u_party = st.selectbox("Select Party:", party_users)
                    u_inv_no = st.text_input("Invoice Number:", value=f"2026-27/{len(st.session_state.bills) + 1}")
                    u_amt = st.number_input("Total Amount (₹):", min_value=0.0, value=0.0, step=100.0)
                    u_vehicle = st.text_input("Vehicle No:", value="BOLERO UP14LT6202")
                    
                    if st.form_submit_button("📤 Issue Invoice to Party"):
                        p_name = st.session_state.users_db[u_party]["company"]
                        new_bill = {
                            "bill_no": u_inv_no,
                            "party_id": u_party,
                            "party_name": p_name,
                            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                            "amount": u_amt,
                            "unread": True,
                            "vehicle": u_vehicle
                        }
                        st.session_state.bills.insert(0, new_bill)
                        st.success(f"Invoice #{u_inv_no} issued to {p_name}!")
                        st.rerun()

        with admin_tab3:
            st.markdown("### 🔐 Party Management (Create, Edit & Delete)")
            
            # 1. CREATE NEW PARTY
            st.markdown("#### ➕ Add New Party")
            with st.form("add_party_form", clear_on_submit=True):
                p_uid = st.text_input("Party User ID (Username):").strip().lower()
                p_comp = st.text_input("Company / Firm Name:")
                p_rep = st.text_input("Representative / Contact Person Name:")
                p_pwd = st.text_input("Set Password:")
                p_addr = st.text_input("Delivery / Plant Address:")
                
                if st.form_submit_button("➕ Register Party"):
                    if not p_uid or not p_comp or not p_pwd:
                        st.error("User ID, Company Name और Password भरना अनिवार्य है!")
                    elif p_uid in st.session_state.users_db:
                        st.error("यह User ID पहले से मौजूद है! कृपया दूसरी चुनें।")
                    else:
                        st.session_state.users_db[p_uid] = {
                            "password": p_pwd,
                            "role": "party",
                            "name": p_rep if p_rep else p_comp,
                            "company": p_comp,
                            "address": p_addr
                        }
                        st.success(f"पार्टी '{p_comp}' सफलतापूर्वक जोड़ दी गई!")
                        st.rerun()

            st.markdown("---")

            # 2. EDIT EXISTING PARTY
            st.markdown("#### ✏️ Edit Existing Party Details")
            parties_list = [uid for uid, uinfo in st.session_state.users_db.items() if uinfo["role"] == "party"]
            if parties_list:
                selected_edit_party = st.selectbox("Select Party to Edit:", parties_list)
                curr_data = st.session_state.users_db[selected_edit_party]
                
                with st.form("edit_party_form"):
                    edit_comp = st.text_input("Company Name:", value=curr_data.get("company", ""))
                    edit_name = st.text_input("Contact Person:", value=curr_data.get("name", ""))
                    edit_pwd = st.text_input("Password:", value=curr_data.get("password", ""))
                    edit_addr = st.text_input("Address:", value=curr_data.get("address", ""))
                    
                    if st.form_submit_button("💾 Save Changes"):
                        st.session_state.users_db[selected_edit_party]["company"] = edit_comp
                        st.session_state.users_db[selected_edit_party]["name"] = edit_name
                        st.session_state.users_db[selected_edit_party]["password"] = edit_pwd
                        st.session_state.users_db[selected_edit_party]["address"] = edit_addr
                        st.success(f"Details for '{selected_edit_party}' updated!")
                        st.rerun()
            else:
                st.info("No party accounts available to edit.")

            st.markdown("---")

            # 3. DELETE PARTY
            st.markdown("#### 🗑️ Delete Party Account")
            if parties_list:
                del_party_id = st.selectbox("Select Party to Delete:", ["-- Select Party --"] + parties_list)
                if st.button("❌ Permanently Delete Party", type="primary"):
                    if del_party_id != "-- Select Party --":
                        del st.session_state.users_db[del_party_id]
                        st.success(f"Party '{del_party_id}' deleted successfully!")
                        st.rerun()
            else:
                st.info("No party accounts available to delete.")

            st.markdown("---")

            # 4. ACTIVE USERS TABLE
            st.markdown("#### 📋 All Active Accounts")
            acc_list = []
            for uid, udata in st.session_state.users_db.items():
                acc_list.append({
                    "User ID": uid,
                    "Role": udata["role"].upper(),
                    "Company": udata["company"],
                    "Contact Person": udata.get("name", ""),
                    "Password": udata["password"]
                })
            st.dataframe(pd.DataFrame(acc_list), use_container_width=True)
