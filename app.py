from flask import Flask, jsonify, request, render_template
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    unset_jwt_cookies,
)
import bcrypt
from datetime import timedelta, datetime, timezone
import logging
from math import radians, cos, sin, asin, sqrt
from bson import ObjectId
import time
import random

from seller_dashboard import seller_app

app = Flask(__name__)
app.register_blueprint(seller_app, url_prefix='/seller')
CORS(app, supports_credentials=True)



# Add these JWT configurations to your Flask app
app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config["JWT_COOKIE_SAMESITE"] = "Lax"
app.config["JWT_ACCESS_COOKIE_NAME"] = "access"
jwt = JWTManager(app)

# Mongo setup
MONGO_URI = "mongodb+srv://jstvamsikrisha:vamsikrishna@cluster0.wzwriwa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
base_url = "https://ksheeram.onrender.com"


try:
    # client = MongoClient("mongodb://localhost:27017/")
    client  = MongoClient(MONGO_URI,server_api=ServerApi('1'))
    db = client["ksheeram"]
    buyers_collection = db["buyers"]
    # sellers_info = db["sellers"]
    sellers_info = db["sellersinfo"]
    carts_collection = db["carts"]
    orders_collection = db["orders"]
    print("Connected to MongoDB")
except Exception as e:
    logging.error(f"MongoDB Error: {e}")
    raise SystemExit("DB connection failed.")


# Routes
@app.route("/")
def index():
    return render_template("index.html")

# home route
@app.route("/home")
@jwt_required()
def home():
    user = get_jwt_identity()
    return render_template("home.html", user=user)

# sellers route
@app.route("/sellers")
@jwt_required()
def sellers():
    user = get_jwt_identity()
    return render_template("sellers.html", user=user)


# ========================== Products ==========================
@app.route("/products/", methods=["GET"])
@app.route("/products", methods=["GET"])
@jwt_required()
def products():
    # Get the email of the user from the JWT
    user_email = get_jwt_identity()
    print(f"User email: {user_email}")  # Debugging: Check the extracted user email

    # Step 1: Get User's Location
    user_data = buyers_collection.find_one({"email": user_email})
    user_location = user_data.get("last_location") if user_data else None

    # Step 2: Fetch all products from all sellers
    all_sellers = list(sellers_info.find())
    all_products = []

    for seller in all_sellers:
        if "products" in seller:
            for product in seller["products"]:
                all_products.append(
                    {
                        "seller_id": str(seller["_id"]),
                        "name": product["name"],
                        "price": product["price"],
                        "unit": product["unit"],
                        "seller": seller.get("name", "Unnamed Store"),
                        "ratings": seller.get("rating", 4.5),
                        "image_url": product.get("image_url", "default_image_url.jpg"),
                        "in_stock": product.get("in_stock", True),
                        "category": product.get("category", "milk"),
                    }
                )

    if not all_products:
        return render_template(
            "products.html", user=user_email, nearby_products=[], other_products=[]
        )

    # Step 3: Partition products into "nearby" and "other" based on user location
    nearby_products = []
    other_products = []
    search_radius_km = 10  # 10km radius for "nearby"

    if user_location and "lat" in user_location and "lon" in user_location:
        user_lat = user_location["lat"]
        user_lon = user_location["lon"]

        # Find nearby seller IDs first
        nearby_seller_ids = set()
        for seller in all_sellers:
            try:
                seller_lat = float(seller.get("latitude"))
                seller_lon = float(seller.get("longitude"))
                dist = haversine(user_lat, user_lon, seller_lat, seller_lon)
                if dist <= search_radius_km:
                    nearby_seller_ids.add(str(seller["_id"]))
            except (ValueError, TypeError, KeyError) as e:
                print(f"Error processing seller's location: {e}")
                continue

        # Partition the products into nearby and other categories
        for product in all_products:
            if product["seller_id"] in nearby_seller_ids:
                nearby_products.append(product)
            else:
                other_products.append(product)
    else:
        # If no location data available, put everything in "other_products"
        other_products = all_products

    # Render the template with both nearby and other products
    return render_template(
        "products.html",
        user=user_email,
        nearby_products=nearby_products,
        other_products=other_products,
    )


# --------------------------- My Orders --------------------------------
@app.route("/myorders", methods=["GET"])
@jwt_required()
def myorders():
    user = get_jwt_identity()
    return render_template("myorders.html", user=user)


