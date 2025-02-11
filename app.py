from flask import Flask, render_template, jsonify, request

from datetime import datetime

app = Flask(__name__)


phones = [
    {
        "brand": "Samsung",
        "model": "Galaxy S23 Ultra",
        "price": 124999,
        "image": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?auto=format&fit=crop&w=500&q=80",
        "specs": {
            "ram": "12GB",
            "storage": "256GB",
            "camera": "200MP + 12MP + 10MP + 10MP",
            "battery": "5000mAh"
        },
        "colors": ["Phantom Black", "Cream", "Green", "Lavender"],
        "category": "Flagship"
    },
    {
        "brand": "iPhone",
        "model": "14 Pro Max",
        "price": 139900,
        "image": "https://images.unsplash.com/photo-1678685888221-cda773a3dcdb?auto=format&fit=crop&w=500&q=80",
        "specs": {
            "ram": "6GB",
            "storage": "256GB",
            "camera": "48MP + 12MP + 12MP",
            "battery": "4323mAh"
        },
        "colors": ["Deep Purple", "Gold", "Silver", "Space Black"],
        "category": "Flagship"
    },
    {
        "brand": "OnePlus",
        "model": "11",
        "price": 61999,
        "image": "https://m.media-amazon.com/images/I/414+xRBltFL.jpg",
        "specs": {
            "ram": "16GB",
            "storage": "256GB",
            "camera": "50MP + 48MP + 32MP",
            "battery": "5000mAh"
        },
        "colors": ["Titan Black", "Eternal Green"],
        "category": "Flagship"
    },
    {
        "brand": "Google",
        "model": "Pixel 7 Pro",
        "price": 84999,
        "image": "https://lh3.googleusercontent.com/V1_LJMXjWyuQ6-fZBtnMS2bYH-CiZbKfe3JlMOJEOiiXaeKugc3AtDpF2E_WFhTGAP-_Xlv1GHqtmYART_9dUeM148ZRFdrlKGs=rw-e365-nu-w525",
        "specs": {
            "ram": "12GB",
            "storage": "128GB",
            "camera": "50MP + 12MP + 48MP",
            "battery": "5000mAh"
        },
        "colors": ["Obsidian", "Snow", "Hazel"],
        "category": "Flagship"
    },
    {
        "brand": "Realme",
        "model": "GT Neo 3",
        "price": 29999,
        "image": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=500&q=80",
        "specs": {
            "ram": "8GB",
            "storage": "128GB",
            "camera": "50MP + 8MP + 2MP",
            "battery": "5000mAh"
        },
        "colors": ["Nitro Blue", "Sprint White", "Asphalt Black"],
        "category": "Mid-range"
    },
    {
        "brand": "Nothing",
        "model": "Phone 2",
        "price": 44999,
        "image": "https://in.nothing.tech/cdn/shop/files/12Image_1280x1020_a11e1bb0-7ace-47b6-a8ad-ae34c33c5314_2160x.png?v=1658151576",
        "specs": {
            "ram": "12GB",
            "storage": "256GB",
            "camera": "50MP + 50MP",
            "battery": "4700mAh"
        },
        "colors": ["White", "Dark Grey"],
        "category": "Mid-range"
    }
]

@app.route("/")
def home():
    return render_template("index.html", phones=phones)

@app.route("/phones")
def get_phones():
    return jsonify(phones)

@app.route("/purchase", methods=["POST"])
def purchase():
    try:
        data = request.get_json()
        # Input validation
        required_fields = ["name", "phone_number", "choice", "color"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        choice = int(data.get("choice", 0)) - 1
        if choice < 0 or choice >= len(phones):
            return jsonify({"error": "Invalid phone selection"}), 400
        # Phone number validation
        if not data["phone_number"].isdigit() or len(data["phone_number"]) != 10:
            return jsonify({"error": "Invalid phone number"}), 400
        phone = phones[choice]
        # Color validation
        if data["color"] not in phone["colors"]:
            return jsonify({"error": "Invalid color selection"}), 400
        # Calculate price with GST (18%)
        original_price = phone["price"]
        gst_amount = original_price * 0.18
        total_with_gst = original_price + gst_amount
        # Apply discount if provided
        discount = min(max(float(data.get("discount", 0)), 0), 100)
        discount_amount = total_with_gst * (discount / 100)
        final_price = total_with_gst - discount_amount
        # Generate bill number (timestamp-based)
        bill_number = f"BILL-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        response = {
            "bill_number": bill_number,
            "customer": data["name"],
            "phone_number": data["phone_number"],
            "phone": f"{phone['brand']} {phone['model']}",
            "color": data["color"],
            "specs": phone["specs"],
            "price_details": {
                "base_price": original_price,
                "gst_amount": round(gst_amount, 2),
                "total_with_gst": round(total_with_gst, 2),
                "discount_percentage": discount,
                "discount_amount": round(discount_amount, 2),
                "final_price": round(final_price, 2)
            },
            "purchase_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
