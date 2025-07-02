# sellers_dashboard.py
from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo import MongoClient
import logging

# Create a Blueprint for seller dashboard routes
sellers_dashboard_bp = Blueprint('sellers_dashboard', __name__)

try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client['ksheeram']
    sellers_collection = db["sellers"]
    print("Connected to MongoDB in sellers_dashboard.py")
except Exception as e:
    logging.error(f"MongoDB Error: {e}")
    raise SystemExit("DB connection failed.")



@sellers_dashboard_bp.route('/seller/save-location', methods=['POST'])
@jwt_required()
def save_location():
    try:
        seller_email = get_jwt_identity()
        data = request.get_json()
        address = data.get("address")
        pincode = data.get("pincode")
        
        location_data = {"address": address, "pincode": pincode}
        
        # Update the seller document where email matches
        result = sellers_collection.update_one(
            {"email": seller_email},
            {"$set": {"address": location_data}}
        )
        
        if result.matched_count == 0:
            return {"error": "Seller not found"}, 404
        
        return {"message": "Location saved successfully"}, 200

    except Exception as e:
        return {"error": f"Failed to save location: {str(e)}"}, 500


# Route to view seller profile
@sellers_dashboard_bp.route('/profile', methods=['GET'])
@jwt_required()
def view_profile():
    try:
        seller_email = get_jwt_identity()
        seller = sellers_collection.find_one({"email": seller_email})

        if not seller:
            return jsonify({"error": "Seller not found"}), 404

        return render_template("seller_profile.html", seller=seller)

    except Exception as e:
        logging.error(f"Error in view_profile: {e}")
        return jsonify({"error": "Server error"}), 500

# Route to update seller profile
@sellers_dashboard_bp.route('/profile/update', methods=['POST'])
@jwt_required()
def update_profile():
    try:
        seller_email = get_jwt_identity()
        data = request.get_json()
        store_name = data.get("storeName")
        phone = data.get("phone")

        if not store_name or not phone:
            return jsonify({"error": "Store name and phone are required"}), 400

        update_data = {"storeName": store_name, "phone": phone}

        
        result = sellers_collection.update_one(
            {"email": seller_email},
            {"$set": update_data}
        )

        if result.modified_count == 0:
            return jsonify({"error": "No changes were made"}), 400

        return jsonify({"message": "Profile updated successfully"}), 200

    except Exception as e:
        logging.error(f"Error in update_profile: {e}")
        return jsonify({"error": "Server error"}), 500

# Add other seller-related routes here (e.g., product management, orders, etc.)
