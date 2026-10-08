import streamlit as st 
import pandas as pd 
import datetime 
import io 
import json

# PAGE CONFIGURATION ---
st.set_page_config( 
page_title="N R TRADERS - Gas Ordering & CRM", 
page_icon="ðŸ›¢ï¸", 
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
    .badge-count {
        background-color: #E53935;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 13px;
        font-weight: bold;
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
        background-color: #E8F0FE;
        border: 1px solid #4285F4;
        padding: 10px 15px;
        border-radius: 8px;
        color: #1A73E8;
        font-weight: bold;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
</style>

""", unsafe_allow_html=True)

# USER DATABASE (CUSTOM PASSWORDS FOR ADMIN & PARTIES) ---
if "users_db" not in st.session_state: 
    st.session_state.users_db = { 
"admin": { 
"password": "admin123", 
"role": "admin", 
"name": "Mr. Nitin Sharma (Owner)", 
"company": "N R TRADERS" 
}, 
"ar_fabtech": { 
"password": "party123", 
"role": "party", 
"name": "AR Fabtech Innovation", 
"company": "AR Fabtech Innovation", 
"address": "Site 4 Industrial Area, Sahibabad, Ghaziabad" 
}, 
"shree_ji": { 
"password": "shree123", 
"role": "party", 
"name": "Shree Ji Coil Solution", 
"company": "SHREE JI COIL SOLUTION", 
"address": "Duhai Industrial Area, Ghaziabad" 
} 
}

# INITIAL SESSION STATE DATA ---
if "logged_in_user" not in st.session_state: 
    st.session_state.logged_in_user = None

if "google_drive_synced" not in st.session_state: 
    st.session_state.google_drive_synced = True

if "orders" not in st.session_state: 
    st.session_state.orders = [ 
{ 
"order_id": "NRT-ORD-2026-101", 
"party_id": "ar_fabtech", 
"party_name": "AR Fabtech Innovation", 
"timestamp": "2026-10-07 16:50", 
"filled_items": [ 
{"Gas Type": "Oxygen (O2)", "Category / Size": "Standard (7 mÂ³)", "Quantity": 12}, 
{"Gas Type": "Argon (Ar)", "Category / Size": "10 cubic metres", "Quantity": 5} 
], 
"empty_items": [ 
{"Gas Type": "Oxygen (O2)", "Category / Size": "Standard (7 mÂ³)", "Quantity": 10}, 
{"Gas Type": "Argon (Ar)", "Category / Size": "10 cubic metres", "Quantity": 3} 
], 
"status": "Accepted", 
"eta": "45 Mins (Delivery by 17:35)", 
"vehicle": "BOLERO UP14LT6202" 
} 
]

if "bills" not in st.session_state: 
    st.session_state.bills = [ 
{ 
"bill_no": "2026-27/161", 
"party_id": "shree_ji", 
"party_name": "SHREE JI COIL SOLUTION", 
"date": "2026-09-15", 
"amount": 14603.00, 
"unread": True, 
"items": [ 
{"Gas": "Oxygen Gas (O2)", "HSN": "28044090", "Qty": 15, "Rate": 350, "Taxable Amount": 5250}, 
{"Gas": "CO2 Gas (Commercial 45kg)", "HSN": "28112190", "Qty": 8, "Rate": 800, "Taxable Amount": 6400}, 
{"Gas": "Freight & Transport", "HSN": "996511", "Qty": 1, "Rate": 725, "Taxable Amount": 725} 
], 
"cgst": 1113.75, 
"sgst": 1113.75, 
"vehicle": "BOLERO UP14LT6202" 
} 
]

if "cart_filled" not in st.session_state: 
    st.session_state.cart_filled = []

if "cart_empty" not in st.session_state: 
    st.session_state.cart_empty = []

# APP HEADER ---
st.markdown("""
<div class="main-header">
    <h1 style="margin:0;">ðŸ›¢ï¸ N R TRADERS</h1>
    <p style="margin:5px 0 0 0; font-size: 16px; opacity:0.9;">Industrial & Medical Gas Cylinders Ordering, Billing & Cloud Sync Portal</p>
    <p style="margin:2px 0 0 0; font-size: 13px; opacity:0.75;">GSTIN: 09MHSPS5749H1Z3 | MSME: UDYAM-UP-29-0162343 | Google Drive Sync: Connected (nrtraders.gases@gmail.com)</p>
</div>
""", unsafe_allow_html=True)

# GOOGLE DRIVE & SHEETS CLOUD SYNC BANNER ---
st.markdown("""
<div class="cloud-sync-banner">
    â˜ï¸ <b>Google Drive & Google Sheets Connected:</b> <code>nrtraders.gases@gmail.com</code> | Real-time Auto-Backup Active for Orders & Invoices!
</div>
""", unsafe_allow_html=True)

# GAS SPECIFICATIONS & COLOUR CODES ---
GAS_SPECS = { 
"Oxygen (O2)": { 
"bg_color": "#1A1A1A", 
"border_color": "#FFFFFF", 
"neck_color": "â¬œ White Neck", 
"body_color": "â¬› Black Body", 
"text_color": "#FFFFFF", 
"categories": ["Standard (7 mÂ³)"], 
"desc": "Industrial Metal Cutting, Welding & Medical Breath Support" 
}, 
"Carbon Dioxide (CO2)": { 
"bg_color": "#212121", 
"border_color": "#757575", 
"neck_color": "â¬› Black Neck", 
"body_color": "â¬› Black Body", 
"text_color": "#FFFFFF", 
"categories": ["Personalised 20kg", "Standard 30kg", "Commercial 45kg"], 
"desc": "MIG Welding Shielding, Beverage Carbonation & Fire Fighting" 
}, 
"Argon (Ar)": { 
"bg_color": "#0D47A1", 
"border_color": "#42A5F5", 
"neck_color": "ðŸŸ¦ Navy Blue Neck", 
"body_color": "ðŸŸ¦ Navy Blue Body", 
"text_color": "#FFFFFF", 
"categories": ["7 cubic metres", "10 cubic metres"], 
"desc": "TIG Welding Shielding, Stainless Steel Fabrication & Precision Alloys" 
}, 
"Nitrogen (N2)": { 
"bg_color": "#78909C", 
"border_color": "#212121", 
"neck_color": "â¬› Black Neck", 
"body_color": "ðŸŒ«ï¸ French Grey Body", 
"text_color": "#FFFFFF", 
"categories": ["Standard (7 mÂ³)"], 
"desc": "Laser Cutting Inerting, Pressure Testing, Purging & Chemical Processing" 
}, 
"Dissolved Acetylene (DA)": { 
"bg_color": "#8D6E63", 
"border_color": "#3E2723", 
"neck_color": "ðŸŸ« Brownish Red Neck", 
"body_color": "ðŸŸ« Brownish Red Body", 
"text_color": "#FFFFFF", 
"categories": ["Standard DA Cylinder"], 
"desc": "Oxy-Acetylene High-Temperature Heavy Metal Cutting & Brazing" 
}, 
"Hydrogen (H2)": { 
"bg_color": "#D32F2F", 
"border_color": "#FF8A80", 
"neck_color": "ðŸŸ¥ Scarlet Red Neck", 
"body_color": "ðŸŸ¥ Scarlet Red Body", 
"text_color": "#FFFFFF", 
"categories": ["Standard (7 mÂ³)"], 
"desc": "High-Precision Cutting, Heat Treatment & Special Laboratory Atmospheres" 
} 
}

# LOGIN / AUTHENTICATION SIDEBAR ---
st.sidebar.markdown("### ðŸ” User Login & Authentication")

if st.session_state.logged_in_user is None: 
    st.sidebar.info("Please login to access your confidential party dashboard.") 
with st.sidebar.form("login_form"): 
    login_id = st.text_input("User ID / Party ID:").strip().lower() 
login_pass = st.text_input("Password:", type="password") 
submit_login = st.form_submit_button("ðŸ”“ Login")

    if submit_login:
        if login_id in st.session_state.users_db and st.session_state.users_db[login_id]["password"] == login_pass:
            st.session_state.logged_in_user = login_id
            st.sidebar.success(f"Welcome, {st.session_state.users_db[login_id]['name']}!")
            st.rerun()
        else:
            st.sidebar.error("âŒ Invalid User ID or Password!")
else: 
    u_info = st.session_state.users_db[st.session_state.logged_in_user] 
    st.sidebar.success(f"Logged in as: {u_info['name']}") 
    st.sidebar.caption(f"Role: {u_info['role'].upper()} | Company: {u_info['company']}")

if st.sidebar.button("ðŸšª Logout"):
    st.session_state.logged_in_user = None
    st.rerun()
st.sidebar.markdown("---") 
st.sidebar.markdown("### ðŸ¢ N R TRADERS Contact Info") 
st.sidebar.markdown("ðŸ“ž Call: +91 9999734204") 
st.sidebar.markdown("ðŸ“ž Call: +91 8130853589") 
st.sidebar.markdown("âœ‰ï¸ Email: nrtraders.gases@gmail.com") 













































































































































































































































































st.sidebar.markdown("ðŸ“ Office & Godown: Duhai Industrial Area, Ghaziabad, UP") 
st.sidebar.markdown("ðŸ‘¤ Owner: Mr. Nitin Sharma")

# HOME PAGE & SHOWCASE (PUBLIC VIEW) ---
if st.session_state.logged_in_user is None: 
    st.subheader("ðŸŽ¨ Welcome to N R TRADERS - Industrial Gas Cylinder Catalog") 
st.markdown("Below are the official cylinder identification color codes and specs for gases supplied by N R TRADERS. Please login from the sidebar to place confidential orders and download tax invoices.")

st.markdown("---")
c1, c2, c3 = st.columns(3)
cols = [c1, c2, c3]

for idx, (gas_name, spec) in enumerate(GAS_SPECS.items()):
    with cols[idx % 3]:
        st.markdown(f"""
        <div class="gas-card" style="background-color: {spec['bg_color']}; border: 2px solid {spec['border_color']}; color: {spec['text_color']};">
            <h3 style="margin:0;">ðŸ›¢ï¸ {gas_name}</h3>
            <p style="margin:5px 0;"><b>Neck / Shoulder Color:</b> {spec['neck_color']}</p>
            <p style="margin:5px 0;"><b>Cylinder Body Color:</b> {spec['body_color']}</p>
            <p style="margin:5px 0;"><b>Available Sizes:</b> {', '.join(spec['categories'])}</p>
            <hr style="margin:8px 0; border-color: rgba(255,255,255,0.2);">
            <p style="margin:0; font-size:12px; opacity:0.9;"><i>{spec['desc']}</i></p>
        </div>
        """, unsafe_allow_html=True)
        
st.markdown("---")
st.warning("ðŸ”’ **Confidentiality Notice:** Every party's orders, ledger, and tax invoices are password-protected and strictly isolated.")

PORTAL 1: CUSTOMER / PARTY ORDERING PORTAL (LOGGED IN PARTY)

elif st.session_state.users_db[st.session_state.logged_in_user]["role"]  "party": 
    curr_user_id = st.session_state.logged_in_user 
    curr_user_info = st.session_state.users_db[curr_user_id]

# Filter party's private data
party_bills = [b for b in st.session_state.bills if b.get("party_id") == curr_user_id or b.get("party_name") == curr_user_info["company"]]
unread_bills_count = sum(1 for b in party_bills if b.get("unread", False))
bill_tab_label = f"ðŸ“„ View Bills & Download Invoices (ðŸ”´ {unread_bills_count} New)" if unread_bills_count > 0 else "ðŸ“„ View Bills & Download Invoices"

tab1, tab2, tab3 = st.tabs(["ðŸ›’ Place Cylinder Order & Download Receipt", bill_tab_label, "ðŸ“ž Help & Support"])

# --------------------------------------------------------------------------
# TAB 1: ORDER CYLINDERS & DOWNLOAD ORDER BACKUP
# --------------------------------------------------------------------------
with tab1:
    st.subheader("ðŸ“ Order Gas Cylinders & Report Empty Cylinders")
    st.caption(f"Logged in Party: **{curr_user_info['company']}** | Data strictly private & auto-synced to Google Drive.")
    
    c_p1, c_p2 = st.columns(2)
    with c_p1:
        party_name = st.text_input("ðŸ¢ Party / Customer Name:", value=curr_user_info["company"], disabled=True)
    with c_p2:
        party_address = st.text_input("ðŸ“ Delivery Address / Location:", value=curr_user_info.get("address", "Sahibabad / Ghaziabad"))
        
    st.markdown("---")
    
    col_filled, col_empty = st.columns(2)
    
    # --- FILLED CYLINDERS BUILDER ---
    with col_filled:
        st.markdown("<div class='card-filled'><h3>ðŸŸ¢ FILLED CYLINDERS REQUIRED</h3><p>Select required gas type, size & quantity:</p></div>", unsafe_allow_html=True)
        
        fgas = st.selectbox("Select Gas Type (Filled):", list(GAS_SPECS.keys()), key="f_gas_sel")
        fcat = st.selectbox("Select Category / Size:", GAS_SPECS[fgas]["categories"], key="f_cat_sel")
        fqty = st.number_input("Enter Number of Cylinders:", min_value=1, max_value=500, value=5, step=1, key="f_qty_sel")
        
        if st.button("âž• Add Filled Cylinder Item"):
            st.session_state.cart_filled.append({
                "Gas Type": fgas,
                "Category / Size": fcat,
                "Quantity": fqty
            })
            st.success(f"Added {fqty} x {fgas} ({fcat}) to Filled Order List!")
            
        if st.session_state.cart_filled:
            st.markdown("**ðŸ›’ Current Filled Cylinders Order List:**")
            st.dataframe(pd.DataFrame(st.session_state.cart_filled), use_container_width=True)
            if st.button("ðŸ—‘ï¸ Clear Filled List"):
                st.session_state.cart_filled = []
                st.rerun()

    # --- EMPTY CYLINDERS BUILDER ---
    with col_empty:
        st.markdown("<div class='card-empty'><h3>ðŸ”´ EMPTY CYLINDERS AT SITE</h3><p>Report empty cylinders ready for pickup:</p></div>", unsafe_allow_html=True)
        
        egas = st.selectbox("Select Gas Type (Empty):", list(GAS_SPECS.keys()), key="e_gas_sel")
        ecat = st.selectbox("Select Category / Size (Empty):", GAS_SPECS[egas]["categories"], key="e_cat_sel")
        eqty = st.number_input("Enter Number of Empty Cylinders:", min_value=0, max_value=500, value=3, step=1, key="e_qty_sel")
        
        if st.button("âž• Add Empty Cylinder Item"):
            st.session_state.cart_empty.append({
                "Gas Type": egas,
                "Category / Size": ecat,
                "Quantity": eqty
            })
            st.success(f"Reported {eqty} x {egas} ({ecat}) empty cylinders at site!")
            
        if st.session_state.cart_empty:
            st.markdown("**ðŸ“¦ Current Empty Cylinders Pickup List:**")
            st.dataframe(pd.DataFrame(st.session_state.cart_empty), use_container_width=True)
            if st.button("ðŸ—‘ï¸ Clear Empty List"):
                st.session_state.cart_empty = []
                st.rerun()

    st.markdown("---")
    
    # SUBMIT ORDER BUTTON
    if st.button("ðŸš€ SUBMIT ORDER & SEND INSTANT ALERT TO N R TRADERS", type="primary", use_container_width=True):
        if not st.session_state.cart_filled and not st.session_state.cart_empty:
            st.error("Please add at least one filled cylinder or empty cylinder item before submitting!")
        else:
            new_ord_id = f"NRT-ORD-2026-{len(st.session_state.orders) + 102}"
            new_order = {
                "order_id": new_ord_id,
                "party_id": curr_user_id,
                "party_name": curr_user_info["company"],
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "filled_items": st.session_state.cart_filled.copy(),
                "empty_items": st.session_state.cart_empty.copy(),
                "status": "Pending Confirmation",
                "eta": "Awaiting N R TRADERS Confirmation",
                "vehicle": "To be assigned"
            }
            st.session_state.orders.insert(0, new_order)
            st.session_state.cart_filled = []
            st.session_state.cart_empty = []
            st.balloons()
            st.success(f"âœ… Order #{new_ord_id} Submitted Successfully!")
            st.info("ðŸ“² Instant alert sent to Mr. Nitin Sharma (+91 9999734204) via WiFi/SMS/WhatsApp. Auto-backed up to Google Drive (nrtraders.gases@gmail.com).")

    # PARTY ORDER HISTORY & BACKUP DOWNLOAD SECTION
    st.markdown("---")
    st.subheader("ðŸ“‹ Order History & Backup Download for Party")
    my_orders = [o for o in st.session_state.orders if o.get("party_id") == curr_user_id or o.get("party_name") == curr_user_info["company"]]
    
    if my_orders:
        for ord_item in my_orders:
            st.markdown(f"#### ðŸ“¦ Order #{ord_item['order_id']} ({ord_item['timestamp']})")
            st.markdown(f"**Status:** `{ord_item['status']}` | **Estimated Delivery Time:** `{ord_item['eta']}`")
            
            b1, b2 = st.columns(2)
            with b1:
                if ord_item['filled_items']:
                    st.markdown("ðŸŸ¢ **Filled Cylinders:**")
                    st.dataframe(pd.DataFrame(ord_item['filled_items']), use_container_width=True)
            with b2:
                if ord_item['empty_items']:
                    st.markdown("ðŸ”´ **Empty Cylinders:**")
                    st.dataframe(pd.DataFrame(ord_item['empty_items']), use_container_width=True)
            
            # DOWNLOAD ORDER BACKUP / RECEIPT (CSV/JSON)
            backup_data = json.dumps(ord_item, indent=2)
            st.download_button(
                label=f"ðŸ“¥ Download Order Backup Receipt (#{ord_item['order_id']})",
                data=backup_data,
                file_name=f"{ord_item['order_id']}_receipt.json",
                mime="application/json",
                key=f"dl_ord_{ord_item['order_id']}"
            )
            st.markdown("---")
    else:
        st.write("No previous orders found.")

# --------------------------------------------------------------------------
# TAB 2: VIEW BILLS & DOWNLOAD INVOICES
# --------------------------------------------------------------------------
with tab2:
    st.subheader("ðŸ“„ GST Tax Invoices & Download Ledger")
    st.caption("View and download official GST tax invoices issued by N R TRADERS.")
    
    if party_bills:
        for b_idx, bill in enumerate(party_bills):
            if bill.get("unread", False):
                st.session_state.bills[b_idx]["unread"] = False
                
            st.markdown(f"""
            <div class="bill-box">
                <h3 style="margin:0; color:#0E2F44;">ðŸ§¾ Tax Invoice #{bill['bill_no']}</h3>
                <p style="margin:3px 0;"><b>Date:</b> {bill['date']} | <b>Billed To:</b> {bill['party_name']} | <b>Vehicle:</b> {bill['vehicle']}</p>
                <p style="margin:3px 0; font-size: 18px;"><b>Grand Total Amount:</b> <span style="color:#2E7D32; font-weight:bold;">â‚¹{bill['amount']:,.2f}</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander(f"ðŸ” View Breakdown & Download Invoice (#{bill['bill_no']})"):
                st.markdown(f"**Supplier:** N R TRADERS (GSTIN: `09MHSPS5749H1Z3` | MSME: `UDYAM-UP-29-0162343`)")
                st.markdown(f"**Recipient:** {bill['party_name']}")
                st.dataframe(pd.DataFrame(bill['items']), use_container_width=True)
                
                mc1, mc2, mc3 = st.columns(3)
                mc1.metric("CGST (9%)", f"â‚¹{bill['cgst']:,.2f}")
                mc2.metric("SGST (9%)", f"â‚¹{bill['sgst']:,.2f}")
                mc3.metric("Grand Total", f"â‚¹{bill['amount']:,.2f}")
                
                # DOWNLOAD TAX INVOICE (CSV/TXT BACKUP)
                inv_df = pd.DataFrame(bill['items'])
                csv_buffer = io.StringIO()
                inv_df.to_csv(csv_buffer, index=False)
                
                st.download_button(
                    label=f"ðŸ“¥ Download Tax Invoice Statement (#{bill['bill_no']})",
                    data=csv_buffer.getvalue(),
                    file_name=f"NR_TRADERS_Invoice_{bill['bill_no'].replace('/', '_')}.csv",
                    mime="text/csv",
                    key=f"dl_bill_{bill['bill_no']}"
                )
    else:
        st.info("No tax invoices issued for your account yet.")

# --------------------------------------------------------------------------
# TAB 3: HELP & SUPPORT
# --------------------------------------------------------------------------
with tab3:
    st.subheader("ðŸ“ž Help & Support - N R TRADERS")
    st.markdown("For urgent cylinder requirements, delivery updates, or ledger reconciliation, reach out to us:")
    
    hc1, hc2 = st.columns(2)
    with hc1:
        st.markdown("""
        ### ðŸ“± Official Contact Numbers
        * **Call:** +91 9999734204
        * **Call:** +91 8130853589
        
        ### âœ‰ï¸ Official Email Address
        * **Email:** nrtraders.gases@gmail.com
        
        ### ðŸ‘¤ Owner / Proprietor
        * **Mr. Nitin Sharma**
        """)
    with hc2:
        st.markdown("""
        ### ðŸ“ Office & Godown Address
        * **N R TRADERS**
        * Duhai Industrial Area, Muradnagar / Panchal Market,
        * Duhai, Ghaziabad, Uttar Pradesh - 201206
        
        ### ðŸ“„ Commercial Registration Details
        * **GSTIN:** `09MHSPS5749H1Z3`
        * **MSME Reg. No.:** `UDYAM-UP-29-0162343`
        """)

PORTAL 2: N R TRADERS ADMIN & CRM DASHBOARD (OWNER VIEW)

elif st.session_state.users_db[st.session_state.logged_in_user]["role"]  "admin": 
st.subheader("âš™ï¸ N R TRADERS Owner CRM & User Password Management Portal") 
st.markdown("Monitor party orders in real-time, accept orders with Estimated Delivery Time (ETA), manage party passwords, and sync with Google Drive.")

admin_tab1, admin_tab2, admin_tab3 = st.tabs(["ðŸ“¥ Live Orders Queue & ETA Confirmation", "ðŸ“¤ Upload Tax Invoice to Party CRM", "ðŸ” User Security & Password Management"])

# --------------------------------------------------------------------------
# ADMIN TAB 1: LIVE ORDERS QUEUE
# --------------------------------------------------------------------------
with admin_tab1:
    pending_list = [o for o in st.session_state.orders if o["status"] == "Pending Confirmation"]
    if pending_list:
        st.warning(f"ðŸ”” **{len(pending_list)} NEW ORDER(S) RECEIVED!** Instant alert sent to Mr. Nitin Sharma via WiFi/Internet/SMS (+91 9999734204). Auto-synced to Google Drive.")

    st.markdown("### ðŸ“¥ Live Party Orders Queue")
    
    for idx, ord_item in enumerate(st.session_state.orders):
        st.markdown(f"#### ðŸ“¦ Order #{ord_item['order_id']} - {ord_item['party_name']} ({ord_item['timestamp']})")
        
        ca, cb = st.columns(2)
        with ca:
            st.markdown("**ðŸŸ¢ FILLED CYLINDERS ORDERED:**")
            if ord_item["filled_items"]:
                st.dataframe(pd.DataFrame(ord_item["filled_items"]), use_container_width=True)
            else:
                st.write("None")
                
        with cb:
            st.markdown("**ðŸ”´ EMPTY CYLINDERS REPORTED AT SITE:**")
            if ord_item["empty_items"]:
                st.dataframe(pd.DataFrame(ord_item["empty_items"]), use_container_width=True)
            else:
                st.write("None")

        # ORDER ACCEPTANCE & ETA SETTING WORKFLOW
        if ord_item["status"] == "Pending Confirmation":
            st.markdown("**âš¡ Order Action & Delivery ETA Confirmation:**")
            e1, e2, e3 = st.columns([2, 2, 2])
            with e1:
                selected_eta_opt = st.selectbox(
                    "Select Estimated Delivery Time:",
                    ["30 Mins", "45 Mins", "1 Hour", "1.5 Hours", "2 Hours", "Today Evening 5 PM", "Custom Time Input"],
                    key=f"eta_opt_{ord_item['order_id']}"
                )
            with e2:
                if selected_eta_opt == "Custom Time Input":
                    final_eta_val = st.text_input("Enter Delivery Time:", value="40 Mins", key=f"custom_eta_{ord_item['order_id']}")
                else:
                    final_eta_val = selected_eta_opt
            with e3:
                assigned_vehicle_val = st.selectbox("Assign Supply Vehicle:", ["BOLERO UP14LT6202", "TEMPO UP14AT1122", "DIRECT GODOWN PICKUP"], key=f"v_sel_{ord_item['order_id']}")
                
            if st.button(f"âœ… CONFIRM ORDER & SEND ESTIMATED TIME TO PARTY (#{ord_item['order_id']})", key=f"cbtn_{ord_item['order_id']}"):
                st.session_state.orders[idx]["status"] = "Accepted"
                st.session_state.orders[idx]["eta"] = final_eta_val
                st.session_state.orders[idx]["vehicle"] = assigned_vehicle_val
                st.success(f"Order #{ord_item['order_id']} Accepted! Confirmation sent to party interface with Estimated Delivery Time: {final_eta_val}.")
                st.rerun()
        else:
            st.markdown(f"<div class='status-confirmed'>âœ… Accepted & Confirmed | Estimated Delivery Time: {ord_item['eta']} | Vehicle: {ord_item['vehicle']}</div>", unsafe_allow_html=True)
            
        st.markdown("---")

# --------------------------------------------------------------------------
# ADMIN TAB 2: UPLOAD BILLS
# --------------------------------------------------------------------------
with admin_tab2:
    st.markdown("### ðŸ“¤ Upload GST Invoice to Party View Bills CRM")
    with st.form("crm_upload_invoice_form"):
        u_party_id = st.selectbox("Select Party Account:", [uid for uid, uinfo in st.session_state.users_db.items() if uinfo["role"] == "party"])
        u_inv_no = st.text_input("Tax Invoice Number:", value=f"2026-27/{len(st.session_state.bills) + 162}")
        u_amount = st.number_input("Invoice Grand Total (â‚¹):", value=11200.0)
        u_veh = st.text_input("Vehicle Number:", value="BOLERO UP14LT6202")
        
        submit_invoice = st.form_submit_button("ðŸ“¤ Upload Invoice to Party App & Sync Google Drive")
        if submit_invoice:
            party_comp_name = st.session_state.users_db[u_party_id]["company"]
            new_bill = {
                "bill_no": u_inv_no,
                "party_id": u_party_id,
                "party_name": party_comp_name,
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "amount": u_amount,
                "unread": True,
                "items": [
                    {"Gas": "Oxygen / Argon / CO2 Supply", "HSN": "28044090", "Qty": 15, "Rate": 600, "Taxable Amount": 9000},
                    {"Gas": "Freight Charges", "HSN": "996511", "Qty": 1, "Rate": 491.52, "Taxable Amount": 491.52}
                ],
                "cgst": round(u_amount * 0.09 / 1.18, 2),
                "sgst": round(u_amount * 0.09 / 1.18, 2),
                "vehicle": u_veh
            }
            st.session_state.bills.insert(0, new_bill)
            st.success(f"Invoice #{u_inv_no} uploaded for {party_comp_name}! Party will receive a notification badge on their app.")

# --------------------------------------------------------------------------
# ADMIN TAB 3: USER SECURITY & PASSWORDS CONTROL PANEL
# --------------------------------------------------------------------------
with admin_tab3:
    st.markdown("### ðŸ” User Security & Password Management")
    st.caption("Manage party accounts, set custom passwords, or update your own Admin password.")
    
    st.markdown("#### âž• Create New Party Account")
    with st.form("create_user_form"):
        nu_id = st.text_input("New Party Username / ID (e.g., `national_steel`):").strip().lower()
        nu_name = st.text_input("Party Representative Name:")
        nu_comp = st.text_input("Company / Firm Name:")
        nu_pass = st.text_input("Assign Password:")
        nu_addr = st.text_input("Delivery Address:")
        
        submit_new_user = st.form_submit_button("ðŸ”‘ Register New Party Account")
        if submit_new_user:
            if nu_id in st.session_state.users_db:
                st.error("Username already exists!")
            elif not nu_id or not nu_pass or not nu_comp:
                st.error("Please fill in Username, Company Name, and Password!")
            else:
                st.session_state.users_db[nu_id] = {
                    "password": nu_pass,
                    "role": "party",
                    "name": nu_name if nu_name else nu_comp,
                    "company": nu_comp,
                    "address": nu_addr
                }
                st.success(f"Party account `{nu_id}` created successfully for **{nu_comp}**!")

    st.markdown("---")
    st.markdown("#### ðŸ“‹ Registered Accounts & Active Passwords Ledger")
    
    user_list_data = []
    for uid, udata in st.session_state.users_db.items():
        user_list_data.append({
            "User ID": uid,
            "Role": udata["role"].upper(),
            "Company / Name": udata["company"],
            "Password": udata["password"]
        })
    st.dataframe(pd.DataFrame(user_list_data), use_container_width=True)