# cart routes
@app.route("/mycart")
@jwt_required()
def my_cart_page():
    return render_template("mycart.html")


# retrieve cart
@app.route("/cart/get", methods=["GET"])
@jwt_required()
def get_cart():
    try:
        user_email = get_jwt_identity()
        user = buyers_collection.find_one({"email": user_email})
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Use the get_or_create_cart helper to ensure a cart always exists
        cart = get_or_create_cart(user["_id"])

        total_items_count = sum(
            item.get("quantity", 0) for item in cart.get("items", [])
        )

        items_with_ids = cart.get("items", [])
        for item in items_with_ids:
            if "seller_id" in item and isinstance(item["seller_id"], ObjectId):
                item["seller_id"] = str(item["seller_id"])

        return jsonify({"items": items_with_ids, "count": total_items_count}), 200

    except Exception as e:
        logging.error(f"Error in get_cart: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


# create or add to cart (for individual products)
@app.route("/cart/add", methods=["POST"])
@jwt_required()
def add_to_cart():
    try:
        user_email = get_jwt_identity()
        user = buyers_collection.find_one({"email": user_email})
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()
        product_name = data.get("name")
        seller_id = data.get("seller_id")

        if not product_name or not seller_id:
            return jsonify({"error": "Product name and seller ID are required"}), 400

        seller = sellers_info.find_one({"_id": ObjectId(seller_id)})
        if not seller:
            return jsonify({"error": "Seller not found"}), 404

        product_info = next(
            (p for p in seller.get("products", []) if p.get("name") == product_name),
            None,
        )
        if not product_info:
            return jsonify({"error": "Product not found"}), 404

        product_key = f"{seller_id}_{product_name}"
        cart = get_or_create_cart(user["_id"])

        # Check if item already exists by its unique key
        item_in_cart = carts_collection.find_one(
            {"_id": cart["_id"], "items.product_key": product_key}
        )

        if item_in_cart:
            # If it exists, just increment quantity
            carts_collection.update_one(
                {"_id": cart["_id"], "items.product_key": product_key},
                {
                    "$inc": {"items.$.quantity": 1},
                    "$set": {"updated_at": datetime.now(timezone.utc)},
                },
            )
        else:
            # If it doesn't exist, add it as a new item
            new_cart_item = {
                "product_key": product_key,
                "type": "product",  # Add a type for clarity
                "name": product_info.get("name"),
                "price": float(product_info.get("price")),
                "unit": product_info.get("unit"),
                "image_url": product_info.get("image_url"),
                "seller_name": seller.get("name"),
                "seller_id": seller_id,
                "quantity": 1,
            }
            carts_collection.update_one(
                {"_id": cart["_id"]},
                {
                    "$push": {"items": new_cart_item},
                    "$set": {"updated_at": datetime.now(timezone.utc)},
                },
            )

        return jsonify({"message": "Item added to cart"}), 200

    except Exception as e:
        logging.error(f"Error in add_to_cart: {str(e)}", exc_info=True)
        return jsonify({"error": "An internal server error occurred"}), 500


# Helper function to get or create a cart
def get_or_create_cart(buyer_id):
    cart = carts_collection.find_one({"buyer_id": buyer_id, "status": "active"})
    if not cart:
        new_cart = {
            "buyer_id": buyer_id,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "items": [],
            "status": "active",
        }
        result = carts_collection.insert_one(new_cart)
        new_cart["_id"] = result.inserted_id
        cart = new_cart
    return cart


# ---  Add a PLAN to the cart ---
@app.route("/cart/add-plan", methods=["POST"])
@jwt_required()
def add_plan_to_cart():
    try:
        user_email = get_jwt_identity()
        user = buyers_collection.find_one({"email": user_email})
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()
        plan_name, seller_id = data.get("plan_name"), data.get("seller_id")
        if not plan_name or not seller_id:
            return jsonify({"error": "Missing plan_name or seller_id"}), 400

        plan_key = f"{seller_id}_{plan_name}"
        seller = sellers_info.find_one({"_id": ObjectId(seller_id)})
        plan_info = next(
            (p for p in seller.get("plans", []) if p.get("name") == plan_name), None
        )
        if not plan_info:
            return jsonify({"error": "Plan not found"}), 404

        cart = get_or_create_cart(user["_id"])

        if (
            carts_collection.count_documents(
                {"_id": cart["_id"], "items.product_key": plan_key}
            )
            > 0
        ):
            return jsonify({"error": "This plan is already in your cart."}), 400

        price_str = plan_info.get("price", "0").split("/")[0].replace("₹", "").strip()
        new_item = {
            "product_key": plan_key,
            "type": "plan",
            "name": plan_info.get("name"),
            "price": float(price_str),
            "unit": "month",
            "image_url": seller.get("logo"),
            "seller_name": seller.get("name"),
            "seller_id": seller_id,  # Store as string for consistency
            "quantity": 1,
        }
        carts_collection.update_one(
            {"_id": cart["_id"]},
            {
                "$push": {"items": new_item},
                "$set": {"updated_at": datetime.now(timezone.utc)},
            },
        )
        return jsonify({"message": "Plan added to cart"}), 200
    except Exception as e:
        logging.error(f"Error adding plan: {e}", exc_info=True)
        return jsonify({"error": "Server error"}), 500


# --- UNIFIED Route to remove ANY item from the cart ---

@app.route("/cart/remove", methods=["POST"])
@jwt_required()
def remove_from_cart():
    try:
        user_email = get_jwt_identity()
        user = buyers_collection.find_one({"email": user_email})
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()
        product_key = data.get("product_key")
        if not product_key:
            return jsonify({"error": "product_key is required"}), 400

        cart = get_or_create_cart(user["_id"])

        result = carts_collection.update_one(
            {"_id": cart["_id"]}, {"$pull": {"items": {"product_key": product_key}}}
        )

        if result.modified_count == 0:
            logging.warning(
                f"Attempted to remove item not found in cart: {product_key}"
            )

            return jsonify({"message": "Item was not in the cart"}), 200

        carts_collection.update_one(
            {"_id": cart["_id"]}, {"$set": {"updated_at": datetime.now(timezone.utc)}}
        )
        return jsonify({"message": "Item removed successfully"}), 200
    except Exception as e:
        logging.error(f"Error removing from cart: {e}", exc_info=True)
        return jsonify({"error": "Server error"}), 500


# --- UNIFIED Route to update item quantity ---
@app.route("/cart/update", methods=["POST"])
@jwt_required()
def update_cart_item_quantity():
    try:
        user_email = get_jwt_identity()
        user = buyers_collection.find_one({"email": user_email})
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()
        product_key = data.get("product_key")
        quantity = data.get("quantity")

        if not product_key or quantity is None:
            return jsonify({"error": "product_key and quantity are required"}), 400

        if not isinstance(quantity, int) or quantity < 1:
            return jsonify({"error": "Quantity must be a positive integer"}), 400

        cart = get_or_create_cart(user["_id"])

        result = carts_collection.update_one(
            {"_id": cart["_id"], "items.product_key": product_key},
            {
                "$set": {
                    "items.$.quantity": quantity,
                    "updated_at": datetime.now(timezone.utc),
                }
            },
        )

        if result.modified_count == 0:
            return jsonify({"error": "Item not found in cart"}), 404

        return jsonify({"message": "Cart updated successfully"}), 200

    except Exception as e:
        logging.error(f"Error updating cart: {e}", exc_info=True)
        return jsonify({"error": "Server error"}), 500


# ======================= Account settings ================================


@app.route("/myaccount", methods=["GET"])
@jwt_required()
def my_account():
    user = get_jwt_identity()
    return render_template("myaccount.html", user=user)


# account details
@app.route("/account/details", methods=["GET"])
@jwt_required()
def get_account_details():
    try:
        user_email = get_jwt_identity()

        user_data = buyers_collection.find_one({"email": user_email})
        if not user_data:
            user_data = sellers_info.find_one({"email": user_email})

        if not user_data:
            return jsonify({"error": "User not found"}), 404

        response_data = {
            "fullName": user_data.get("fullName", user_data.get("storeName", "")),
            "email": user_data.get("email"),
            "phone": user_data.get("phone"),
        }
        return jsonify(response_data), 200

    except Exception as e:
        logging.error(f"Error fetching account details: {e}")
        return jsonify({"error": "Server error"}), 500


# update the account settings
@app.route("/account/update", methods=["POST"])
@jwt_required()
def update_account_details():
    try:
        user_email = get_jwt_identity()

        data = request.get_json()
        updated_full_name = data.get("fullName")
        updated_phone = data.get("phone")

        if not updated_full_name or not updated_phone:
            return jsonify({"error": "Full name and phone number are required"}), 400

        user_data = buyers_collection.find_one({"email": user_email})
        if not user_data:
            user_data = sellers_info.find_one({"email": user_email})

        if not user_data:
            return jsonify({"error": "User not found"}), 404

        if user_data.get("email") == user_email:
            if "fullName" in user_data:
                buyers_collection.update_one(
                    {"email": user_email},
                    {"$set": {"fullName": updated_full_name, "phone": updated_phone}},
                )
            else:
                sellers_info.update_one(
                    {"email": user_email},
                    {"$set": {"storeName": updated_full_name, "phone": updated_phone}},
                )

            return jsonify({"message": "Account updated successfully!"}), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        logging.error(f"Error updating account details: {e}")
        return jsonify({"error": "Server error"}), 500


# validate the objectid
def is_valid_objectid(id_string):
    try:
        ObjectId(id_string)
        return True
    except Exception:
        return False


# Select seller info
@app.route("/sellers/<string:seller_id>")
@jwt_required()
def seller_profile(seller_id):
    if not is_valid_objectid(seller_id):
        logging.warning(f"Invalid ObjectId format for seller profile: {seller_id}")
        return render_template("404.html"), 404

    seller_data = sellers_info.find_one({"_id": ObjectId(seller_id)})
    if not seller_data:
        logging.warning(f"Seller not found in database for ID: {seller_id}")
        return render_template("404.html"), 404

    return render_template(
        "sellers_info.html",
        seller=seller_data,
        plans=seller_data.get("plans", []),
        products=seller_data.get("products", []),
    )


# ---------- Buyer Login ----------
@app.route("/login/buyer", methods=["POST"])
def buyer_login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        user = buyers_collection.find_one({"email": email})
        if not user or not bcrypt.checkpw(password.encode(), user["password"].encode()):
            return jsonify({"error": "Invalid credentials"}), 401

        access_token = create_access_token(
            identity=email, expires_delta=timedelta(hours=1)
        )
        cookie_expires = timedelta(hours=1)
        resp = jsonify({"message": "Login successful", "redirect": f"{base_url}/home"})
        set_access_cookies(resp, access_token, max_age=cookie_expires)
        # resp.set_cookie("access_token", access_token, httponly=True, samesite="Lax")

        return resp

    except Exception as e:
        logging.error(f"Buyer login error: {e}")
        return jsonify({"error": "Server error"}), 500


# # ---------- Seller Login ----------
# @app.route("/login/seller", methods=["POST"])
# def seller_login():
#     try:
#         data = request.get_json()
#         identifier = data.get("email") or data.get("storeid")
#         password = data.get("password")

#         if not identifier or not password:
#             return jsonify({"error": "ID/email and password required"}), 400

#         seller = sellers_info.find_one(
#             {"$or": [{"email": identifier}, {"storeid": identifier}]}
#         )

#         if not seller or not bcrypt.checkpw(
#             password.encode(), seller["password"].encode()
#         ):
#             return jsonify({"error": "Invalid credentials"}), 401

#         access_token = create_access_token(
#             identity=identifier, expires_delta=timedelta(hours=1)
#         )
#         cookie_expiry = timedelta(hours=1)
#         resp = jsonify({"message": "Login successful", "redirect": "/home"})
#         set_access_cookies(resp, access_token, max_age=cookie_expiry)
#         # resp.set_cookie("access_token", access_token, httponly=True, samesite="Lax")
#         return resp

#     except Exception as e:
#         logging.error(f"Seller login error: {e}")
#         return jsonify({"error": "Server error"}), 500

# ---------- Buyer Registration ----------
@app.route("/register/buyer", methods=["POST"])
def signup_buyer():
    try:
        data = request.get_json()
        full_name = data.get("fullName")
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")

        if not all([full_name, email, phone, password]):
            return jsonify({"error": "All fields required"}), 400

        if buyers_collection.find_one({"email": email}):
            return jsonify({"error": "Email already in use"}), 400

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = {
            "fullName": full_name,
            "email": email,
            "phone": phone,
            "password": hashed_password,
        }
        buyers_collection.insert_one(new_user)

        access_token = create_access_token(identity=email, expires_delta=timedelta(days=1))
        cookie_expiry = timedelta(hours=1)
        resp = jsonify({"message": "Registration successful", "redirect": f"{base_url}/home"})
        set_access_cookies(resp, access_token, max_age=cookie_expiry)
        return resp

    except Exception as e:
        logging.error(f"Buyer registration error: {e}")
        return jsonify({"error": "Server error"}), 500

# # ---------- Seller Registration ----------
# @app.route("/register/seller", methods=["POST"])
# def signup_seller():
#     try:
#         data = request.get_json()
#         store_name = data.get("storeName")
#         email = data.get("email")
#         phone = data.get("phone")
#         password = data.get("password")

#         if not all([store_name, email, phone, password]):
#             return jsonify({"error": "All fields required"}), 400

#         if sellers_info.find_one({"email": email}):
#             return jsonify({"error": "Email already in use"}), 400

#         hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
#         new_seller = {
#             "storeName": store_name,
#             "email": email,
#             "phone": phone,
#             "password": hashed_password,
#         }
#         sellers_info.insert_one(new_seller)

#         access_token = create_access_token(
#             identity=email, expires_delta=timedelta(hours=1)
#         )
#         cookie_expiry = timedelta(hours=1)
#         resp = jsonify({"message": "Registration successful", "redirect": "/home"})
#         set_access_cookies(resp, access_token, max_age=cookie_expiry)
#         return resp

#     except Exception as e:
#         logging.error(f"Seller registration error: {e}")
#         return jsonify({"error": "Server error"}), 500

# ---------- User Location and Nearby sellers ----------
@app.route("/get-user-location", methods=["GET"])
@jwt_required()
def get_user_location():
    try:
        user_email = get_jwt_identity()

        user_data = buyers_collection.find_one({"email": user_email})
        if not user_data:
            user_data = sellers_info.find_one({"email": user_email})

        if not user_data:
            return jsonify({"error": "User not found"}), 404

        last_location = user_data.get("last_location")

        if last_location and "lat" in last_location and "lon" in last_location:
            response_data = {
                "location": {"lat": last_location["lat"], "lon": last_location["lon"]}
            }

            if "address" in last_location:
                response_data["location"]["address"] = last_location["address"]

            return jsonify(response_data), 200
        else:
            return jsonify({"message": "No location found"}), 404

    except Exception as e:
        logging.error(f"Get user location error: {e}")
        return jsonify({"error": "Server error"}), 500


# Update the save-location route to also save address
@app.route("/save-location", methods=["POST"])
@jwt_required()
def save_location():
    try:
        user_email = get_jwt_identity()
        data = request.get_json()
        lat = data.get("lat")
        lon = data.get("lon")
        address = data.get("address")

        if not lat or not lon:
            return jsonify({"error": "Location data required"}), 400

        location_data = {"lat": lat, "lon": lon}
        if address:
            location_data["address"] = address

        if buyers_collection.find_one({"email": user_email}):
            buyers_collection.update_one(
                {"email": user_email}, {"$set": {"last_location": location_data}}
            )
        else:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "Location saved successfully"}), 200

    except Exception as e:
        logging.error(f"Location save error: {e}")
        return jsonify({"error": "Failed to save location"}), 500


