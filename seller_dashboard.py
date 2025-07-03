from flask import Flask, render_template, request, redirect, url_for, jsonify, Blueprint
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from flask_cors import CORS
from datetime import timedelta, datetime, timezone
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    unset_jwt_cookies,
)
import bcrypt
import logging

# All routes in this file will be prefixed with /seller (defined in app.py)
seller_app = Blueprint("seller_app", __name__, template_folder="templates/seller")
CORS(seller_app, supports_credentials=True)

# REMOVED: JWT and App config is inherited from the main app.py

# MongoDB Connection
MONGO_URI = "mongodb+srv://jstvamsikrisha:vamsikrishna@cluster0.wzwriwa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
    db = client["ksheeram"]
    sellers_info = db["sellersinfo"]
    orders_collection = db["orders"]
    print("Seller Blueprint: Connected to MongoDB")
except Exception as e:
    logging.error(f"Seller Blueprint MongoDB Error: {e}")
    raise SystemExit("Seller DB connection failed.")


# Helper function
def convert_mongo_types(obj):
    if isinstance(obj, list):
        return [convert_mongo_types(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: convert_mongo_types(v) for k, v in obj.items()}
    elif isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, datetime):
        # Using a more detailed format for seller view
        return obj.strftime("%d/%m/%Y %H:%M")
    else:
        return obj


# Renamed index to login_page to avoid confusion with main app's index
@seller_app.route("/")
@seller_app.route("/login")
def login_page():
    return render_template("login.html")


@seller_app.route("/dashboard")
@jwt_required()
def dashboard():
    try:
        user_email = get_jwt_identity()
        seller = sellers_info.find_one({"email": user_email})
        if not seller:
            # FIXED: Correctly redirect to the namespaced login route
            return redirect(url_for("seller_app.login_page"))

        seller_id = seller["_id"]

        # Find all orders where this seller's ID is the main seller_id
        seller_orders = list(orders_collection.find({"seller_id": seller_id}))

        stats = {
            "total_products": len(seller.get("products", [])),
            "total_orders": len(seller_orders),
            "pending_orders": sum(
                1 for o in seller_orders if o.get("status") == "Pending"
            ),
            "total_revenue": sum(
                float(o.get("total_amount", 0))
                for o in seller_orders
                if o.get("status") == "Delivered"
            ),
        }

        recent_orders = sorted(
            seller_orders,
            key=lambda x: x.get(
                "order_date", datetime.min.replace(tzinfo=timezone.utc)
            ),
            reverse=True,
        )[:5]

        # NOTE: You will need to make sure your seller templates are in a subfolder
        # e.g., templates/seller/dashboard.html
        return render_template(
            "dashboard.html",
            stats=stats,
            recent_orders=convert_mongo_types(recent_orders),
            seller=seller,
        )

    except Exception as e:
        # This will now correctly log the actual error instead of the BuildError
        logging.error(f"Dashboard error: {e}", exc_info=True)
        return "An internal error occurred", 500


@seller_app.route("/products")
@jwt_required()
def products():
    user_email = get_jwt_identity()
    seller = sellers_info.find_one({"email": user_email})
    if not seller:
        return redirect(url_for("seller_app.login_page"))
    products_data = seller.get("products", [])
    return render_template(
        "sellerside_products.html", products=products_data, seller=seller
    )


@seller_app.route("/orders")
@jwt_required()
def orders():
    user_email = get_jwt_identity()
    seller = sellers_info.find_one({"email": user_email})
    if not seller:
        # FIXED: Correctly redirect to the namespaced login route
        return redirect(url_for("seller_app.login_page"))

    seller_id = seller["_id"]
    # Your order finding logic is much simpler now
    seller_orders = list(orders_collection.find({"seller_id": seller_id}))

    return render_template(
        "orders.html", orders=convert_mongo_types(seller_orders), seller=seller
    )


@seller_app.route("/settings")
@jwt_required()
def settings():
    user_email = get_jwt_identity()
    seller_data = sellers_info.find_one({"email": user_email})
    if not seller_data:
        return redirect(url_for("seller_app.login_page"))
    return render_template("settings.html", seller=seller_data)


# ======================== sellers Products ==========================
@seller_app.route("/api/add_product", methods=["POST"])
@jwt_required()
def add_product():
    try:
        user_email = get_jwt_identity()
        new_product = {
            "_id": ObjectId(),
            "name": request.form["name"],
            "price": float(request.form["price"]),
            "unit": request.form["unit"],
            "category": request.form.get("category", "milk"),
            "description": request.form.get("description", ""),
            "image_url": request.form.get("image_url", "default_image_url.jpg"),
            "stock": int(request.form.get("stock", 0)),
            "in_stock": int(request.form.get("stock", 0)) > 0,
        }
        sellers_info.update_one(
            {"email": user_email}, {"$push": {"products": new_product}}
        )
        return redirect(url_for("seller_app.products"))
    except Exception as e:
        logging.error(f"Add product error: {e}")
        return "Server Error", 500


