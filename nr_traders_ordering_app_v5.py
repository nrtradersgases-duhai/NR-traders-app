import streamlit as st
import pandas as pd
import datetime
import json
import os
import base64

# --- CONFIGURATION ---
st.set_page_config(page_title="N.R. TRADERS - CRM", page_icon="🏭", layout="wide")

# --- DATABASE FILES (Local Fallback for Testing) ---
# Jab aap Google Cloud Service Account bana lenge, toh inko Gspread (Google Sheets) se replace kar sakte hain.
USERS_FILE = "nrt_users.json"
ORDERS_FILE = "nrt_orders.json"
BILLS_FILE = "nrt_bills.json"

DEFAULT_USERS = {
    "admin": {
        "password": "admin",
        "role": "admin",
        "name": "Nitin Sharma",
        "company": "N.R. TRADERS",
        "gst": "09MHSPS5749H1Z3",
        "address": "Panchal Market, Duhai industrial area, Duhai"
    }
}

def load_data(file_path, default_data):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f: return json.load(f)
        except: return default_data
    return default_data

def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

if "users_db" not in st.session_state: st.session_state.users_db = load_data(USERS_FILE, DEFAULT_USERS)
if "orders" not in st.session_state: st.session_state.orders = load_data(ORDERS_FILE, [])
if "bills" not in st.session_state: st.session_state.bills = load_data(BILLS_FILE, [])

# --- NOTIFICATION SOUND ---
def play_sound():
    # Ek simple default notification beep sound
    sound_html = """
    <audio autoplay="true">
        <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg">
    </audio>
    """
    st.markdown(sound_html, unsafe_allow_html=True)

