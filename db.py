import os
import time
import requests
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

AZURE_SUBSCRIPTION_KEY = os.getenv("AZURE_SUBSCRIPTION_KEY")

client = MongoClient("mongodb://localhost:27017/")
db = client["ksheeram"]
collection = db["sellersinfo"]

# Sample seller data (abbreviated for brevity)
dairy_data =[
  {
    "name": "Amul Dairy Delights",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Anand, Gujarat",
    "description": "Your trusted source for pure and fresh dairy products for over 75 years. We bring health and happiness to every home.",
    "owner": "Tribhuvandas Patel",
    "address": "Amul Dairy Road, Anand 388001, Gujarat, India",
    "rating": 4.8,
    "latitude": 22.5645,
    "longitude": 72.9288,
    "plans": [
      {
        "name": "Family Milk Plan",
        "price": "₹1500 / month",
        "features": [
          "1L Toned Milk Daily",
          "Free delivery before 7 AM",
          "Pause subscription anytime"
        ],
        "description": "Perfect for a family of four. Never run out of fresh milk for your morning coffee and breakfast."
      },
      {
        "name": "Premium Ghee & Curd Plan",
        "price": "₹950 / month",
        "features": [
          "500g Pure Cow Ghee",
          "1kg Fresh Curd Weekly",
          "Priority delivery"
        ],
        "description": "Get the essentials for a healthy Indian kitchen delivered to your doorstep every week."
      }
    ],
    "products": [
      {
        "name": "Fresh Paneer",
        "price": "120",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Fresh+Paneer"
      },
      {
        "name": "Amul Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Amul+Butter"
      },
      {
        "name": "Masti Dahi (Curd)",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Masti+Dahi+(Curd)"
      }
    ]
  },
  {
    "name": "Anand Dairy Farm",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Bhimavaram, Andhra Pradesh",
    "description": "Distributor of milk powder, cow ghee, butter.",
    "owner": "Mr. Anil Kumar",
    "address": "14-89 PP Road, Narasimhapuram, Bhimavaram, 534206",
    "rating": 4.1,
    "latitude": 16.5445,
    "longitude": 81.5213,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk Powder",
        "price": "250",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk+Powder"
      },
      {
        "name": "Cow Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Cow+Ghee"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      },
      {
        "name": "Cookies",
        "price": "50",
        "unit": "pack",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Cookies"
      }
    ]
  },
  {
    "name": "Annapurna Milk Corner",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Bhimavaram, Andhra Pradesh",
    "description": "Milk and dairy essentials corner.",
    "owner": "Unknown",
    "address": "Near Bus Stand, Bhimavaram, 534201",
    "rating": 4.5,
    "latitude": 16.5445,
    "longitude": 81.5213,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Amrutha Milk & Ghee Shop",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Bhimavaram, Andhra Pradesh",
    "description": "Known for quality milk and ghee.",
    "owner": "Unknown",
    "address": "Commercial Complex, Bhimavaram, 534201",
    "rating": 4.8,
    "latitude": 16.5445,
    "longitude": 81.5213,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      },
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      }
    ]
  },
  {
    "name": "Bhavani Milk Corner",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Bhimavaram, Andhra Pradesh",
    "description": "Local favorite for milk and curd.",
    "owner": "Unknown",
    "address": "Station Road, Bhimavaram, 534201",
    "rating": 4.2,
    "latitude": 16.5445,
    "longitude": 81.5213,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "City Dairy Hub",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Bhimavaram, Andhra Pradesh",
    "description": "Modern dairy hub with packaged milk.",
    "owner": "Unknown",
    "address": "Market Road, Bhimavaram, 534201",
    "rating": 3.9,
    "latitude": 16.5445,
    "longitude": 81.5213,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Packaged Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Packaged+Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      }
    ]
  },
  {
    "name": "Ganesh Dairy Farm",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Bhimavaram, Andhra Pradesh",
    "description": "Supplier and trader of cow milk, ghee, butter.",
    "owner": "Mr. Gubbala Ganesh",
    "address": "6-52 Doddipatla Road, Palakollu, Bhimavaram, 534260",
    "rating": 4.6,
    "latitude": 16.5445,
    "longitude": 81.5213,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Cow Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Cow+Milk"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      }
    ]
  },
  {
    "name": "Hari Dairy Products",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Bhimavaram, Andhra Pradesh",
    "description": "Fresh dairy products for households.",
    "owner": "Unknown",
    "address": "Temple Street, Bhimavaram, 534201",
    "rating": 4.0,
    "latitude": 16.5445,
    "longitude": 81.5213,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      }
    ]
  },
  {
    "name": "Haritha Dairy Shop",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Bhimavaram, Andhra Pradesh",
    "description": "Dairy shop offering fresh milk and curd.",
    "owner": "Unknown",
    "address": "Govt. Hospital Road, Bhimavaram, 534201",
    "rating": 4.4,
    "latitude": 16.5445,
    "longitude": 81.5213,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Lakshmi Dairy Store",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Bhimavaram, Andhra Pradesh",
    "description": "Store offering supermarket dairy items.",
    "owner": "Unknown",
    "address": "Powerpet Road, Bhimavaram, 534201",
    "rating": 3.7,
    "latitude": 16.5445,
    "longitude": 81.5213,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      }
    ]
  },
  {
    "name": "Padmavathi Milk Shop",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Bhimavaram, Andhra Pradesh",
    "description": "Paneer & curd specialists with daily milk.",
    "owner": "Unknown",
    "address": "Panduranga Colony, Bhimavaram, 534201",
    "rating": 4.1,
    "latitude": 16.5445,
    "longitude": 81.5213,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      }
    ]
  },
  {
    "name": "Sai Milk Parlour",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Bhimavaram, Andhra Pradesh",
    "description": "Local parlour serving fresh milk & curd.",
    "owner": "Unknown",
    "address": "Dowleswaram Road, Bhimavaram, 534201",
    "rating": 3.9,
    "latitude": 16.5445,
    "longitude": 81.5213,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Sri Vijaya Co-op Dairy",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Bhimavaram, Andhra Pradesh",
    "description": "Local cooperative dairy selling milk & butter.",
    "owner": "Co-operative Society",
    "address": "Undi Road, Bhimavaram, 534201",
    "rating": 4.2,
    "latitude": 16.5445,
    "longitude": 81.5213,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Sri Vijaya Durga Dairy Farm",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Bhimavaram, Andhra Pradesh",
    "description": "Supplier of milk powder, ghee, butter, cookies.",
    "owner": "Mr. Siva Sankar",
    "address": "Ullamparru Village, Palakollu Road, Bhimavaram, 534265",
    "rating": 4.5,
    "latitude": 16.5445,
    "longitude": 81.5213,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk Powder",
        "price": "250",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk+Powder"
      },
      {
        "name": "Cow Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Cow+Ghee"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      },
      {
        "name": "Cookies",
        "price": "50",
        "unit": "pack",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Cookies"
      }
    ]
  },
  {
    "name": "Suman Co-op Milk Booth",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Bhimavaram, Andhra Pradesh",
    "description": "Milk booth under co‑op network.",
    "owner": "Unknown",
    "address": "Main Street, Bhimavaram, 534201",
    "rating": 4.0,
    "latitude": 16.5445,
    "longitude": 81.5213,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Suman Milk Dairy",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Bhimavaram, Andhra Pradesh",
    "description": "Booth offering fresh milk to local residents.",
    "owner": "Unknown",
    "address": "Somavaram, Gandhi Nagar, Bhimavaram, 534201",
    "rating": 3.8,
    "latitude": 16.5445,
    "longitude": 81.5213,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Vijaya Dairy Parlour",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Bhimavaram, Andhra Pradesh",
    "description": "Local milk parlour in Gandhi Nagar.",
    "owner": "Unknown",
    "address": "PP Road, Gandhi Nagar, Bhimavaram, 534201",
    "rating": 4.3,
    "latitude": 16.5445,
    "longitude": 81.5213,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Visakha Teja Milk Dairy",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Bhimavaram, Andhra Pradesh",
    "description": "Milk dairy booth serving local colonies.",
    "owner": "Unknown",
    "address": "Shop No 1, Balusumoodi, Bhimavaram, 534201",
    "rating": 4.1,
    "latitude": 16.5445,
    "longitude": 81.5213,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      }
    ]
  },
  {
    "name": "Yashwant Dairy",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Bhimavaram, Andhra Pradesh",
    "description": "Retailer of cow milk, pasteurized offers.",
    "owner": "Mr. Kalidindi Raghu Sita Rama Raju",
    "address": "ASR Nagar, Bhimavaram, 534202",
    "rating": 4.0,
    "latitude": 16.5445,
    "longitude": 81.5213,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Cow Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Cow+Milk"
      }
    ]
  },
  {
    "name": "Dodla Milk Dairy",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Jangareddygudem, Andhra Pradesh",
    "description": "Farm‑fresh dairy essentials booth.",
    "owner": "Dodla Dairy",
    "address": "Shop No 1, Main Road, Jangareddygudem, 534447",
    "rating": 4.5,
    "latitude": 17.119,
    "longitude": 81.293,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      }
    ]
  },
  {
    "name": "Eswari Dairy Hub",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Jangareddygudem, Andhra Pradesh",
    "description": "Cheese, dairy and eggs outlet.",
    "owner": "Unknown",
    "address": "47CR+XCX, Jangareddygudem, 534447",
    "rating": 4.1,
    "latitude": 17.119,
    "longitude": 81.293,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Cheese",
        "price": "100",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Cheese"
      },
      {
        "name": "Eggs",
        "price": "72",
        "unit": "dozen",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Eggs"
      }
    ]
  },
  {
    "name": "Eswari Milk Center",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Jangareddygudem, Andhra Pradesh",
    "description": "Local milk and dairy stall.",
    "owner": "Unknown",
    "address": "Aswaraopeta–Jangareddygudem Rd, 534447",
    "rating": 3.9,
    "latitude": 17.119,
    "longitude": 81.293,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Krishna Milk",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Jangareddygudem, Andhra Pradesh",
    "description": "Local dairy vendor with fresh dairy produce.",
    "owner": "Unknown",
    "address": "Mysannagudem Road, Jangareddygudem, 534447",
    "rating": 4.2,
    "latitude": 17.119,
    "longitude": 81.293,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      }
    ]
  },
  {
    "name": "Lakshmi Milk Store",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Jangareddygudem, Andhra Pradesh",
    "description": "Dairy store near medical establishments.",
    "owner": "Unknown",
    "address": "Buttayagudem Road, Jangareddygudem, 534448",
    "rating": 4.0,
    "latitude": 17.119,
    "longitude": 81.293,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      }
    ]
  },
  {
    "name": "Model Milk Products & Ice Cream Parlour",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Jangareddygudem, Andhra Pradesh",
    "description": "Milk booth with ice‑cream parlour attached.",
    "owner": "Unknown",
    "address": "Buttayagudem Road, Jangareddygudem, 534448",
    "rating": 4.3,
    "latitude": 17.119,
    "longitude": 81.293,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Ice Cream",
        "price": "50",
        "unit": "scoop",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ice+Cream"
      }
    ]
  },
  {
    "name": "Mounika Dairy Stall",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Jangareddygudem, Andhra Pradesh",
    "description": "Milk booth beside local medical store.",
    "owner": "Unknown",
    "address": "Jangareddygudem Buttayagudem Road, 534448",
    "rating": 3.7,
    "latitude": 17.119,
    "longitude": 81.293,
    "plans": [],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      }
    ]
  },
  {
    "name": "Raithu Dairy Stall",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Jangareddygudem, Andhra Pradesh",
    "description": "Local dairy stall with milk & eggs.",
    "owner": "Unknown",
    "address": "Aswaraopeta–Jangareddygudem Rd, 534447",
    "rating": 3.8,
    "latitude": 17.119,
    "longitude": 81.293,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Eggs",
        "price": "72",
        "unit": "dozen",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Eggs"
      }
    ]
  },
  {
    "name": "Sri Hanuman Sharma Milk Booth",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Jangareddygudem, Andhra Pradesh",
    "description": "Small dairy stall offering milk.",
    "owner": "Unknown",
    "address": "Jangareddygudem Buttayagudem Road, 534448",
    "rating": 3.8,
    "latitude": 17.119,
    "longitude": 81.293,
    "plans": [],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      }
    ]
  },
  {
    "name": "Sri Ramachandra Milk Products",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Jangareddygudem, Andhra Pradesh",
    "description": "Registered dairy product provider.",
    "owner": "Sri Ramachandra Agri & Milk Products Ltd",
    "address": "10-2-67 Ramachandra Residency, Subbampeta Road, 534447",
    "rating": 4.4,
    "latitude": 17.119,
    "longitude": 81.293,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Milk Powder",
        "price": "250",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk+Powder"
      }
    ]
  },
  {
    "name": "Sri Sitarama Milk Dairy",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Jangareddygudem, Andhra Pradesh",
    "description": "Rural dairy stall supplying milk & curd.",
    "owner": "Unknown",
    "address": "Mysannagudem Road, Jangareddygudem, 534447",
    "rating": 4.0,
    "latitude": 17.119,
    "longitude": 81.293,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Sri Sriramadurga Milk Booth",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Jangareddygudem, Andhra Pradesh",
    "description": "Dairy stall near main road.",
    "owner": "Unknown",
    "address": "Buttayagudem Road, Jangareddygudem, 534448",
    "rating": 3.7,
    "latitude": 17.119,
    "longitude": 81.293,
    "plans": [],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Upland Milk Dairy Farmers Producer Co Ltd",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Jangareddygudem, Andhra Pradesh",
    "description": "Private dairy farmer producer company.",
    "owner": "Upland Milk Dairy Producer Co",
    "address": "H.No.4‑31, Perampeta, Jangareddygudem Mandal, 534447",
    "rating": 4.6,
    "latitude": 17.119,
    "longitude": 81.293,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      }
    ]
  },
  {
    "name": "Vallabha Milk Products",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Jangareddygudem, Andhra Pradesh",
    "description": "Cheese, dairy and milk vendor.",
    "owner": "Unknown",
    "address": "Aswaraopeta–Jangareddygudem Rd, 534447",
    "rating": 4.4,
    "latitude": 17.119,
    "longitude": 81.293,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      },
      {
        "name": "Cheese",
        "price": "100",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Cheese"
      }
    ]
  },
  {
    "name": "Varshini Milk Parlour",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Jangareddygudem, Andhra Pradesh",
    "description": "Cheese & milk booth nearby main road.",
    "owner": "Unknown",
    "address": "Aswaraopeta–Jangareddygudem Rd, 534447",
    "rating": 4.1,
    "latitude": 17.119,
    "longitude": 81.293,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Cheese",
        "price": "100",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Cheese"
      },
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      }
    ]
  },
  {
    "name": "Venkateswara Milk Outlet",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Jangareddygudem, Andhra Pradesh",
    "description": "Retail dairy shop for daily milk needs.",
    "owner": "Unknown",
    "address": "Buttayagudem Road, Jangareddygudem, 534448",
    "rating": 4.2,
    "latitude": 17.119,
    "longitude": 81.293,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Vijaya Dairy Parlour",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Jangareddygudem, Andhra Pradesh",
    "description": "Cheese, dairy and eggs outlet (now closed).",
    "owner": "Unknown",
    "address": "47FR+3W3, Aswaraopeta–Jangareddygudem Rd, 534447",
    "rating": 3.7,
    "latitude": 17.119,
    "longitude": 81.293,
    "plans": [],
    "products": [
      {
        "name": "Cheese",
        "price": "100",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Cheese"
      },
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      }
    ]
  },
  {
    "name": "Vijaya Krishna Dairy Store",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Jangareddygudem, Andhra Pradesh",
    "description": "Local dairy with milk products variety.",
    "owner": "Unknown",
    "address": "Buttayagudem Main Road, Jangareddygudem, 534448",
    "rating": 4.1,
    "latitude": 17.119,
    "longitude": 81.293,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      }
    ]
  },
  {
    "name": "Amma Milk Dairy Farm",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Kakinada, Andhra Pradesh",
    "description": "Local dairy farm producing fresh cow & buffalo milk.",
    "owner": "Amma Milk Dairy Farm",
    "address": "Rangaraya Medical College Backside, Kondayyapalem, Kakinada, 533003",
    "rating": 4.5,
    "latitude": 16.9891,
    "longitude": 82.2475,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Cow Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Cow+Milk"
      },
      {
        "name": "Buffalo Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Buffalo+Milk"
      }
    ]
  },
  {
    "name": "Amogha Milk Farm",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Kakinada, Andhra Pradesh",
    "description": "Genuine, pure, preservative‑free buffalo & cow milk delivered daily.",
    "owner": "Amogha Milk",
    "address": "Local farms across Kakinada, 533003",
    "rating": 4.7,
    "latitude": 16.9891,
    "longitude": 82.2475,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Buffalo Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Buffalo+Milk"
      },
      {
        "name": "Cow Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Cow+Milk"
      }
    ]
  },
  {
    "name": "Amrutha Milk & Dairy",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Kakinada, Andhra Pradesh",
    "description": "Known for quality milk and ghee.",
    "owner": "Unknown",
    "address": "Commercial Complex Near Court, Kakinada, 533003",
    "rating": 4.3,
    "latitude": 16.9891,
    "longitude": 82.2475,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      },
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      }
    ]
  },
  {
    "name": "Annapurna Milk Sellers",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Kakinada, Andhra Pradesh",
    "description": "Local sellers with daily milk delivery.",
    "owner": "Unknown",
    "address": "Balajinagar, Kakinada, 533003",
    "rating": 4.1,
    "latitude": 16.9891,
    "longitude": 82.2475,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Bhavani Dairy Parlour",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Kakinada, Andhra Pradesh",
    "description": "Neighborhood dairy stall serving milk products.",
    "owner": "Unknown",
    "address": "Corner of Jagannadhapuram Road, Kakinada, 533003",
    "rating": 3.9,
    "latitude": 16.9891,
    "longitude": 82.2475,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "City Milk Corner",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Kakinada, Andhra Pradesh",
    "description": "Neighborhood milk booth serving fresh milk packs.",
    "owner": "Unknown",
    "address": "Seethampeta Road, Kakinada, 533004",
    "rating": 4.2,
    "latitude": 16.9891,
    "longitude": 82.2475,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Ganesh Milk Booth",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Kakinada, Andhra Pradesh",
    "description": "Local stall offering milk and curd.",
    "owner": "Unknown",
    "address": "RTC Complex Road, Kakinada, 533003",
    "rating": 4.0,
    "latitude": 16.9891,
    "longitude": 82.2475,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Gopalakrishna Milk Supply & Dairy Farm",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Kakinada, Andhra Pradesh",
    "description": "Local supply & dairy farm in Kakinada region.",
    "owner": "Gopalakrishna Milk Supply",
    "address": "Kakinada, 533003",
    "rating": 4.3,
    "latitude": 16.9891,
    "longitude": 82.2475,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Hari Dairy Hub",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Kakinada, Andhra Pradesh",
    "description": "Modern hub offering fresh and packaged dairy.",
    "owner": "Unknown",
    "address": "Dr. Mamidada Road, Kakinada, 533004",
    "rating": 4.6,
    "latitude": 16.9891,
    "longitude": 82.2475,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Packaged Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Packaged+Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      }
    ]
  },
  {
    "name": "Lakshmi Narayana Milk Agency",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Kakinada, Andhra Pradesh",
    "description": "Local store offering milk and paneer.",
    "owner": "Unknown",
    "address": "Gowthami Canal Road, Kakinada, 533005",
    "rating": 4.2,
    "latitude": 16.9891,
    "longitude": 82.2475,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      }
    ]
  },
  {
    "name": "Narasimha Dairy Store",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Kakinada, Andhra Pradesh",
    "description": "Local supply of milk and butter.",
    "owner": "Unknown",
    "address": "Temple Road, Kakinada, 533004",
    "rating": 3.8,
    "latitude": 16.9891,
    "longitude": 82.2475,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Padmavathi Milk Shop",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Kakinada, Andhra Pradesh",
    "description": "Local store specializing in paneer and curd.",
    "owner": "Ms. Padmavathi",
    "address": "Jagannaickapuram, Kakinada, 533006",
    "rating": 4.1,
    "latitude": 16.9891,
    "longitude": 82.2475,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      }
    ]
  },
  {
    "name": "Sangam Milk Dairy",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Kakinada, Andhra Pradesh",
    "description": "Daily supplier of fresh milk in the Venkateswara Colony area.",
    "owner": "Sangam Milk Dairy",
    "address": "17-24-37/7/C, Dairy Farm Road, Venkateswara Colony, Kakinada, 533001",
    "rating": 4.4,
    "latitude": 16.9891,
    "longitude": 82.2475,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Sri Lakshmi Dairy",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Kakinada, Andhra Pradesh",
    "description": "Well-known for hygienic packed toned milk.",
    "owner": "Unknown",
    "address": "Thimmapuram, Kakinada, 533005",
    "rating": 4.0,
    "latitude": 16.9891,
    "longitude": 82.2475,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Toned Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Toned+Milk"
      },
      {
        "name": "Packaged Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Packaged+Milk"
      }
    ]
  },
  {
    "name": "Sri Sai Milk Parlour",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Kakinada, Andhra Pradesh",
    "description": "Parlour providing fresh milk and dahi.",
    "owner": "Unknown",
    "address": "Opp. SM Valmiki Temple, Kakinada, 533002",
    "rating": 3.9,
    "latitude": 16.9891,
    "longitude": 82.2475,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Vallabha Milk Store",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Kakinada, Andhra Pradesh",
    "description": "Fresh dairy products for households.",
    "owner": "Unknown",
    "address": "Visweswara Rao Nagar, Kakinada, 533003",
    "rating": 4.5,
    "latitude": 16.9891,
    "longitude": 82.2475,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      }
    ]
  },
  {
    "name": "Veda Farms",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Kakinada, Andhra Pradesh",
    "description": "100% original milk; liter priced at ₹80 and delivery across the city.",
    "owner": "Veda Farms",
    "address": "Kakinada (various locations), 533003",
    "rating": 4.8,
    "latitude": 16.9891,
    "longitude": 82.2475,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Pure Milk",
        "price": "40",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Pure+Milk"
      }
    ]
  },
  {
    "name": "Visakha Dairy Parlour",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Kakinada, Andhra Pradesh",
    "description": "Official parlour from Visakha Dairy cooperative.",
    "owner": "Visakha Dairy (Sri Vijaya Visakha Milk Producers Co‑op)",
    "address": "Sarpavaram Junction, Kakinada, 533005",
    "rating": 4.6,
    "latitude": 16.9891,
    "longitude": 82.2475,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      }
    ]
  },
  {
    "name": "Amul Milk Dealer",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Palakollu, Andhra Pradesh",
    "description": "Retail outlet for Amul milk products.",
    "owner": "Amul Co-op Society",
    "address": "Palakollu Bazaar Area, 534260",
    "rating": 4.6,
    "latitude": 16.5333,
    "longitude": 81.7333,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Amul Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Amul+Milk"
      },
      {
        "name": "Amul Butter Milk",
        "price": "20",
        "unit": "200ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Amul+Butter+Milk"
      }
    ]
  },
  {
    "name": "Amrutha Milk & Ghee Shop",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Palakollu, Andhra Pradesh",
    "description": "Known for quality milk and ghee.",
    "owner": "Ms. Unknown",
    "address": "Commercial Complex, Palakollu, 534260",
    "rating": 4.4,
    "latitude": 16.5333,
    "longitude": 81.7333,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      },
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      }
    ]
  },
  {
    "name": "Annapurna Milk Corner",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Palakollu, Andhra Pradesh",
    "description": "Booth with daily fresh milk & curd supply.",
    "owner": "Mrs. Anjali",
    "address": "Opp. RTC Complex, Palakollu, 534260",
    "rating": 4.1,
    "latitude": 16.5333,
    "longitude": 81.7333,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Bhavani Dairy Store",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Palakollu, Andhra Pradesh",
    "description": "Local favorite for milk, curd and butter.",
    "owner": "Mr. Ravi",
    "address": "Station Road, Palakollu, 534260",
    "rating": 4.3,
    "latitude": 16.5333,
    "longitude": 81.7333,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      }
    ]
  },
  {
    "name": "City Dairy Parlor",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Palakollu, Andhra Pradesh",
    "description": "Parlor offering fresh milk and curd daily.",
    "owner": "Ms. Prakashini",
    "address": "Jogulamba Colony, Palakollu, 534260",
    "rating": 4.0,
    "latitude": 16.5333,
    "longitude": 81.7333,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "City Milk Parlour",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Palakollu, Andhra Pradesh",
    "description": "Neighborhood parlour serving fresh milk packs.",
    "owner": "Mr. Ramesh",
    "address": "Beside Bus Stand, Palakollu, 534260",
    "rating": 4.2,
    "latitude": 16.5333,
    "longitude": 81.7333,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Hari Dairy Corner",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Palakollu, Andhra Pradesh",
    "description": "Fresh dairy items for households.",
    "owner": "Mr. Anil",
    "address": "Main Junction, Palakollu, 534260",
    "rating": 4.1,
    "latitude": 16.5333,
    "longitude": 81.7333,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Haritha Dairy Shop",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Palakollu, Andhra Pradesh",
    "description": "Daily supply of toned milk & butter.",
    "owner": "Ms. Savitri",
    "address": "Main Street, Palakollu, 534260",
    "rating": 3.9,
    "latitude": 16.5333,
    "longitude": 81.7333,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Toned Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Toned+Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      }
    ]
  },
  {
    "name": "Lakshmi Milk Sellers",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Palakollu, Andhra Pradesh",
    "description": "Packaged milk and ghee in hygienic packs.",
    "owner": "Ms. Gowri",
    "address": "Powerpet Road, Palakollu, 534260",
    "rating": 3.8,
    "latitude": 16.5333,
    "longitude": 81.7333,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Packaged Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Packaged+Milk"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      }
    ]
  },
  {
    "name": "Mother Dairy Milk Dealer",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Palakollu, Andhra Pradesh",
    "description": "Authorized Mother Dairy milk dealership.",
    "owner": "Mother Dairy",
    "address": "Palakollu Main Road, West Godavari, 534260",
    "rating": 4.5,
    "latitude": 16.5333,
    "longitude": 81.7333,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Toned Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Toned+Milk"
      },
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Narasimha Milk Booth",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Palakollu, Andhra Pradesh",
    "description": "Local stall offering fresh milk and snacks.",
    "owner": "Mr. Raju",
    "address": "Temple Street, Palakollu, 534260",
    "rating": 3.9,
    "latitude": 16.5333,
    "longitude": 81.7333,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      }
    ]
  },
  {
    "name": "Padmavathi Dairy Hub",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Palakollu, Andhra Pradesh",
    "description": "Paneer and curd specialists with daily supply.",
    "owner": "Ms. Padmavathi",
    "address": "Prakash Nagar, Palakollu, 534260",
    "rating": 4.2,
    "latitude": 16.5333,
    "longitude": 81.7333,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      }
    ]
  },
  {
    "name": "Palakollu Dairy Booth",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Palakollu, Andhra Pradesh",
    "description": "Booth offering fresh milk and curd to local residents.",
    "owner": "Local Co-op Society",
    "address": "Market Road, Palakollu, 534260",
    "rating": 4.0,
    "latitude": 16.5333,
    "longitude": 81.7333,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "SS Infra Logistics Pvt Ltd",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Palakollu, Andhra Pradesh",
    "description": "Retailer of milk dairy, dairy farms and dairy-based products.",
    "owner": "Ali",
    "address": "Palakollu, West Godavari, 534260",
    "rating": 4.1,
    "latitude": 16.5333,
    "longitude": 81.7333,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Dairy Products",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Dairy+Products"
      }
    ]
  },
  {
    "name": "Sai Sri Dairy Hub",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Palakollu, Andhra Pradesh",
    "description": "Modern dairy hub with packaged milk & ghee.",
    "owner": "Mr. Prasad",
    "address": "Kathipudi Road, Palakollu, 534260",
    "rating": 4.4,
    "latitude": 16.5333,
    "longitude": 81.7333,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Packaged Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Packaged+Milk"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Sri Padmavathi Milk Centre",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Palakollu, Andhra Pradesh",
    "description": "Paneer, curd specialists with fresh milk.",
    "owner": "Ms. Padmavathi",
    "address": "Church Road, Palakollu, 534260",
    "rating": 4.3,
    "latitude": 16.5333,
    "longitude": 81.7333,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      }
    ]
  },
  {
    "name": "Sri Satya Sai Dairy Traders",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Palakollu, Andhra Pradesh",
    "description": "Dairy hub with hygienic packaging.",
    "owner": "Mr. Prasad",
    "address": "Service Road, Palakollu, 534260",
    "rating": 4.0,
    "latitude": 16.5333,
    "longitude": 81.7333,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Packaged Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Packaged+Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      }
    ]
  },
  {
    "name": "Vallabha Milk Agency",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Palakollu, Andhra Pradesh",
    "description": "Trusted for fresh dairy produce.",
    "owner": "Mr. Ravi",
    "address": "Jagannaickapuram Road, Palakollu, 534260",
    "rating": 4.5,
    "latitude": 16.5333,
    "longitude": 81.7333,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      },
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      }
    ]
  },
  {
    "name": "Ajay Milk",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Rajahmundry, Andhra Pradesh",
    "description": "Dairy outlet offering milk products.",
    "owner": "Mr. Unknown",
    "address": "Jampet, Rajahmundry, 533103",
    "rating": 4.0,
    "latitude": 16.994,
    "longitude": 81.774,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      }
    ]
  },
  {
    "name": "Ambica Milk Parlour",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Rajahmundry, Andhra Pradesh",
    "description": "Parlour serving fresh milk and curd.",
    "owner": "Mr. Unknown",
    "address": "Near Kotipalli Bus Stand, Innespeta, 533101",
    "rating": 4.1,
    "latitude": 16.994,
    "longitude": 81.774,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Amrutha Milk & Milk Products",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Rajahmundry, Andhra Pradesh",
    "description": "Milk products outlet under APPM complex.",
    "owner": "Mr. Unknown",
    "address": "Opp. APPM Ltd., Sriram Nagar, Rajahmundry, 533103",
    "rating": 4.4,
    "latitude": 16.994,
    "longitude": 81.774,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      },
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      }
    ]
  },
  {
    "name": "Chella Ram Dairy Farm",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Rajahmundry, Andhra Pradesh",
    "description": "Local dairy farm selling milk and ghee.",
    "owner": "Mr. Unknown",
    "address": "Gunduvari Street, Rajahmundry, 533101",
    "rating": 4.3,
    "latitude": 16.994,
    "longitude": 81.774,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      }
    ]
  },
  {
    "name": "City Milk",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Rajahmundry, Andhra Pradesh",
    "description": "Retail milk outlet in Danavaipet area.",
    "owner": "Mr. Unknown",
    "address": "Danavaipet, Rajahmundry, 533103",
    "rating": 4.2,
    "latitude": 16.994,
    "longitude": 81.774,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      }
    ]
  },
  {
    "name": "Devi Sri Santhoshi Milk Foods",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Rajahmundry, Andhra Pradesh",
    "description": "Local milk foods and dairy products provider.",
    "owner": "Ms. Unknown",
    "address": "Near JK Restaurant, Kumari Talkies Road, Rajahmundry, 533101",
    "rating": 4.1,
    "latitude": 16.994,
    "longitude": 81.774,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      }
    ]
  },
  {
    "name": "Godavari Co-Op Milk Producers Union",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Rajahmundry, Andhra Pradesh",
    "description": "Co-op union selling fresh and processed dairy products.",
    "owner": "Co-Operative Society",
    "address": "Rajahmundry Dairy Complex, Alcot Gardens, 533101",
    "rating": 4.6,
    "latitude": 16.994,
    "longitude": 81.774,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Govt. Dairy Farm",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Rajahmundry, Andhra Pradesh",
    "description": "Government-run dairy farm with fresh milk supply.",
    "owner": "Government of AP",
    "address": "Alcot Gardens, Rajahmundry, 533101",
    "rating": 4.2,
    "latitude": 16.994,
    "longitude": 81.774,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      }
    ]
  },
  {
    "name": "Heritage Foods (Gangaraju Dairy)",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Rajahmundry, Andhra Pradesh",
    "description": "Packaged and pasteurized milk products.",
    "owner": "Heritage Foods Ltd",
    "address": "Near Kumari Talkies, T. Nagar, Rajahmundry, 533101",
    "rating": 4.5,
    "latitude": 16.994,
    "longitude": 81.774,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Toned Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Toned+Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      },
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      }
    ]
  },
  {
    "name": "Manikanta Dairy Products (Lingampeta)",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Rajahmundry, Andhra Pradesh",
    "description": "Local dairy with fresh buffalo milk supply.",
    "owner": "Mr. Unknown",
    "address": "Lingampeta, Rajahmundry, 533103",
    "rating": 4.1,
    "latitude": 16.994,
    "longitude": 81.774,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Buffalo Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Buffalo+Milk"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      }
    ]
  },
  {
    "name": "Margani Dairy Farm",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Rajahmundry, Andhra Pradesh",
    "description": "Local dairy farm producing fresh milk and ghee.",
    "owner": "Mr. Unknown",
    "address": "V.L. Puram, Rajahmundry, 533103",
    "rating": 4.4,
    "latitude": 16.994,
    "longitude": 81.774,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      }
    ]
  },
  {
    "name": "Nava Jyothi Dairy",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Rajahmundry, Andhra Pradesh",
    "description": "Fresh milk and dairy products supplier.",
    "owner": "Mr. Unknown",
    "address": "Seethampet, Rajahmundry, 533103",
    "rating": 4.0,
    "latitude": 16.994,
    "longitude": 81.774,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      },
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      }
    ]
  },
  {
    "name": "Sai Ram Milk",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Rajahmundry, Andhra Pradesh",
    "description": "Local milk parlour serving fresh milk daily.",
    "owner": "Mr. Unknown",
    "address": "Thadithota, Rajahmundry (Beside Rama Krishna Theatre), 533103",
    "rating": 4.3,
    "latitude": 16.994,
    "longitude": 81.774,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Sri Ayyappa Milk & Dry Fruits",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Rajahmundry, Andhra Pradesh",
    "description": "Retail sale of dairy products, dry fruits, and eggs.",
    "owner": "Mr. Unknown",
    "address": "46-22-14, Danavaipeta, Near Petrol Bunk, Rajahmundry, 533103",
    "rating": 4.5,
    "latitude": 16.994,
    "longitude": 81.774,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Eggs",
        "price": "72",
        "unit": "dozen",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Eggs"
      },
      {
        "name": "Dry Fruits",
        "price": "200",
        "unit": "250g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Dry+Fruits"
      }
    ]
  },
  {
    "name": "Sri Sai Supplies",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Rajahmundry, Andhra Pradesh",
    "description": "Retail milk and dairy provider.",
    "owner": "Mr. Unknown",
    "address": "Dowleswaram, Rajahmundry, 533124",
    "rating": 4.0,
    "latitude": 16.994,
    "longitude": 81.774,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      }
    ]
  },
  {
    "name": "Vandana Agencies",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Rajahmundry, Andhra Pradesh",
    "description": "Retail dairy supplies including milk and ghee.",
    "owner": "Mr. Unknown",
    "address": "Opp. APPM Gate, Lalbahadur Sastry Road, Rajahmundry, 533101",
    "rating": 4.2,
    "latitude": 16.994,
    "longitude": 81.774,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Visakha Co-Operative Dairy",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Rajahmundry, Andhra Pradesh",
    "description": "Local co-op outlet for dairy and allied products.",
    "owner": "Co-Operative Society",
    "address": "Near Vimalamma Hospital, Gandhipuram, 533103",
    "rating": 4.5,
    "latitude": 16.994,
    "longitude": 81.774,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Visakha Parlour",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Rajahmundry, Andhra Pradesh",
    "description": "Local dairy parlour serving fresh milk products.",
    "owner": "Mr. Unknown",
    "address": "Dowleswaram, Rajahmundry, 533124",
    "rating": 4.1,
    "latitude": 16.994,
    "longitude": 81.774,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      }
    ]
  },
  {
    "name": "AMRUTHA MILK STORE",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tadepalligudem, Andhra Pradesh",
    "description": "Daily fresh dairy supply at best price.",
    "owner": "Mr. Prasad",
    "address": "DNO 1-28-32, near BUS STAND, 534101",
    "rating": 4.2,
    "latitude": 16.833,
    "longitude": 81.52,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      },
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "ATYAM NAGA SUBRAMANYAM TRADERS",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tadepalligudem, Andhra Pradesh",
    "description": "Best little Dairy Farm Best Quality Best Milk",
    "owner": "Mr. Prasad",
    "address": "Shop NO 02, Tadepalligudem - Nallajerla Rd, 534101",
    "rating": 4.6,
    "latitude": 16.833,
    "longitude": 81.52,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      },
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      }
    ]
  },
  {
    "name": "Ayyappa milk dairy",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tadepalligudem, Andhra Pradesh",
    "description": "Trusted source for organic milk.",
    "owner": "Mr. Ravi",
    "address": "Tadepalligudem - Nallajerla Rd, 534101",
    "rating": 4.5,
    "latitude": 16.833,
    "longitude": 81.52,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      },
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      }
    ]
  },
  {
    "name": "Darmika milk dairy",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tadepalligudem, Andhra Pradesh",
    "description": "Best little Dairy Farm Best Quality Best Milk",
    "owner": "Mr. Kiran",
    "address": "Wekarscolony, Ksn colony, 534101",
    "rating": 4.7,
    "latitude": 16.833,
    "longitude": 81.52,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      },
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      }
    ]
  },
  {
    "name": "Dumont Creamery",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tadepalligudem, Andhra Pradesh",
    "description": "Best quality dairy store in town.",
    "owner": "Ms. Lakshmi",
    "address": "KN PLAZA, KN Rd, 534101",
    "rating": 4.6,
    "latitude": 16.833,
    "longitude": 81.52,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Fresh Dairy Products",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Fresh+Dairy+Products"
      }
    ]
  },
  {
    "name": "Hosanna Milk Dairy",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tadepalligudem, Andhra Pradesh",
    "description": "Best quality dairy store in town.",
    "owner": "Mr. Raju",
    "address": "RGCH+P8P, Koti Bomma Center Rd, 534101",
    "rating": 4.3,
    "latitude": 16.833,
    "longitude": 81.52,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk Products Variety",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk+Products+Variety"
      }
    ]
  },
  {
    "name": "Nandhi Milk",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tadepalligudem, Andhra Pradesh",
    "description": "Daily fresh dairy supply at best price.",
    "owner": "Mrs. Anjali",
    "address": "Tadepalligudem Rd, 534101",
    "rating": 4.1,
    "latitude": 16.833,
    "longitude": 81.52,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Full Cream Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Full+Cream+Milk"
      },
      {
        "name": "Organic Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Organic+Ghee"
      }
    ]
  },
  {
    "name": "Reliance SMART Superstore",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tadepalligudem, Andhra Pradesh",
    "description": "Organic and hygienic dairy items available.",
    "owner": "Mr. Raju",
    "address": "WN 33, No 101, DN 1/47/105, KN Rd, 534101",
    "rating": 4.4,
    "latitude": 16.833,
    "longitude": 81.52,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk Products Variety",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk+Products+Variety"
      }
    ]
  },
  {
    "name": "S S MILK DAIRY",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tadepalligudem, Andhra Pradesh",
    "description": "Local favorite for milk and ghee.",
    "owner": "Mr. Prasad",
    "address": "SHOP NO 1, NEAR, HP Gas Rd, 534101",
    "rating": 4.2,
    "latitude": 16.833,
    "longitude": 81.52,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      },
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Sairam Foods",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tadepalligudem, Andhra Pradesh",
    "description": "Fresh milk and dairy products delivered daily.",
    "owner": "Mr. Ravi",
    "address": "Tadepalligudem - Nallajerla Rd, 534101",
    "rating": 4.4,
    "latitude": 16.833,
    "longitude": 81.52,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      },
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      }
    ]
  },
  {
    "name": "SRI LAKSHMI MILK AND GENERAL STORES",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tadepalligudem, Andhra Pradesh",
    "description": "Fresh milk and dairy products delivered daily.",
    "owner": "Mr. Suresh",
    "address": "RELANGI THEATER OPPO, KN ROAD, 534101",
    "rating": 4.3,
    "latitude": 16.833,
    "longitude": 81.52,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Toned Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Toned+Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      }
    ]
  },
  {
    "name": "SRI SANTHANA GANAPATI MILK AGENCIES",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tadepalligudem, Andhra Pradesh",
    "description": "Trusted source for organic milk.",
    "owner": "Ms. Lakshmi",
    "address": "D.NO.11-2-42/1,RAMACHANDRAO PETA,TADEPALLIGUDEM,WG(D), 534101",
    "rating": 4.4,
    "latitude": 16.833,
    "longitude": 81.52,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      },
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      }
    ]
  },
  {
    "name": "Sri sathya maruthi milk dairy",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tadepalligudem, Andhra Pradesh",
    "description": "Fresh milk and dairy products delivered daily.",
    "owner": "Mrs. Anjali",
    "address": "Ambedkar Nagar, kondayya cheruvu, road, 534101",
    "rating": 4.3,
    "latitude": 16.833,
    "longitude": 81.52,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Full Cream Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Full+Cream+Milk"
      },
      {
        "name": "Organic Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Organic+Ghee"
      }
    ]
  },
  {
    "name": "Sri Vasavi Home Foods & Department Stores",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tadepalligudem, Andhra Pradesh",
    "description": "Daily fresh dairy supply at best price.",
    "owner": "Mr. Kiran",
    "address": "13-9-31/2 Near krishnudu cherruvu, 534101",
    "rating": 4.1,
    "latitude": 16.833,
    "longitude": 81.52,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Full Cream Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Full+Cream+Milk"
      },
      {
        "name": "Organic Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Organic+Ghee"
      }
    ]
  },
  {
    "name": "Tadapalligudam Reilance",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tadepalligudem, Andhra Pradesh",
    "description": "Local favorite for milk and ghee.",
    "owner": "Mr. Suresh",
    "address": "Tadepalligudem - Nallajerla Rd, 534101",
    "rating": 4.0,
    "latitude": 16.833,
    "longitude": 81.52,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk Products Variety",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk+Products+Variety"
      }
    ]
  },
  {
    "name": "Varri Durga Rao",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tadepalligudem, Andhra Pradesh",
    "description": "Best little Dairy Farm Best Quality Best Milk",
    "owner": "Mr. Ravi",
    "address": "QGWJ+RR, 534101",
    "rating": 4.8,
    "latitude": 16.833,
    "longitude": 81.52,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Fresh Dairy Products",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Fresh+Dairy+Products"
      }
    ]
  },
  {
    "name": "Venkatesh MILK STORES",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tadepalligudem, Andhra Pradesh",
    "description": "Best quality dairy store in town.",
    "owner": "Mr. Kiran",
    "address": "Gandhi Bomma Center, 534101",
    "rating": 4.5,
    "latitude": 16.833,
    "longitude": 81.52,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      },
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      }
    ]
  },
  {
    "name": "Vijetha supermarket-Tadepalligudem",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tadepalligudem, Andhra Pradesh",
    "description": "Organic and hygienic dairy items available.",
    "owner": "Mr. Prasad",
    "address": "RG9F+PM6, 534101",
    "rating": 4.6,
    "latitude": 16.833,
    "longitude": 81.52,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      },
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Ayyappa Milk & Cold Drink",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tanuku, Andhra Pradesh",
    "description": "Milk and chilled beverages near local market.",
    "owner": "Mr. Unknown",
    "address": "Sthri Samajam Road, Venkiatrayapuram, Tanuku, 534211",
    "rating": 3.9,
    "latitude": 16.754,
    "longitude": 81.68,
    "plans": [],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Cold Drinks",
        "price": "40",
        "unit": "750ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Cold+Drinks"
      }
    ]
  },
  {
    "name": "HAP Dairy by Garuda Agencies",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tanuku, Andhra Pradesh",
    "description": "High‑quality dairy distribution.",
    "owner": "Mr. Unknown",
    "address": "Station Road, Tanuku, 534211",
    "rating": 4.7,
    "latitude": 16.754,
    "longitude": 81.68,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      }
    ]
  },
  {
    "name": "Karuna Sri Milk Center",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tanuku, Andhra Pradesh",
    "description": "Toned milk and everyday essentials.",
    "owner": "Ms. Unknown",
    "address": "Velpur Road, Venkatarayapuram, Tanuku, 534211",
    "rating": 3.8,
    "latitude": 16.754,
    "longitude": 81.68,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Toned Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Toned+Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      }
    ]
  },
  {
    "name": "Lakshmi Dairy Farm",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tanuku, Andhra Pradesh",
    "description": "Supplier of cow milk, curd, pure cow ghee since 2016.",
    "owner": "Mr. Balakrishna Gandrothu",
    "address": "11-5-82, Koppaka Vari Street, Venkatarayapuram, Tanuku, 534211",
    "rating": 4.5,
    "latitude": 16.754,
    "longitude": 81.68,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Cow Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Cow+Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      }
    ]
  },
  {
    "name": "Lakshmi Narayana Milk Diary",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tanuku, Andhra Pradesh",
    "description": "Local milk diary with daily supply.",
    "owner": "Mr. Unknown",
    "address": "Near Temple Road, Tanuku, 534211",
    "rating": 3.9,
    "latitude": 16.754,
    "longitude": 81.68,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Maruthi Milk Dairy",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tanuku, Andhra Pradesh",
    "description": "Fresh milk and dairy products.",
    "owner": "Mr. Unknown",
    "address": "R K Plaza, Opp. Royal Park Palace, Tanuku, 534211",
    "rating": 4.2,
    "latitude": 16.754,
    "longitude": 81.68,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      }
    ]
  },
  {
    "name": "Raraju Milk Store",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tanuku, Andhra Pradesh",
    "description": "Fresh dairy products for local homes.",
    "owner": "Mr. Unknown",
    "address": "Tanuku Bhimavaram Road, Venkiatrayapuram, Tanuku, 534211",
    "rating": 4.0,
    "latitude": 16.754,
    "longitude": 81.68,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Satya Sai Kirana & General Stores",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tanuku, Andhra Pradesh",
    "description": "Local dairy corner for townships.",
    "owner": "Ms. Unknown",
    "address": "Road Number 9, Venkiatrayapuram, Tanuku, 534211",
    "rating": 4.3,
    "latitude": 16.754,
    "longitude": 81.68,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Shanmukh Milk Agency",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tanuku, Andhra Pradesh",
    "description": "Known for quality milk and ghee.",
    "owner": "Mr. Unknown",
    "address": "Commercial Complex, Tanuku, 534211",
    "rating": 4.5,
    "latitude": 16.754,
    "longitude": 81.68,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      }
    ]
  },
  {
    "name": "Sree Lakshmi Milk Suppliers",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tanuku, Andhra Pradesh",
    "description": "Paneer and pure milk suppliers.",
    "owner": "Ms. Unknown",
    "address": "Tanuku Central Market, 534211",
    "rating": 4.4,
    "latitude": 16.754,
    "longitude": 81.68,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Sri Lakshmi Nagendra Store",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tanuku, Andhra Pradesh",
    "description": "General store with fresh milk packets.",
    "owner": "Mr. Unknown",
    "address": "Tanuku Bhimavaram Road, Venkiatrayapuram, 534211",
    "rating": 4.1,
    "latitude": 16.754,
    "longitude": 81.68,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      }
    ]
  },
  {
    "name": "Sri Sairam Milk Shop",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tanuku, Andhra Pradesh",
    "description": "Milk & cold drinks booth open all day.",
    "owner": "Mr. Unknown",
    "address": "Venkiatrayapuram, Velpur Road, Tanuku, 534211",
    "rating": 4.3,
    "latitude": 16.754,
    "longitude": 81.68,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Cold Drinks",
        "price": "40",
        "unit": "750ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Cold+Drinks"
      }
    ]
  },
  {
    "name": "Sri Satya Sai Kirana",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tanuku, Andhra Pradesh",
    "description": "Convenience store offering dairy products.",
    "owner": "Mr. Unknown",
    "address": "Tanuku Bhimavaram Road, Venkiatrayapuram, 534211",
    "rating": 4.2,
    "latitude": 16.754,
    "longitude": 81.68,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Paneer",
        "price": "115",
        "unit": "200g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Paneer"
      }
    ]
  },
  {
    "name": "Sri Venkata Padma Milk Dairy",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tanuku, Andhra Pradesh",
    "description": "Milk delivery service with 3.7⭐ rating.",
    "owner": "Ms. Unknown",
    "address": "Velpur Road, Tanuku, 534211",
    "rating": 3.7,
    "latitude": 16.754,
    "longitude": 81.68,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      },
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      }
    ]
  },
  {
    "name": "Sri Venkateshwara Milk Dairy",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tanuku, Andhra Pradesh",
    "description": "Local milk booth near city centre.",
    "owner": "Mr. Unknown",
    "address": "Sri Challa Apparao Anasuya Complex, Tanuku, 534211",
    "rating": 4.0,
    "latitude": 16.754,
    "longitude": 81.68,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Toned Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Toned+Milk"
      },
      {
        "name": "Butter",
        "price": "55",
        "unit": "100g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Butter"
      }
    ]
  },
  {
    "name": "Srinivasa Milk Dairy",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tanuku, Andhra Pradesh",
    "description": "Departmental store with dairy essentials.",
    "owner": "Mr. Unknown",
    "address": "Alamurivarividi Street No 2, Tanuku, 534211",
    "rating": 4.1,
    "latitude": 16.754,
    "longitude": 81.68,
    "plans": [
      {
        "name": "Weekly Essentials Plan",
        "price": "₹450 / week",
        "features": [
          "Weekly restock of core products",
          "Flexible delivery",
          "Easy payments"
        ],
        "description": "A convenient weekly plan to keep your kitchen stocked with fresh dairy."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Curd",
        "price": "35",
        "unit": "400g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Curd"
      },
      {
        "name": "Ghee",
        "price": "280",
        "unit": "500g",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ghee"
      }
    ]
  },
  {
    "name": "Thirumala Milk Agency & IceCream Parlour",
    "logo": "https://placehold.co/100x100/CCCCCC/FFFFFF?text=Logo",
    "cover_image": "https://placehold.co/800x300/DDDDDD/AAAAAA?text=Dairy+Shop",
    "location": "Tanuku, Andhra Pradesh",
    "description": "Milk agency combined with ice‑cream parlour.",
    "owner": "Mr. Unknown",
    "address": "Tanuku Main Street, 534211",
    "rating": 4.6,
    "latitude": 16.754,
    "longitude": 81.68,
    "plans": [
      {
        "name": "Monthly Family Plan",
        "price": "₹1800 / month",
        "features": [
          "Daily milk delivery option",
          "Worry-free monthly supply",
          "Pause anytime"
        ],
        "description": "The perfect plan for families to get fresh dairy all month long."
      }
    ],
    "products": [
      {
        "name": "Milk",
        "price": "30",
        "unit": "500ml",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Milk"
      },
      {
        "name": "Ice Cream",
        "price": "50",
        "unit": "scoop",
        "image_url": "https://placehold.co/400x300/EFEFEF/777777?text=Ice+Cream"
      }
    ]
  }
]

def geocode_address(address):
    url = "https://atlas.microsoft.com/search/address/json"
    params = {
        "api-version": "1.0",
        "subscription-key": AZURE_SUBSCRIPTION_KEY,
        "query": address
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data["results"]:
            position = data["results"][0]["position"]
            return position["lat"], position["lon"]
        else:
            print(f"[WARN] No results found for: {address}")
            return None, None
    except Exception as e:
        print(f"[ERROR] Geocoding failed for {address}: {e}")
        return None, None

enriched_data = []
for seller in dairy_data:
    full_address = f"{seller['address']}"
    lat, lon = geocode_address(full_address)
    
    seller["latitude"] = lat
    seller["longitude"] = lon

    enriched_data.append(seller)
    print(f"[INFO] {seller['name']} -> lat: {lat}, lon: {lon}")
    time.sleep(1)  # Respect rate limits

# Insert into MongoDB
try:
    collection.delete_many({})
    result = collection.insert_many(enriched_data)
    print(f"[SUCCESS] Inserted {len(result.inserted_ids)} sellers with coordinates.")
except Exception as e:
    print(f"[ERROR] MongoDB insert failed: {e}")
