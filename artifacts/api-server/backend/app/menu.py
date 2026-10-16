"""Backend-owned menu catalog and lookup structures."""

from decimal import Decimal

from .models.food import FoodItem

MENU: tuple[FoodItem, ...] = (
    FoodItem(
        id="chicken-biryani",
        name="Hyderabadi Chicken Biryani",
        category="Biryani",
        price=Decimal("249.00"),
        description=(
            "Fragrant basmati rice layered with slow-cooked spiced chicken, saffron and caramelised onions."
        ),
        imageUrl="https://images.unsplash.com/photo-1589302168068-964664d93dc0?auto=format&fit=crop&w=900&q=85",
    ),
    FoodItem(
        id="butter-chicken",
        name="Butter Chicken (Murgh Makhani)",
        category="North Indian",
        price=Decimal("269.00"),
        description="Tandoori chicken pieces simmered in a rich, buttery tomato cream gravy with fenugreek.",
        imageUrl="https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=900&q=85",
    ),
    FoodItem(
        id="paneer-butter-masala",
        name="Paneer Butter Masala",
        category="North Indian",
        price=Decimal("229.00"),
        description="Soft paneer in a silky tomato, cashew and butter gravy finished with fresh cream.",
        imageUrl="https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=900&q=85",
    ),
    FoodItem(
        id="dal-makhani",
        name="Dal Makhani",
        category="North Indian",
        price=Decimal("179.00"),
        description="Slow-cooked black lentils and kidney beans simmered overnight with butter and cream.",
        imageUrl="https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=900&q=85",
    ),
    FoodItem(
        id="chole-bhature",
        name="Chole Bhature",
        category="North Indian",
        price=Decimal("159.00"),
        description="Two golden puffed bhaturas served with spicy Punjabi chickpea curry and pickled onions.",
        imageUrl="https://images.unsplash.com/photo-1626132647523-66f5bf380027?auto=format&fit=crop&w=900&q=85",
    ),
    FoodItem(
        id="butter-naan",
        name="Garlic Butter Naan",
        category="North Indian",
        price=Decimal("59.00"),
        description="Tandoor-baked leavened flatbread brushed generously with melted cultured butter and garlic.",
        imageUrl="https://images.unsplash.com/photo-1606471191009-63994c53433b?auto=format&fit=crop&w=900&q=85",
    ),
    FoodItem(
        id="chicken-65",
        name="Crispy Chicken 65",
        category="Starters",
        price=Decimal("199.00"),
        description="Crisp, fiery chicken tossed with fresh curry leaves, green chillies and house spices.",
        imageUrl="https://images.unsplash.com/photo-1610057099443-fde8c4d50f91?auto=format&fit=crop&w=900&q=85",
    ),
    FoodItem(
        id="paneer-tikka",
        name="Tandoori Paneer Tikka",
        category="Starters",
        price=Decimal("189.00"),
        description="Marinated cottage cheese and bell peppers char-grilled in a clay tandoor with mint chutney.",
        imageUrl="https://images.unsplash.com/photo-1596797038530-2c107229654b?auto=format&fit=crop&w=900&q=85",
    ),
    FoodItem(
        id="samosa",
        name="Punjabi Samosa (2 pcs)",
        category="Starters",
        price=Decimal("49.00"),
        description="Crisp golden pastries stuffed with spiced potatoes and peas, served with sweet tamarind dip.",
        imageUrl="https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&w=900&q=85",
    ),
    FoodItem(
        id="masala-dosa",
        name="Mysore Masala Dosa",
        category="South Indian",
        price=Decimal("149.00"),
        description="Crispy golden rice crêpe smeared with spiced red chutney, potato bhaji, sambar and chutneys.",
        imageUrl="https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&w=900&q=85",
    ),
    FoodItem(
        id="idli",
        name="Steamed Idli Sambar (4 pcs)",
        category="South Indian",
        price=Decimal("99.00"),
        description="Four soft steamed rice cakes served with fresh coconut chutney and comforting sambar.",
        imageUrl="https://images.unsplash.com/photo-1630383249896-424e482df921?auto=format&fit=crop&w=900&q=85",
    ),
    FoodItem(
        id="vada",
        name="Crispy Medu Vada (2 pcs)",
        category="South Indian",
        price=Decimal("79.00"),
        description="Crisp golden lentil doughnuts with a fluffy centre, served hot with coconut chutney.",
        imageUrl="https://th.bing.com/th/id/OIP.qtKdrkiaOc_W9AqqygVyaAHaHa?w=198&h=198&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3",
    ),
    FoodItem(
        id="veg-fried-rice",
        name="Veg Fried Rice",
        category="Chinese",
        price=Decimal("179.00"),
        description="Wok-tossed basmati rice with crunchy vegetables, spring onion and aromatic sauces.",
        imageUrl="https://images.unsplash.com/photo-1603133872878-684f208fb84b?auto=format&fit=crop&w=900&q=85",
    ),
    FoodItem(
        id="chicken-fried-rice",
        name="Chicken Fried Rice",
        category="Chinese",
        price=Decimal("219.00"),
        description="Smoky wok-fried rice with tender chicken chunks, scrambled egg, and scallions.",
        imageUrl="https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=900&q=85",
    ),
    FoodItem(
        id="mango-lassi",
        name="Alphonso Mango Lassi",
        category="Beverages",
        price=Decimal("99.00"),
        description="Thick chilled Alphonso mango and fresh yogurt blended smooth with a dash of cardamom.",
        imageUrl="https://images.unsplash.com/photo-1553530666-ba11a7da3888?auto=format&fit=crop&w=900&q=85",
    ),
    FoodItem(
        id="masala-chai",
        name="Kullad Masala Chai",
        category="Beverages",
        price=Decimal("49.00"),
        description="Aromatic Assam tea simmered with fresh crushed ginger, cardamom, cloves and whole milk.",
        imageUrl="https://tse1.mm.bing.net/th/id/OIP.N2fDmxiehVkah77jbVx7egHaE8?r=0&rs=1&pid=ImgDetMain&o=7&rm=3",
    ),
)

# A dictionary gives constant-time lookup when resolving IDs from an order.
MENU_BY_ID: dict[str, FoodItem] = {item.id: item for item in MENU}

# A set is appropriate for coupon membership checks and unique category values.
VALID_COUPONS: set[str] = {"WELCOME50", "SAVE10", "FESTIVE20"}
CATEGORIES: set[str] = {item.category for item in MENU}
