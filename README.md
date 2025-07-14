# 🥛 Ksheeram - Smart Local Milk Delivery Platform

**Ksheeram** is a modern web application connecting local dairy sellers with buyers for seamless ordering and delivery of milk and dairy products. Powered by Flask, MongoDB, JWT authentication, and geolocation-based services.

---

[![Deploy on Render](https://img.shields.io/badge/Deploy%20on-Render-blueviolet?logo=render)](https://render.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🚀 Features

### 👥 Buyer Authentication
- JWT-based login and registration
- Secure cookie storage
- Logout support

### 📦 Order Management
- Cart management with product/plan support
- Multi-seller (simulated) payment
- Complete buyer order history

### 📍 Location Awareness
- Save and retrieve geolocation
- Display sellers within a 10 km radius using the Haversine formula

### 👨‍💼 Seller Dashboard
- Seller registration and login
- Product and plan management for sellers

---

## 🧱 Project Structure

ksheeram/
│
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
├── seller_dashboard/       # Seller Blueprint
│   └── seller_app.py
├── app.py                  # Main app
├── requirements.txt        # Python dependencies
└── README.md
---

## 🌐 Live Demo

**Render Deployment:**  
🔗 [https://ksheeram.onrender.com](https://ksheeram.onrender.com)

---

## 🛠️ Deploying on Render

### Steps to Deploy

1. **Push your code to GitHub** (if not already).
2. **Go to [Render.com](https://render.com)** and log in.
3. Click **"New Web Service"**.
4. Connect your GitHub repository.
5. Set the following settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
   - **Environment:** Python 3.10+
   - Add environment variables for:
     - `SECRET_KEY`
     - `JWT_SECRET_KEY`
     - MongoDB connection URI (if needed)
6. Click **Deploy**.

---

## 📡 API Overview

### 🔐 Authentication
- `POST /login/buyer`
- `POST /register/buyer`
- `GET`/`POST /logout`

### 📍 Location
- `POST /save-location`
- `GET /get-user-location`
- `POST /get-sellers-nearby`

### 🛒 Cart
- `GET /cart/get`
- `POST /cart/add`
- `POST /cart/add-plan`
- `POST /cart/update`
- `POST /cart/remove`

### 📦 Orders
- `POST /order/create`
- `POST /fake_payment/initiate`
- `GET /orders/get`

### 👤 Profile
- `GET /account/details`
- `POST /account/update`

---

## 🗃️ MongoDB Collections

- `buyers`
- `sellersinfo`
- `carts`
- `orders`

---

## 📦 Local Installation

# Clone the repository
git clone https://github.com/SreeTarak2/Ksheeram.git
cd Ksheeram

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py

---

## ✅ TODO

- [x] Buyer-Seller Split
- [x] JWT Secure Auth
- [x] Order System & Cart
- [x] Location-based Seller Matching
- [ ] Real Payment Gateway (e.g., Razorpay)
- [ ] Admin Panel for Seller Verification
- [ ] Mobile-friendly UI with Tailwind or Bootstrap

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

## 🙌 Author

Made with ❤️ by **Vamsi Krishna**  
GitHub: [@SreeTarak2](https://github.com/SreeTarak2)