# --- CSS STYLING ---
st.markdown("""
<style>
    .header-banner { background: #b71c1c; color: white; padding: 20px; text-align: center; border-radius: 8px; margin-bottom: 20px; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #f1f1f1; color: #333; text-align: center; padding: 10px; font-size: 12px; font-weight: bold; }
    .v-card { background: white; border: 2px solid #b71c1c; border-radius: 5px; padding: 15px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    .v-card h3 { color: #b71c1c; margin: 0; font-family: Arial Black; }
    .v-card p { font-size: 12px; margin: 5px 0; color: #333; }
    .v-card .contact { font-weight: bold; color: #b71c1c; font-size: 14px; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# --- VIRTUAL CARD ---
def show_virtual_card():
    st.sidebar.markdown("""
    <div class="v-card">
        <h3>N.R. TRADERS</h3>
        <p><b>Deals In:</b> All Type Of Oxygen, Co2, Nitrogen<br>Argon, Da Gas Cylinder & Welding Material</p>
        <hr style="margin:10px 0;">
        <p><b>Address:</b> Panchal Market, Duhai industrial area, Duhai, Ghaziabad (U.P.)</p>
        <div class="contact">
            Nitin Sharma<br>
            📞 9999734204 | 8130853589
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- APP BANNER ---
st.markdown("""
<div class="header-banner">
    <h1 style="margin:0;">N.R. TRADERS - OFFICIAL PORTAL</h1>
    <p style="margin:0;">GSTIN: 09MHSPS5749H1Z3 | Authorized Dealer & Supplier</p>
</div>
""", unsafe_allow_html=True)

# --- LOGIN SYSTEM ---
if "user" not in st.session_state:
    show_virtual_card()
    st.sidebar.subheader("🔐 Secure Login")
    user_id = st.sidebar.text_input("User ID")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if user_id in st.session_state.users_db and st.session_state.users_db[user_id]["password"] == password:
            st.session_state.user = user_id
            st.rerun()
        else:
            st.sidebar.error("❌ Invalid ID or Password")
else:
    role = st.session_state.users_db[st.session_state.user]["role"]
    show_virtual_card()
    st.sidebar.success(f"Logged in as: {st.session_state.users_db[st.session_state.user]['name']}")
    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()
    if st.sidebar.button("🚪 Logout"):
        del st.session_state.user
        st.rerun()

    # ================= PARTY (CLIENT) DASHBOARD =================
    if role == "party":
        tab1, tab2 = st.tabs(["🛒 Place Order", "📄 View Bills/Challans"])
        
        with tab1:
            st.subheader("Place New Order")
            gas_type = st.selectbox("Select Gas", ["Oxygen (O2)", "Carbon Dioxide (CO2)", "Argon (Ar)", "Nitrogen (N2)"])
            qty = st.number_input("Quantity", min_value=1, value=1)
            
            if st.button("🚀 Confirm Order"):
                new_order = {
                    "id": f"ORD{len(st.session_state.orders)+100}",
                    "party": st.session_state.user,
                    "company": st.session_state.users_db[st.session_state.user]["company"],
                    "gas": gas_type,
                    "qty": qty,
                    "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "Pending",
                    "eta": "Awaiting"
                }
                st.session_state.orders.insert(0, new_order)
                save_data(ORDERS_FILE, st.session_state.orders)
                play_sound()
                st.success("✅ Order Placed Successfully")
                
            st.markdown("---")
            st.subheader("Your Recent Orders (1-Min Cancellation)")
            for idx, ord_item in enumerate(st.session_state.orders):
                if ord_item["party"] == st.session_state.user:
                    st.write(f"**{ord_item['id']}** | {ord_item['gas']} (Qty: {ord_item['qty']}) | Status: {ord_item['status']} | ETA: {ord_item['eta']}")
                    
                    if ord_item["status"] == "Pending":
                        time_diff = (datetime.datetime.now() - datetime.datetime.strptime(ord_item["time"], "%Y-%m-%d %H:%M:%S")).total_seconds()
                        if time_diff <= 60:
                            if st.button("❌ Cancel Order", key=f"cancel_{ord_item['id']}"):
                                st.session_state.orders.pop(idx)
                                save_data(ORDERS_FILE, st.session_state.orders)
                                st.rerun()
                        else:
                            st.caption("Cancellation window (1 min) closed.")
                    st.divider()

        with tab2:
            st.subheader("Your Invoices & Challans")
            for bill in st.session_state.bills:
                if bill["party"] == st.session_state.user:
                    st.info(f"📄 Document: {bill['filename']} (Uploaded: {bill['date']})")

    # ================= ADMIN DASHBOARD =================
    elif role == "admin":
        tab1, tab2, tab3 = st.tabs(["📥 Live Orders", "📤 Upload Bills", "👥 Manage Clients"])
        
        with tab1:
            st.subheader("Live Order Management")
            for idx, ord_item in enumerate(st.session_state.orders):
                st.markdown(f"**{ord_item['company']}** ordered **{ord_item['qty']}x {ord_item['gas']}** at {ord_item['time']}")
                
                if ord_item["status"] == "Pending":
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        eta = st.text_input("ETA (e.g., 2 Hours / 4 PM)", key=f"eta_{ord_item['id']}")
                    with col2:
                        if st.button("✅ Accept", key=f"acc_{ord_item['id']}"):
                            st.session_state.orders[idx]["status"] = "Accepted"
                            st.session_state.orders[idx]["eta"] = eta if eta else "ASAP"
                            save_data(ORDERS_FILE, st.session_state.orders)
                            play_sound()
                            st.rerun()
                    with col3:
                        if st.button("🗑️ Delete", key=f"del_{ord_item['id']}"):
                            st.session_state.orders.pop(idx)
                            save_data(ORDERS_FILE, st.session_state.orders)
                            st.rerun()
                else:
                    st.success(f"Status: {ord_item['status']} | ETA: {ord_item['eta']}")
                st.divider()

        with tab2:
            st.subheader("Upload Challans & Bills")
            parties = {k: v["company"] for k, v in st.session_state.users_db.items() if v["role"] == "party"}
            selected_party = st.selectbox("Select Party", list(parties.keys()), format_func=lambda x: parties[x])
            
            uploaded_file = st.file_uploader("Upload File", type=['pdf', 'png', 'jpg', 'jpeg', 'docx', 'xlsx', 'txt'])
            if uploaded_file is not None:
                if st.button("Upload to Portal"):
                    # Abhi JSON me save kar rahe hain (Drive me save karne ke liye Drive API upload logic lagega)
                    st.session_state.bills.append({
                        "party": selected_party,
                        "filename": uploaded_file.name,
                        "date": datetime.datetime.now().strftime("%Y-%m-%d")
                    })
                    save_data(BILLS_FILE, st.session_state.bills)
                    st.success(f"✅ {uploaded_file.name} uploaded for {parties[selected_party]}")

        with tab3:
            st.subheader("Client Directory")
            action = st.radio("Action", ["Add New", "Edit Existing"])
            
            if action == "Add New":
                nid = st.text_input("New User ID")
                npass = st.text_input("Password")
                ncomp = st.text_input("Company Name")
                ngst = st.text_input("GST Number")
                if st.button("Add Client") and nid:
                    st.session_state.users_db[nid] = {"password": npass, "role": "party", "name": ncomp, "company": ncomp, "gst": ngst}
                    save_data(USERS_FILE, st.session_state.users_db)
                    st.success("Client Added!")
                    st.rerun()
                    
            elif action == "Edit Existing":
                parties = [k for k, v in st.session_state.users_db.items() if v["role"] == "party"]
                if parties:
                    edit_id = st.selectbox("Select Client to Edit", parties)
                    e_comp = st.text_input("Company Name", value=st.session_state.users_db[edit_id]["company"])
                    e_gst = st.text_input("GST Number", value=st.session_state.users_db[edit_id].get("gst", ""))
                    e_pass = st.text_input("Password", value=st.session_state.users_db[edit_id]["password"])
                    
                    if st.button("Update Details"):
                        st.session_state.users_db[edit_id].update({"company": e_comp, "name": e_comp, "gst": e_gst, "password": e_pass})
                        save_data(USERS_FILE, st.session_state.users_db)
                        st.success("Details Updated!")
                        st.rerun()

# --- FOOTER ---
st.markdown("""
<div class="footer">
    © 2026 N.R. TRADERS. All Rights Reserved. | Official Business Portal
</div>
""", unsafe_allow_html=True)