# delete product
@seller_app.route("/api/delete_product", methods=["POST"])
@jwt_required()
def delete_product():
    user_email = get_jwt_identity()
    product_id = request.form.get("product_id")
    if not product_id:
        return "Product ID is required", 400

    # Convert product_id string to ObjectId
    try:
        product_oid = ObjectId(product_id)
    except Exception as e:
        return "Invalid Product ID", 400

    # Delete product from the seller's products list by _id
    result = sellers_info.update_one(
        {"email": user_email}, {"$pull": {"products": {"_id": product_oid}}}
    )

    if result.modified_count == 0:
        return "Product not found or already deleted", 404

    return redirect(url_for("seller_app.products"))


# update product stock
@seller_app.route("/api/update_product_stock", methods=["POST"])
@jwt_required()
def update_product_stock():
    user_email = get_jwt_identity()
    product_name = request.form["product_name"]
    new_stock = int(request.form["stock"])
    in_stock = new_stock > 0
    sellers_info.update_one(
        {"email": user_email, "products.name": product_name},
        {"$set": {"products.$.stock": new_stock, "products.$.in_stock": in_stock}},
    )
    return redirect(url_for("seller_app.products"))


# update the order details
@seller_app.route("/api/update_order_status", methods=["POST"])
@jwt_required()
def update_order_status():
    order_id = request.form["order_id"]
    new_status = request.form["status"]
    orders_collection.update_one(
        {"_id": ObjectId(order_id)}, {"$set": {"status": new_status}}
    )
    return redirect(url_for("seller_app.orders"))


# update the seller
@seller_app.route("/api/update_seller", methods=["POST"])
@jwt_required()
def update_seller():
    user_email = get_jwt_identity()
    update_data = {
        "name": request.form["name"],
        "phone": request.form["phone"],
        "address": request.form.get("address", ""),
        "description": request.form.get("description", ""),
        "latitude": request.form.get("latitude", ""),
        "longitude": request.form.get("longitude", ""),
        "rating": float(request.form.get("rating", 4.5)),
    }
    update_data = {k: v for k, v in update_data.items() if v != ""}
    sellers_info.update_one({"email": user_email}, {"$set": update_data})
    return redirect(url_for("seller_app.settings"))


@seller_app.route("/api/add_plan", methods=["POST"])
@jwt_required()
def add_plan():
    user_email = get_jwt_identity()
    new_plan = {
        "name": request.form["name"],
        "price": request.form["price"],
        "description": request.form.get("description", ""),
        "duration": request.form.get("duration", "1 month"),
    }
    sellers_info.update_one({"email": user_email}, {"$push": {"plans": new_plan}})
    return redirect(url_for("seller_app.settings"))


@seller_app.route("/api/delete_plan", methods=["POST"])
@jwt_required()
def delete_plan():
    user_email = get_jwt_identity()
    plan_name = request.form["plan_name"]
    sellers_info.update_one(
        {"email": user_email}, {"$pull": {"plans": {"name": plan_name}}}
    )
    return redirect(url_for("seller_app.settings"))


# ---------- Seller Auth Routes ----------


@seller_app.route("/register", methods=["POST"])
def signup_seller():
    try:
        data = request.get_json()
        # CHANGED: Standardized to 'name'
        store_name = data.get("storeName")
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")

        if not all([store_name, email, phone, password]):
            return jsonify({"error": "All fields required"}), 400
        if sellers_info.find_one({"email": email}):
            return jsonify({"error": "Email already in use"}), 400

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_seller = {
            "name": store_name,
            "email": email,
            "phone": phone,
            "password": hashed_password,
            "products": [],
            "plans": [],
        }
        sellers_info.insert_one(new_seller)

        access_token = create_access_token(
            identity=email, expires_delta=timedelta(hours=1)
        )
        resp = jsonify(
            {
                "message": "Registration successful",
                "redirect": url_for("seller_app.dashboard"),
            }
        )
        set_access_cookies(resp, access_token, max_age=timedelta(hours=1))
        return resp

    except Exception as e:
        logging.error(f"Seller registration error: {e}", exc_info=True)
        return jsonify({"error": "Server error"}), 500


@seller_app.route("/login", methods=["POST"])
def seller_login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        seller = sellers_info.find_one({"email": email})

        if not seller or not bcrypt.checkpw(
            password.encode(), seller["password"].encode()
        ):
            return jsonify({"error": "Invalid credentials"}), 401

        access_token = create_access_token(
            identity=seller["email"], expires_delta=timedelta(hours=1)
        )
        resp = jsonify(
            {"message": "Login successful", "redirect": url_for("seller_app.dashboard")}
        )
        set_access_cookies(resp, access_token, max_age=timedelta(hours=1))
        return resp

    except Exception as e:
        logging.error(f"Seller login error: {e}", exc_info=True)
        return jsonify({"error": "Server error"}), 500


@seller_app.route("/logout", methods=["POST", "GET"])
@jwt_required(optional=True)
def logout():
    resp = jsonify({"message": "Logged out successfully", "redirect": url_for("index")})
    unset_jwt_cookies(resp)
    return resp
