# sellers_dashboard.py
from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo import MongoClient
import logging

# Create a Blueprint for seller dashboard routes
sellers_dashboard_bp = Blueprint("sellers_dashboard", __name__)

try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ksheeram"]
    sellers_collection = db["sellers"]
    print("Connected to MongoDB in sellers_dashboard.py")
except Exception as e:
    logging.error(f"MongoDB Error: {e}")
    raise SystemExit("DB connection failed.")


@sellers_dashboard_bp.route("/seller/save-location", methods=["POST"])
@jwt_required()
def save_location():
    try:
        seller_email = get_jwt_identity()
        data = request.get_json()
        address = data.get("address")
        pincode = data.get("pincode")

        location_data = {"address": address, "pincode": pincode}

        result = sellers_collection.update_one(
            {"email": seller_email}, {"$set": {"address": location_data}}
        )

        if result.matched_count == 0:
            return {"error": "Seller not found"}, 404

        return {"message": "Location saved successfully"}, 200

    except Exception as e:
        return {"error": f"Failed to save location: {str(e)}"}, 500


# Route to view seller profile
@sellers_dashboard_bp.route("/profile", methods=["GET"])
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
@sellers_dashboard_bp.route("/profile/update", methods=["POST"])
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
            {"email": seller_email}, {"$set": update_data}
        )

        if result.modified_count == 0:
            return jsonify({"error": "No changes were made"}), 400

        return jsonify({"message": "Profile updated successfully"}), 200

    except Exception as e:
        logging.error(f"Error in update_profile: {e}")
        return jsonify({"error": "Server error"}), 500


# Add other seller-related routes here (e.g., product management, orders, etc.)
# In sellers_dashboard.py


@sellers_dashboard_bp.route("/orders", methods=["GET"])
@jwt_required()
def get_seller_orders():
    """
    Fetches all orders that contain at least one item from this seller.
    """
    try:
        seller_email = get_jwt_identity()  # Get seller's email from JWT token
        seller_account = sellers_collection.find_one(
            {"email": seller_email}
        )  # Get seller details
        if not seller_account:
            return jsonify({"error": "Seller account not found"}), 404

        seller_profile = sellers_info_collection.find_one(
            {"owner_email": seller_email}
        )  # Get seller's profile
        if not seller_profile:
            return (
                jsonify({"error": "Seller profile not found. Cannot fetch orders."}),
                404,
            )

        seller_id_str = str(seller_profile["_id"])  # Get seller ID for filtering orders

        # Query to find orders where any item in the 'items' array has the matching seller_id
        pipeline = [
            # Unwind the items array to process each item individually
            {"$unwind": "$items"},
            # Match documents where the item's seller_id is the one we're looking for
            {"$match": {"items.seller_id": seller_id_str}},
            # Group back to the original order structure, but only with items from this seller
            {
                "$group": {
                    "_id": "$_id",
                    "order_id": {"$first": "$order_id"},
                    "buyer_name": {"$first": "$buyer_name"},
                    "order_date": {"$first": "$order_date"},
                    "status": {"$first": "$status"},
                    "seller_items": {"$push": "$items"},
                }
            },
            # Add a field for the total value of items for this seller in this order
            {
                "$addFields": {
                    "seller_total": {
                        "$sum": {
                            "$multiply": [
                                "$seller_items.price",
                                "$seller_items.quantity",
                            ]
                        }
                    },
                    "seller_item_count": {"$sum": "$seller_items.quantity"},
                }
            },
            # Sort by date, newest first
            {"$sort": {"order_date": -1}},
        ]

        seller_orders = list(
            orders_collection.aggregate(pipeline)
        )  # Fetch seller-specific orders using aggregation pipeline

        # Convert ObjectId and datetime for JSON serialization
        for order in seller_orders:
            order["_id"] = str(order["_id"])
            if isinstance(order["order_date"], datetime):
                order["order_date"] = order["order_date"].isoformat()

        return jsonify(orders=seller_orders), 200  # Return the filtered orders

    except Exception as e:
        logging.error(f"Error fetching seller orders: {e}", exc_info=True)
        return jsonify({"error": "Server error while fetching orders"}), 500
