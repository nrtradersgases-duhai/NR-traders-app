<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
		<title>N R TRADERS - Client Portal</title>
		<style>
			/* Professional Business Theme */
			:root {
			    --primary-blue: #0A3D62;
			    --payment-green: #218C74;
			    --bg-color: #F4F7F6;
			    --text-dark: #2F3542;
			    --white: #FFFFFF;
			}
			body {
			    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
			    background-color: var(--bg-color);
			    color: var(--text-dark);
			    margin: 0;
			    padding: 0;
			    display: flex;
			    flex-direction: column;
			    min-height: 100vh;
			}
			/* Login Screen */
			#login-screen {
			    display: flex;
			    flex-direction: column;
			    align-items: center;
			    justify-content: center;
			    flex-grow: 1;
			}
			.login-box {
			    background: var(--white);
			    padding: 40px;
			    border-radius: 8px;
			    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
			    width: 100%;
			    max-width: 400px;
			    text-align: center;
			}
			.login-box input, .login-box select {
			    width: 90%;
			    padding: 10px;
			    margin: 10px 0;
			    border: 1px solid #ccc;
			    border-radius: 4px;
			}
			.btn {
			    background-color: var(--primary-blue);
			    color: var(--white);
			    border: none;
			    padding: 10px 20px;
			    border-radius: 4px;
			    cursor: pointer;
			    font-size: 16px;
			    transition: background 0.3s;
			}
			.btn:hover { background-color: #062b47; }

			/* Dashboard & Navigation */
			#dashboard { display: none; width: 100%; }
			.top-nav {
			    background-color: var(--primary-blue);
			    color: var(--white);
			    padding: 15px 20px;
			    display: flex;
			    justify-content: space-between;
			    align-items: center;
			}
			.notification-icon {
			    position: relative;
			    cursor: pointer;
			    font-size: 24px;
			}
			.badge {
			    position: absolute;
			    top: -5px;
			    right: -10px;
			    background-color: red;
			    color: white;
			    border-radius: 50%;
			    padding: 2px 6px;
			    font-size: 12px;
			    font-weight: bold;
			}

			/* Content Area */
			.content { padding: 20px; max-width: 1200px; margin: 0 auto; }

			/* Prominent Payment Box */
			.payment-highlight-box {
			    background-color: var(--payment-green);
			    color: var(--white);
			    padding: 30px;
			    border-radius: 8px;
			    text-align: center;
			    cursor: pointer;
			    margin-bottom: 20px;
			    box-shadow: 0 4px 15px rgba(33, 140, 116, 0.4);
			    transition: transform 0.2s;
			}
			.payment-highlight-box:active { transform: scale(0.98); }
			.payment-highlight-box h2 { margin: 0; font-size: 24px; }
			.payment-highlight-box p { margin: 10px 0 0 0; font-size: 14px; opacity: 0.9; }

			/* Payment Details Section */
			#payment-details-view {
			    display: none;
			    background: var(--white);
			    padding: 20px;
			    border-radius: 8px;
			    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
			    margin-top: 20px;
			    border-left: 5px solid var(--payment-green);
			}
			.qr-container { display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; }
			.qr-box { text-align: center; border: 1px solid #eee; padding: 10px; border-radius: 8px; }
			.qr-box img { max-width: 200px; height: auto; }

			/* Admin Bank Edit Section */
			#admin-bank-section {
			    display: none;
			    background: #fff3cd;
			    padding: 20px;
			    border-radius: 8px;
			    margin-top: 20px;
			    border-left: 5px solid #ffc107;
			}

			/* PWA Install Prompts */
			.install-prompt {
			    background: #e1f5fe;
			    padding: 15px;
			    margin-top: 20px;
			    border-radius: 8px;
			    text-align: center;
			    display: none;
			}

			/* Footer */
			.footer {
			    text-align: center;
			    padding: 20px;
			    font-size: 12px;
			    color: #7f8fa6;
			    margin-top: auto;
			}
			.legal-terms { font-size: 10px; margin-top: 10px; }
		</style>
	</head>
	<body>
		<!-- Notification Sound -->
		<audio
			id="notif-sound"
			src="data:audio/wav;base64,UklGRl9vT19XQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YU..."
			preload="auto"
		></audio>

		<!-- Login Screen -->
		<div id="login-screen">
			<div class="login-box">
				<h2>N R TRADERS Portal</h2>
				<p style="color: #666; font-size: 14px;">Secure Portal Login</p>
				<select id="user-role">
					<option value="billing">Billing Customer</option>
					<option value="cash">Cash Customer</option>
					<option value="admin">Admin</option>
				</select>
				<button class="btn" onclick="processLogin()">Secure Login</button>
			</div>

			<div class="footer">
				<strong>Made with Love for their exclusive customers by N R TRADERS</strong>
				<div class="legal-terms">
					Licensed under the Apache License, Version 2.0<br />
					You may obtain a copy of the License at
					http://www.apache.org/licenses/LICENSE-2.0
				</div>
			</div>
		</div>

		<!-- Main Dashboard -->
		<div id="dashboard">
			<div class="top-nav">
				<div>N R TRADERS Dashboard</div>
				<div class="notification-icon" onclick="playNotification()">
					🔔 <span class="badge" id="notif-badge">1</span>
				</div>
			</div>

			<div class="content">
				<!-- PWA Install Prompts -->
				<div id="android-install" class="install-prompt">
					<p>Install our Web App for a seamless experience.</p>
					<button class="btn" id="install-btn">Download App</button>
				</div>
				<div id="ios-install" class="install-prompt">
					<p>
						To install on iOS: Tap the <strong>Share</strong> icon below and select
						<strong>'Add to Home Screen'</strong>.
					</p>
				</div>

				<!-- Prominent Payment Action Box -->
				<div class="payment-highlight-box" onclick="togglePaymentDetails()">
					<h2>Initiate Payment</h2>
					<p>Click here to view your secure payment options</p>
				</div>

				<!-- Dynamic Payment Details -->
				<div id="payment-details-view">
					<h3 style="margin-top:0;">Payment Information</h3>

					<!-- View for Billing Customers -->
					<div id="billing-view" style="display:none;">
						<h4>Current Account Details</h4>
						<p>
							<strong>Bank Name:</strong>
							<span id="display-bank">HDFC BANK, RAJENDER NAGAR</span>
						</p>
						<p><strong>Account No:</strong> <span id="display-acc">50200099034568</span></p>
						<p><strong>IFSC Code:</strong> <span id="display-ifsc">HDFC0001266</span></p>
						<p>
							<strong>Account Holder:</strong> <span id="display-name">N R TRADERS</span>
						</p>
					</div>

					<!-- View for Cash Customers -->
					<div id="cash-view" style="display:none;">
						<h4>UPI & Barcode Scanning</h4>
						<div class="qr-container">
							<div class="qr-box">
								<p><strong>Paytm Business</strong><br />Receiver: N R TRADERS</p>
								<img src="image.png" alt="Business QR - N R Traders" />
							</div>
							<div class="qr-box">
								<p><strong>UPI / IDFC First Bank</strong><br />Receiver: Nitin Sharma</p>
								<img src="image_2.png" alt="Savings QR - Nitin Sharma" />
								<p style="font-size:12px; color:#555;">UPI ID: nitin.sharma@upi</p>
							</div>
						</div>
					</div>
				</div>

				<!-- Admin Only Section -->
				<div id="admin-bank-section">
					<h3>Admin: Manage Bank Details</h3>
					<label>Bank Name:</label>
					<input
						type="text"
						id="edit-bank"
						value="HDFC BANK, RAJENDER NAGAR"
						style="width:100%; padding:8px; margin-bottom:10px;"
					/>
					<label>Account Number:</label>
					<input
						type="text"
						id="edit-acc"
						value="50200099034568"
						style="width:100%; padding:8px; margin-bottom:10px;"
					/>
					<label>IFSC Code:</label>
					<input
						type="text"
						id="edit-ifsc"
						value="HDFC0001266"
						style="width:100%; padding:8px; margin-bottom:10px;"
					/>
					<button
						class="btn"
						onclick="updateBankDetails()"
						style="background-color: #d32f2f;"
					>
						Update Bank Details
					</button>
				</div>

				<button
					class="btn"
					onclick="logout()"
					style="margin-top: 40px; background-color:#7f8fa6;"
				>
					Logout
				</button>
			</div>

			<div class="footer">
				<strong>Made with Love for their exclusive customers by N R TRADERS</strong>
				<div class="legal-terms">Apache 2.0 Licensed</div>
			</div>
		</div>

		<script>
			let currentUserRole = '';

			// Professional Login Transition
			function processLogin() {
			    currentUserRole = document.getElementById('user-role').value;
			    document.getElementById('login-screen').style.display = 'none';
			    document.getElementById('dashboard').style.display = 'block';
			    setupDashboard();
			    detectDeviceForPWA();
			}

			// Setup Dashboard based on Role
			function setupDashboard() {
			    document.getElementById('billing-view').style.display = 'none';
			    document.getElementById('cash-view').style.display = 'none';
			    document.getElementById('admin-bank-section').style.display = 'none';
			    document.getElementById('payment-details-view').style.display = 'none';

			    if (currentUserRole === 'admin') {
			        document.getElementById('admin-bank-section').style.display = 'block';
			        document.getElementById('billing-view').style.display = 'block';
			    } else if (currentUserRole === 'billing') {
			        document.getElementById('billing-view').style.display = 'block';
			    } else if (currentUserRole === 'cash') {
			        document.getElementById('cash-view').style.display = 'block';
			    }
			}

			// Toggle Payment Details Box
			function togglePaymentDetails() {
			    const detailsView = document.getElementById('payment-details-view');
			    if (detailsView.style.display === 'none' || detailsView.style.display === '') {
			        detailsView.style.display = 'block';
			    } else {
			        detailsView.style.display = 'none';
			    }
			}

			// Admin Function: Edit Bank Details
			function updateBankDetails() {
			    const newBank = document.getElementById('edit-bank').value;
			    const newAcc = document.getElementById('edit-acc').value;
			    const newIfsc = document.getElementById('edit-ifsc').value;

			    document.getElementById('display-bank').innerText = newBank;
			    document.getElementById('display-acc').innerText = newAcc;
			    document.getElementById('display-ifsc').innerText = newIfsc;

			    alert('Bank details updated successfully.');
			}

			// Notification Sound Logic
			function playNotification() {
			    const audio = document.getElementById('notif-sound');
			    audio.play().catch(e => console.log("Audio play requires interaction first."));
			    document.getElementById('notif-badge').style.display = 'none';
			}

			// Device Detection for PWA Prompts
			function detectDeviceForPWA() {
			    const userAgent = window.navigator.userAgent.toLowerCase();
			    const isIOS = /iphone|ipad|ipod/.test(userAgent);

			    if (isIOS) {
			        document.getElementById('ios-install').style.display = 'block';
			    } else {
			        document.getElementById('android-install').style.display = 'block';
			    }
			}

			function logout() {
			    document.getElementById('dashboard').style.display = 'none';
			    document.getElementById('login-screen').style.display = 'flex';
			}
		</script>
	</body>
</html>
