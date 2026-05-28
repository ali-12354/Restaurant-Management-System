from models import Category, MenuItem, User
from werkzeug.security import generate_password_hash


def seed_database(db, update_existing=False):
    category_seed = [
        {"name": "Starters", "description": "Small plates to begin the meal"},
        {"name": "Mains", "description": "Chef-crafted signature dishes"},
        {"name": "Desserts", "description": "Sweet finishes"},
        {"name": "Beverages", "description": "Fresh drinks and mocktails"},
    ]

    category_by_name = {category.name: category for category in Category.query.all()}
    for category_data in category_seed:
        if category_data["name"] not in category_by_name:
            category = Category()
            category.name = category_data["name"]
            category.description = category_data["description"]
            db.session.add(category)
            category_by_name[category_data["name"]] = category

    db.session.flush()

    menu_seed = [
        {
            "name": "Smoky Paneer Tikka",
            "description": "Char-grilled paneer cubes served with mint chutney and onion salad.",
            "price": 890,
            "category": "Starters",
            "tags": ["veg", "spicy"],
            "is_featured": True,
            "prep_time": 18,
            "rating": 4.7,
            "image_url": "https://images.unsplash.com/photo-1601050690597-6be9667b9f70?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Herb Butter Chicken",
            "description": "Creamy butter chicken with slow-cooked tomato gravy and fragrant herbs.",
            "price": 1290,
            "category": "Mains",
            "tags": ["bestseller"],
            "is_featured": True,
            "prep_time": 24,
            "rating": 4.8,
            "image_url": "https://images.unsplash.com/photo-1631515243349-e0cb75fb8d3a?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Wood-Fired Veggie Pizza",
            "description": "Crisp base with seasonal vegetables, mozzarella, and smoky chili oil.",
            "price": 1490,
            "category": "Mains",
            "tags": ["veg", "new"],
            "prep_time": 20,
            "rating": 4.5,
            "image_url": "https://images.unsplash.com/photo-1593504049359-74330189a345?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Molten Chocolate Cake",
            "description": "Warm chocolate cake with vanilla ice cream and cocoa dust.",
            "price": 690,
            "category": "Desserts",
            "tags": ["dessert"],
            "prep_time": 14,
            "rating": 4.6,
            "image_url": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Citrus Sparkler",
            "description": "Lemon, mint, and soda served over crushed ice.",
            "price": 390,
            "category": "Beverages",
            "tags": ["drink", "fresh"],
            "prep_time": 8,
            "rating": 4.4,
            "image_url": "https://images.unsplash.com/photo-1497534446932-c925b458314e?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Chicken Biryani",
            "description": "Layered basmati biryani with saffron, tender chicken, and raita.",
            "price": 1450,
            "category": "Mains",
            "tags": ["pakistani", "bestseller", "spicy"],
            "is_featured": True,
            "prep_time": 30,
            "rating": 4.9,
            "image_url": "https://images.unsplash.com/photo-1701579231305-d84d8af9a3fd?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Mutton Karahi",
            "description": "Traditional wok-cooked mutton karahi with tomato, ginger, and green chili.",
            "price": 1890,
            "category": "Mains",
            "tags": ["pakistani", "classic"],
            "prep_time": 32,
            "rating": 4.8,
            "image_url": "https://images.unsplash.com/photo-1628294896516-7f6f4f5f26f1?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Lahori Fish Fry",
            "description": "Crispy gram-flour coated fish fillets with house masala.",
            "price": 1150,
            "category": "Starters",
            "tags": ["pakistani", "crispy"],
            "prep_time": 22,
            "rating": 4.6,
            "image_url": "https://images.unsplash.com/photo-1615141982883-c7ad0e69fd62?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Beef Nihari",
            "description": "Slow-braised beef shank stew served with naan and lemon.",
            "price": 1560,
            "category": "Mains",
            "tags": ["pakistani", "comfort"],
            "prep_time": 28,
            "rating": 4.7,
            "image_url": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Hyderabadi Haleem",
            "description": "Hearty blend of lentils, wheat, and beef topped with fried onions.",
            "price": 1290,
            "category": "Mains",
            "tags": ["pakistani", "ramadan-favorite"],
            "prep_time": 26,
            "rating": 4.7,
            "image_url": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Chapli Kebab Platter",
            "description": "Juicy chapli kebabs with pickled onions, chutney, and naan wedges.",
            "price": 1240,
            "category": "Starters",
            "tags": ["pakistani", "kebab"],
            "prep_time": 20,
            "rating": 4.8,
            "image_url": "https://images.unsplash.com/photo-1529692236671-f1dc1f55c49e?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Seekh Kebab Roll",
            "description": "Smoky seekh kebab wrapped in paratha with mint yogurt sauce.",
            "price": 890,
            "category": "Starters",
            "tags": ["pakistani", "street-food"],
            "prep_time": 16,
            "rating": 4.5,
            "image_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Peshawari Charsi Tikka",
            "description": "Charcoal-grilled chicken tikka, lightly spiced in Peshawari style.",
            "price": 1360,
            "category": "Mains",
            "tags": ["pakistani", "grilled"],
            "is_featured": True,
            "prep_time": 24,
            "rating": 4.8,
            "image_url": "https://images.unsplash.com/photo-1596797038530-2c107aa7d55b?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Daal Chawal",
            "description": "Creamy yellow lentils over steamed rice with tempered spices.",
            "price": 720,
            "category": "Mains",
            "tags": ["pakistani", "veg", "comfort"],
            "prep_time": 15,
            "rating": 4.4,
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Aloo Keema",
            "description": "Minced beef with potatoes cooked in homestyle masala.",
            "price": 980,
            "category": "Mains",
            "tags": ["pakistani", "homestyle"],
            "prep_time": 22,
            "rating": 4.5,
            "image_url": "https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?auto=format&fit=crop&w=1200&q=80",
        },
        {
            "name": "Kheer Delight",
            "description": "Traditional rice pudding with cardamom, almonds, and pistachios.",
            "price": 540,
            "category": "Desserts",
            "tags": ["pakistani", "dessert"],
            "prep_time": 12,
            "rating": 4.6,
            "image_url": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?auto=format&fit=crop&w=1200&q=80",
        },
    ]

    existing_items = {item.name: item for item in MenuItem.query.all()}
    for item_data in menu_seed:
        category = category_by_name[item_data["category"]]
        existing_item = existing_items.get(item_data["name"])
        if existing_item:
            if update_existing:
                existing_item.description = item_data["description"]
                existing_item.price = item_data["price"]
                existing_item.category_id = category.id
                existing_item.tags = item_data.get("tags", [])
                existing_item.is_featured = item_data.get("is_featured", False)
                existing_item.prep_time = item_data.get("prep_time", 20)
                existing_item.rating = item_data.get("rating", 4.5)
                existing_item.image_url = item_data.get("image_url")
            continue

        menu_item = MenuItem()
        menu_item.name = item_data["name"]
        menu_item.description = item_data["description"]
        menu_item.price = item_data["price"]
        menu_item.category_id = category.id
        menu_item.tags = item_data.get("tags", [])
        menu_item.is_featured = item_data.get("is_featured", False)
        menu_item.prep_time = item_data.get("prep_time", 20)
        menu_item.rating = item_data.get("rating", 4.5)
        menu_item.image_url = item_data.get("image_url")
        db.session.add(menu_item)

    if not User.query.filter_by(email="admin@restaurant.local").first():
        admin_user = User()
        admin_user.name = "Admin User"
        admin_user.email = "admin@restaurant.local"
        admin_user.password_hash = generate_password_hash("Admin@12345")
        admin_user.role = "admin"
        admin_user.phone = "0000000000"
        db.session.add(admin_user)

    db.session.commit()