# location distance calculation
def haversine(lat1, lon1, lat2, lon2):
    """Calculate the distance between two points on Earth."""
    R = 6371.0  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    c = 2 * asin(sqrt(a))
    return R * c


@app.route("/get-sellers-nearby", methods=["POST"])
@jwt_required()
def get_sellers_nearby():
    try:
        data = request.get_json()
        # print(f"DEBUG: Received user location: {data}")
        user_lat = float(data["lat"])
        user_lon = float(data["lon"])

        # Query: Check for latitude and longitude fields
        query = {
    "latitude": {"$exists": True, "$ne": None},
    "longitude": {"$exists": True, "$ne": None}
        }

        # print(f"DEBUG: MongoDB Query: {query}")

        # Fetch sellers from DB
        all_sellers = list(sellers_info.find(query))
        # print(f"DEBUG: Found {len(all_sellers)} sellers with coordinates.")

        nearby_sellers = []
        for seller in all_sellers:
            try:
                seller_lat = float(seller["latitude"])
                seller_lon = float(seller["longitude"])

                # Calculate distance between user and seller
                dist = haversine(user_lat, user_lon, seller_lat, seller_lon)
                search_radius_km = 10  # km
                if dist <= search_radius_km:
                    nearby_seller_data = {
                        "id": str(seller["_id"]),
                        "storeName": seller.get("name", "Unnamed Store"),
                        "lat": seller_lat,
                        "lon": seller_lon,
                        "distance": round(dist, 2),
                        "rating": seller.get("rating", 4.5),
                        "description": seller.get("description", ""),
                    }
                    nearby_sellers.append(nearby_seller_data)
            except (ValueError, TypeError) as e:
                print(
                    f"DEBUG: Skipping seller '{seller.get('name')}' due to invalid latitude/longitude: {e}"
                )
                continue

        # Sort by distance
        print(f"DEBUG: Found {len(nearby_sellers)} nearby sellers.")
        nearby_sellers.sort(key=lambda x: x["distance"])

        return jsonify({"sellers": nearby_sellers})

    except Exception as e:
        logging.error(f"Error in get_sellers_nearby: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500


# # get sellers
# @app.route("/sellers", methods=["GET"])
# @jwt_required()
# def get_sellers():
#     sellers = list(sellers_info.find({}, {"_id": 0}))
#     return jsonify(sellers=sellers)


# ---------- Logout ----------
@app.route("/logout", methods=["POST", "GET"])
def logout():
    try:
        resp = jsonify({"message": "Logged out successfully", "redirect": "/"})
        unset_jwt_cookies(resp)
        resp.delete_cookie("access_token")
        return resp
    except Exception as e:
        logging.error(f"Logout error: {e}")
        return jsonify({"error": "Logout failed"}), 500


# ------------------ Fake Payments -----------------------------
DELIVERY_FEE = 20

def process_fake_payment_result(order_id, user_id, was_successful):
    if was_successful:
        orders_collection.update_one(
            {"_id": ObjectId(order_id), "status": "Awaiting Payment"},
            {"$set": {"status": "Pending"}},
        )
        carts_collection.update_one(
            {"buyer_id": user_id, "status": "active"}, {"$set": {"status": "completed"}}
        )
        logging.info(f"✅ FAKE-WEBHOOK: Order {order_id} marked as Pending.")
    else:
        orders_collection.update_one(
            {"_id": ObjectId(order_id)}, {"$set": {"status": "Payment Failed"}}
        )
        logging.info(f"❌ FAKE-WEBHOOK: Order {order_id} marked as failed.")

# fake payment
@app.route("/fake_payment/initiate", methods=["POST"])
@jwt_required()
def initiate_fake_payment():
    try:
        user_email = get_jwt_identity()
        user = buyers_collection.find_one({"email": user_email})
        if not user:
            return jsonify({"error": "User not found"}), 404

        cart = carts_collection.find_one({"buyer_id": user["_id"], "status": "active"})
        if not cart or not cart.get("items"):
            return jsonify({"error": "Your cart is empty."}), 400

        sellers_orders = {}
        for item in cart.get("items", []):
            seller_id = item.get("seller_id")
            if not seller_id:
                continue
            if seller_id not in sellers_orders:
                sellers_orders[seller_id] = {"items": [], "subtotal": 0.0}
            sellers_orders[seller_id]["items"].append(item)
            sellers_orders[seller_id]["subtotal"] += item.get("price", 0) * item.get("quantity", 1)

        if not sellers_orders:
            return jsonify({"error": "No valid items in cart to process."}), 400

        created_order_ids = []
        user_info_for_seller = {
            "buyer_id": user["_id"],
            "name": user.get("fullName", "N/A"),
            "email": user.get("email"),
            "phone": user.get("phone", "N/A"),
            "address": user.get("last_location", {}).get("address", "Address not provided")
        }

        for seller_id, order_data in sellers_orders.items():
            total_for_this_seller = order_data['subtotal'] + DELIVERY_FEE
            new_order = {
                "order_id": f"KS{int(time.time())}-{random.randint(100, 999)}",
                "seller_id": ObjectId(seller_id),
                "buyer_info": user_info_for_seller,
                "items": order_data["items"],
                "total_amount": total_for_this_seller,
                "status": "Awaiting Payment",
                "order_date": datetime.now(timezone.utc),
            }
            result = orders_collection.insert_one(new_order)
            created_order_ids.append(result.inserted_id)

        logging.info(f"⏳ FAKE-PAYMENT: Processing payment for {len(created_order_ids)} sub-orders.")
        time.sleep(2)
        payment_succeeded = random.random() < 0.9

        if payment_succeeded:
            orders_collection.update_many(
                {"_id": {"$in": created_order_ids}},
                {"$set": {"status": "Pending"}}
            )
            carts_collection.update_one(
                {"_id": cart["_id"]}, {"$set": {"status": "completed"}}
            )
            logging.info(f"✅ FAKE-PAYMENT: SUCCESS for orders: {created_order_ids}")
            return jsonify({
                "message": "Payment Successful! Your order has been placed with each seller.",
                "success": True,
                "redirect": "/myorders"
            })
        else:
            orders_collection.update_many(
                {"_id": {"$in": created_order_ids}},
                {"$set": {"status": "Payment Failed"}}
            )
            logging.info(f"❌ FAKE-PAYMENT: FAILED for orders: {created_order_ids}")
            return jsonify({
                "error": "Payment Failed. Please try again.",
                "success": False,
            }), 400

    except Exception as e:
        logging.error(f"Error in fake payment initiation: {e}", exc_info=True)
        return jsonify({"error": "An internal server error occurred."}), 500

# -------------------------- ORDER MANAGEMENT --------------------------------
@app.route("/order/create", methods=["POST"])
@jwt_required()
def create_order():
    try:
        user_email = get_jwt_identity()
        user = buyers_collection.find_one({"email": user_email})
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Find the user's active cart
        cart = carts_collection.find_one({"buyer_id": user["_id"], "status": "active"})
        if not cart or not cart.get("items"):
            return jsonify({"error": "Your cart is empty."}), 400

        # Get payment method from the frontend request
        data = request.get_json()
        payment_method = data.get("payment_method", "Not Specified")

        # --- IMPORTANT: Recalculate total on the server to prevent manipulation ---
        subtotal = sum(item["price"] * item["quantity"] for item in cart["items"])
        delivery_fee = 20.00  # Your standard delivery fee
        total_amount = subtotal + delivery_fee

        # Create the new order document
        new_order = {
            "order_id": f"KS{int(datetime.now(timezone.utc).timestamp())}",  # Simple unique ID
            "buyer_id": user["_id"],
            "buyer_name": user.get("fullName", "Unknown"),  # Get buyer's name
            "items": cart["items"],
            "item_count": sum(item["quantity"] for item in cart["items"]),
            "total_amount": total_amount,
            "payment_method": payment_method,
            "status": "Pending",  # Default status for a new order
            "order_date": datetime.now(timezone.utc),
        }
        orders_collection.insert_one(new_order)

        # Mark the cart as "completed" so it's no longer active
        carts_collection.update_one(
            {"_id": cart["_id"]}, {"$set": {"status": "completed"}}
        )

        # Respond with success and where to redirect the user
        return (
            jsonify({"message": "Order placed successfully!", "redirect": "/myorders"}),
            201,
        )  # 201 = Created

    except Exception as e:
        logging.error(f"Error creating order: {e}", exc_info=True)
        return jsonify({"error": "Server error while creating order"}), 500

# helper function
def convert_mongo_types(obj):
    if isinstance(obj, list):
        return [convert_mongo_types(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: convert_mongo_types(v) for k, v in obj.items()}
    elif isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.strftime("%d/%m/%Y")
    else:
        return obj

# order get
@app.route("/orders/get", methods=["GET"])
@jwt_required()
def get_my_orders():
    try:
        user_email = get_jwt_identity()
        user = buyers_collection.find_one({"email": user_email})
        if not user:
            return jsonify({"error": "User not found"}), 404

        orders_cursor = orders_collection.find({"buyer_id": user["_id"]}).sort(
            "order_date", -1
        )
        orders_list = []
        for order in orders_cursor:
            order = convert_mongo_types(order)
            orders_list.append(order)

        return jsonify(orders=orders_list), 200

    except Exception as e:
        logging.error(f"Error fetching orders: {e}", exc_info=True)
        return jsonify({"error": "Server error while fetching orders"}), 500

if __name__ == "__main__":
    app.run(debug=True)
