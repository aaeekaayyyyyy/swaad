from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
try:
    from email_validator import validate_email
    EMAIL_VALIDATION_AVAILABLE = True
except ImportError:
    EMAIL_VALIDATION_AVAILABLE = False
    # Use string instead if email-validator not available
    EmailStr = str
from typing import List, Dict, Optional
import pandas as pd
import ast
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
from sqlalchemy.orm import Session
from database import get_db, User, Base, engine
from auth import (
    verify_password, get_password_hash, create_access_token,
    get_user_by_email, get_user_by_username, get_current_user
)
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

try:
    from google_auth import verify_google_token
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_AUTH_AVAILABLE = bool(GOOGLE_CLIENT_ID)
except ImportError:
    GOOGLE_AUTH_AVAILABLE = False
    GOOGLE_CLIENT_ID = None
from datetime import timedelta

# Optional OCR imports
try:
    from PIL import Image
    import io
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False

try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False

app = FastAPI(title="Swaad Recipe Recommendation API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load recipes data
recipes_df = None

def load_recipes():
    global recipes_df
    if recipes_df is None:
        import os
        # Try current directory first, then parent directory
        csv_path = 'recipes_with_flavour_profiles.csv'
        if not os.path.exists(csv_path):
            csv_path = '../recipes_with_flavour_profiles.csv'
        recipes_df = pd.read_csv(csv_path)
        # Parse flavor_profile strings to dictionaries
        recipes_df['flavor_profile'] = recipes_df['flavor_profile'].apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) else x
        )
    return recipes_df

# Request models
class DishInput(BaseModel):
    name: str
    category: str  # "appetizer", "mains", "desserts"

class UserDishes(BaseModel):
    dishes: List[DishInput]

class MenuText(BaseModel):
    text: str

# Response models
class FlavorProfile(BaseModel):
    spicy: float
    sweet: float
    umami: float
    sour: float
    salty: float

class UserProfile(BaseModel):
    appetizer: FlavorProfile
    mains: FlavorProfile
    desserts: FlavorProfile

class RecommendationsRequest(BaseModel):
    user_profile: UserProfile
    menu_dishes: List[str]
    categorized_dishes: Optional[Dict[str, List[str]]] = None

# Auth models
class UserSignup(BaseModel):
    email: EmailStr
    username: str
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "securepassword123"
            }
        }

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str

class GoogleLoginRequest(BaseModel):
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None
    google_id: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    flavor_profile: Optional[UserProfile] = None
    favorite_dishes: List[DishInput] = []

class RecipeRecommendation(BaseModel):
    id: int
    name: str
    ingredients: List[str]
    flavor_profile: FlavorProfile
    similarity_score: float
    category: str

class RecommendationsResponse(BaseModel):
    recommendations: Dict[str, List[RecipeRecommendation]]

def find_recipe_by_name(name: str, df: pd.DataFrame) -> Optional[Dict]:
    """Find a recipe by name (fuzzy matching)"""
    name_lower = name.lower().strip()
    
    # Exact match
    exact_match = df[df['name'].str.lower() == name_lower]
    if not exact_match.empty:
        return exact_match.iloc[0].to_dict()
    
    # Partial match
    partial_match = df[df['name'].str.lower().str.contains(name_lower, na=False)]
    if not partial_match.empty:
        return partial_match.iloc[0].to_dict()
    
    # Word-based matching
    name_words = set(name_lower.split())
    best_match = None
    best_score = 0
    
    for idx, row in df.iterrows():
        recipe_name = str(row['name']).lower()
        recipe_words = set(recipe_name.split())
        common_words = name_words.intersection(recipe_words)
        if common_words:
            score = len(common_words) / max(len(name_words), len(recipe_words))
            if score > best_score:
                best_score = score
                best_match = row.to_dict()
    
    return best_match if best_score > 0.3 else None

def calculate_average_flavor_profile(recipes: List[Dict]) -> Dict[str, float]:
    """Calculate average flavor profile from a list of recipes"""
    if not recipes:
        return {"spicy": 0.0, "sweet": 0.0, "umami": 0.0, "sour": 0.0, "salty": 0.0}
    
    profiles = []
    for recipe in recipes:
        if isinstance(recipe['flavor_profile'], str):
            profile = ast.literal_eval(recipe['flavor_profile'])
        else:
            profile = recipe['flavor_profile']
        profiles.append(profile)
    
    avg_profile = {
        "spicy": np.mean([p.get("spicy", 0) for p in profiles]),
        "sweet": np.mean([p.get("sweet", 0) for p in profiles]),
        "umami": np.mean([p.get("umami", 0) for p in profiles]),
        "sour": np.mean([p.get("sour", 0) for p in profiles]),
        "salty": np.mean([p.get("salty", 0) for p in profiles])
    }
    
    return {k: round(v, 2) for k, v in avg_profile.items()}

def extract_dishes_from_menu(menu_text: str) -> Dict[str, List[str]]:
    """Extract dish names from menu text and categorize them"""
    lines = menu_text.split('\n')
    
    # Category synonyms mapping
    appetizer_synonyms = ['appetizer', 'appetiser', 'appetizers', 'appetisers', 
                         'starter', 'starters', 'small plates', 'small plate',
                         'tapas', 'hors d\'oeuvres', 'hors d\'oeuvre']
    mains_synonyms = ['main', 'mains', 'main course', 'main courses', 
                     'entree', 'entrees', 'big plates', 'big plate',
                     'large plates', 'large plate', 'mains course']
    dessert_synonyms = ['dessert', 'desserts', 'sweet', 'sweets', 
                       'pudding', 'puddings', 'finale', 'finales']
    
    categorized_dishes = {
        "appetizer": [],
        "mains": [],
        "desserts": []
    }
    
    current_category = None
    
    for line in lines:
        line_original = line.strip()
        if not line_original:
            continue
        
        line_lower = line_original.lower()
        
        # Check if this line is a category header
        is_appetizer_header = any(syn in line_lower for syn in appetizer_synonyms)
        is_mains_header = any(syn in line_lower for syn in mains_synonyms)
        is_dessert_header = any(syn in line_lower for syn in dessert_synonyms)
        
        if is_appetizer_header:
            current_category = "appetizer"
            continue
        elif is_mains_header:
            current_category = "mains"
            continue
        elif is_dessert_header:
            current_category = "desserts"
            continue
        
        # Skip lines that are clearly not dish names
        skip_keywords = ['$', 'price', 'menu', 'drink', 'beverage', 'wine', 'beer', 
                        'cocktail', 'coffee', 'tea', 'juice', 'allergen', 'contains']
        if any(skip in line_lower for skip in skip_keywords):
            continue
        
        # Remove common prefixes/suffixes
        line_clean = re.sub(r'^\d+[\.\)]\s*', '', line_original)  # Remove numbering
        line_clean = re.sub(r'\s*\$.*$', '', line_clean)  # Remove prices
        line_clean = re.sub(r'\s*-\s*\$.*$', '', line_clean)  # Remove prices with dash
        line_clean = line_clean.strip()
        
        # Skip if too short or too long
        if len(line_clean) < 3 or len(line_clean) > 100:
            continue
        
        # If we have a current category, use it; otherwise try to infer
        if current_category:
            categorized_dishes[current_category].append(line_clean)
        else:
            # Try to infer category from dish name
            dish_lower = line_clean.lower()
            dessert_keywords = ['cake', 'pie', 'ice cream', 'pudding', 'chocolate', 'cookie', 
                              'brownie', 'tart', 'mousse', 'custard', 'flan', 'sorbet']
            appetizer_keywords = ['salad', 'soup', 'dip', 'bruschetta', 'samosa', 'spring roll',
                                'wings', 'nachos', 'quesadilla', 'hummus', 'guacamole']
            
            if any(kw in dish_lower for kw in dessert_keywords):
                categorized_dishes["desserts"].append(line_clean)
            elif any(kw in dish_lower for kw in appetizer_keywords):
                categorized_dishes["appetizer"].append(line_clean)
            else:
                # Default to mains if uncertain
                categorized_dishes["mains"].append(line_clean)
    
    # Limit each category to 20 dishes
    for category in categorized_dishes:
        categorized_dishes[category] = categorized_dishes[category][:20]
    
    return categorized_dishes

def calculate_similarity(profile1: Dict, profile2: Dict) -> float:
    """Calculate cosine similarity between two flavor profiles"""
    keys = ['spicy', 'sweet', 'umami', 'sour', 'salty']
    vec1 = np.array([profile1.get(k, 0) for k in keys])
    vec2 = np.array([profile2.get(k, 0) for k in keys])
    
    # Avoid division by zero
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        return 0.0
    
    return float(cosine_similarity([vec1], [vec2])[0][0])

# Initialize database
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Swaad Recipe Recommendation API"}

# Authentication endpoints
@app.post("/api/auth/signup", response_model=Token)
def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    """Create a new user account"""
    try:
        # Check if email already exists
        if get_user_by_email(db, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if username already exists
        if get_user_by_username(db, user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Validate password length
        if len(user_data.password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 6 characters"
            )
        
        # Check byte length (bcrypt limit is 72 bytes, not characters)
        password_bytes = user_data.password.encode('utf-8')
        if len(password_bytes) > 72:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is too long (maximum 72 bytes). Please use a shorter password."
            )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            favorite_dishes=[]
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Create access token
        access_token_expires = timedelta(minutes=30 * 24 * 60)  # 30 days
        access_token = create_access_token(
            data={"sub": db_user.id}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": db_user.id,
            "username": db_user.username
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Signup error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating account: {str(e)}"
        )

@app.post("/api/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and get access token"""
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30 * 24 * 60)  # 30 days
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }

@app.post("/api/auth/google", response_model=Token)
def google_login(google_data: GoogleLoginRequest, db: Session = Depends(get_db)):
    """Login or signup with Google OAuth"""
    email = google_data.email
    name = google_data.name or ''
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required"
        )
    
    # Validate email format
    if '@' not in email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    
    # Check if user exists by email
    user = get_user_by_email(db, email)
    
    if not user:
        # Create new user with Google account
        # Generate a username from email or name
        username_base = name.lower().replace(' ', '_').replace('.', '_') if name else email.split('@')[0]
        # Remove special characters
        username_base = ''.join(c for c in username_base if c.isalnum() or c == '_')
        username = username_base[:30]  # Limit username length
        counter = 1
        
        # Ensure username is unique
        while get_user_by_username(db, username):
            username = f"{username_base[:25]}{counter}"
            counter += 1
            if counter > 1000:  # Safety limit
                username = f"user_{email.split('@')[0][:20]}"
                break
        
        # Create user without password (Google-authenticated users don't need password)
        db_user = User(
            email=email,
            username=username,
            hashed_password="",  # Empty for Google-authenticated users
            favorite_dishes=[]
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        user = db_user
    else:
        # Existing user - update username if it's empty
        if not user.username:
            username_base = name.lower().replace(' ', '_') if name else email.split('@')[0]
            username_base = ''.join(c for c in username_base if c.isalnum() or c == '_')
            user.username = username_base[:30]
            db.commit()
    
    # Create access token
    access_token_expires = timedelta(minutes=30 * 24 * 60)  # 30 days
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }

@app.get("/api/auth/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    flavor_profile = None
    if current_user.flavor_profile:
        flavor_profile = UserProfile(**current_user.flavor_profile)
    
    favorite_dishes = []
    if current_user.favorite_dishes:
        favorite_dishes = [DishInput(**dish) for dish in current_user.favorite_dishes]
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "flavor_profile": flavor_profile,
        "favorite_dishes": favorite_dishes
    }

# User profile management endpoints
@app.post("/api/user/profile", response_model=UserProfile)
def save_user_profile(
    user_dishes: UserDishes,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Save or update user's flavor profile"""
    df = load_recipes()
    
    categories = {
        "appetizer": [],
        "mains": [],
        "desserts": []
    }
    
    for dish in user_dishes.dishes:
        recipe = find_recipe_by_name(dish.name, df)
        if recipe:
            categories[dish.category].append(recipe)
    
    # Calculate average profiles for each category
    appetizer_profile = calculate_average_flavor_profile(categories["appetizer"])
    mains_profile = calculate_average_flavor_profile(categories["mains"])
    desserts_profile = calculate_average_flavor_profile(categories["desserts"])
    
    user_profile = {
        "appetizer": appetizer_profile,
        "mains": mains_profile,
        "desserts": desserts_profile
    }
    
    # Save to database
    current_user.flavor_profile = user_profile
    current_user.favorite_dishes = [dish.dict() for dish in user_dishes.dishes]
    db.commit()
    
    return user_profile

@app.get("/api/user/profile", response_model=UserProfile)
def get_user_profile(current_user: User = Depends(get_current_user)):
    """Get user's saved flavor profile"""
    if not current_user.flavor_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No flavor profile found. Please create one first."
        )
    return UserProfile(**current_user.flavor_profile)

@app.put("/api/user/profile/dishes")
def update_user_dishes(
    user_dishes: UserDishes,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's favorite dishes and recalculate profile"""
    # Save dishes
    current_user.favorite_dishes = [dish.dict() for dish in user_dishes.dishes]
    
    # Recalculate profile
    df = load_recipes()
    categories = {
        "appetizer": [],
        "mains": [],
        "desserts": []
    }
    
    for dish in user_dishes.dishes:
        recipe = find_recipe_by_name(dish.name, df)
        if recipe:
            categories[dish.category].append(recipe)
    
    appetizer_profile = calculate_average_flavor_profile(categories["appetizer"])
    mains_profile = calculate_average_flavor_profile(categories["mains"])
    desserts_profile = calculate_average_flavor_profile(categories["desserts"])
    
    current_user.flavor_profile = {
        "appetizer": appetizer_profile,
        "mains": mains_profile,
        "desserts": desserts_profile
    }
    
    db.commit()
    
    return {
        "message": "Profile updated successfully",
        "flavor_profile": current_user.flavor_profile,
        "favorite_dishes": current_user.favorite_dishes
    }

@app.delete("/api/user/profile/dishes")
def remove_dish_from_profile(
    dish_name: str,
    category: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a dish from user's profile"""
    if not current_user.favorite_dishes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No dishes found in profile"
        )
    
    # Remove dish
    updated_dishes = [
        dish for dish in current_user.favorite_dishes
        if not (dish.get("name") == dish_name and dish.get("category") == category)
    ]
    
    if len(updated_dishes) == len(current_user.favorite_dishes):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dish not found in profile"
        )
    
    current_user.favorite_dishes = updated_dishes
    
    # Recalculate profile
    if updated_dishes:
        df = load_recipes()
        categories = {
            "appetizer": [],
            "mains": [],
            "desserts": []
        }
        
        for dish in updated_dishes:
            recipe = find_recipe_by_name(dish["name"], df)
            if recipe:
                categories[dish["category"]].append(recipe)
        
        appetizer_profile = calculate_average_flavor_profile(categories["appetizer"])
        mains_profile = calculate_average_flavor_profile(categories["mains"])
        desserts_profile = calculate_average_flavor_profile(categories["desserts"])
        
        current_user.flavor_profile = {
            "appetizer": appetizer_profile,
            "mains": mains_profile,
            "desserts": desserts_profile
        }
    else:
        current_user.flavor_profile = None
    
    db.commit()
    
    return {
        "message": "Dish removed successfully",
        "flavor_profile": current_user.flavor_profile,
        "favorite_dishes": current_user.favorite_dishes
    }

@app.post("/api/create-profile", response_model=UserProfile)
def create_user_profile(user_dishes: UserDishes):
    """Create user flavor profile from liked dishes (works for both authenticated and guest users)"""
    df = load_recipes()
    
    categories = {
        "appetizer": [],
        "mains": [],
        "desserts": []
    }
    
    found_recipes = []
    not_found = []
    
    for dish in user_dishes.dishes:
        recipe = find_recipe_by_name(dish.name, df)
        if recipe:
            categories[dish.category].append(recipe)
            found_recipes.append(dish.name)
        else:
            not_found.append(dish.name)
    
    # Calculate average profiles for each category
    appetizer_profile = calculate_average_flavor_profile(categories["appetizer"])
    mains_profile = calculate_average_flavor_profile(categories["mains"])
    desserts_profile = calculate_average_flavor_profile(categories["desserts"])
    
    return {
        "appetizer": appetizer_profile,
        "mains": mains_profile,
        "desserts": desserts_profile
    }

# Initialize EasyOCR reader (lazy loading)
ocr_reader = None

def get_ocr_reader():
    """Lazy load OCR reader"""
    global ocr_reader
    if ocr_reader is None:
        if EASYOCR_AVAILABLE:
            try:
                ocr_reader = easyocr.Reader(['en'], gpu=False)
            except Exception as e:
                print(f"Warning: EasyOCR initialization failed: {e}")
                ocr_reader = "pytesseract" if PYTESSERACT_AVAILABLE else None
        elif PYTESSERACT_AVAILABLE:
            ocr_reader = "pytesseract"
        else:
            ocr_reader = None
    return ocr_reader

def extract_text_from_image(image_bytes: bytes) -> str:
    """Extract text from menu image using OCR"""
    if not PIL_AVAILABLE:
        raise HTTPException(
            status_code=500, 
            detail="PIL/Pillow not installed. Please install: pip install Pillow"
        )
    
    reader = get_ocr_reader()
    
    if reader is None:
        raise HTTPException(
            status_code=500, 
            detail="OCR not available. Please install easyocr (pip install easyocr) or pytesseract (pip install pytesseract). See OCR_SETUP.md for instructions."
        )
    
    try:
        from PIL import Image
        import io
        image = Image.open(io.BytesIO(image_bytes))
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        if reader != "pytesseract":
            # Use EasyOCR
            import numpy as np
            img_array = np.array(image)
            results = reader.readtext(img_array)
            # Combine all detected text
            text = '\n'.join([result[1] for result in results])
            return text
        else:
            # Use pytesseract
            import pytesseract
            text = pytesseract.image_to_string(image)
            return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text from image: {str(e)}")

@app.post("/api/process-menu")
def process_menu_text(menu: MenuText):
    """Extract dish names from menu text and categorize them"""
    categorized_dishes = extract_dishes_from_menu(menu.text)
    # Flatten for backward compatibility, but also return categorized
    all_dishes = categorized_dishes["appetizer"] + categorized_dishes["mains"] + categorized_dishes["desserts"]
    return {
        "dishes": all_dishes,
        "categorized": categorized_dishes
    }

@app.post("/api/upload-menu-image")
async def upload_menu_image(file: UploadFile = File(...)):
    """Upload menu image and extract text using OCR"""
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Read image bytes
    try:
        image_bytes = await file.read()
        
        # Extract text from image
        extracted_text = extract_text_from_image(image_bytes)
        
        if not extracted_text or len(extracted_text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Could not extract text from image. Please ensure the image is clear and contains readable text.")
        
        # Process the extracted text
        categorized_dishes = extract_dishes_from_menu(extracted_text)
        all_dishes = categorized_dishes["appetizer"] + categorized_dishes["mains"] + categorized_dishes["desserts"]
        
        return {
            "extracted_text": extracted_text,
            "dishes": all_dishes,
            "categorized": categorized_dishes
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/api/recommendations", response_model=RecommendationsResponse)
def get_recommendations(request: RecommendationsRequest):
    """Get recommendations based on user profile and menu dishes"""
    df = load_recipes()
    
    user_profile = request.user_profile
    menu_dishes = request.menu_dishes
    categorized_dishes = request.categorized_dishes
    
    # Use categorized dishes if provided, otherwise categorize from flat list
    if categorized_dishes:
        dish_categories = categorized_dishes
    else:
        # Fallback: categorize dishes ourselves
        dish_categories = {
            "appetizer": [],
            "mains": [],
            "desserts": []
        }
        for dish in menu_dishes:
            dish_lower = dish.lower()
            dessert_keywords = ['cake', 'pie', 'ice cream', 'pudding', 'chocolate', 'cookie', 
                              'brownie', 'tart', 'mousse', 'custard', 'flan', 'sorbet']
            appetizer_keywords = ['salad', 'soup', 'dip', 'bruschetta', 'samosa', 'spring roll',
                                'wings', 'nachos', 'quesadilla', 'hummus', 'guacamole']
            
            if any(kw in dish_lower for kw in dessert_keywords):
                dish_categories["desserts"].append(dish)
            elif any(kw in dish_lower for kw in appetizer_keywords):
                dish_categories["appetizer"].append(dish)
            else:
                dish_categories["mains"].append(dish)
    
    # Find recipes matching menu dishes, keeping track of their categories
    categorized_recipes = {
        "appetizer": [],
        "mains": [],
        "desserts": []
    }
    
    for category, dishes in dish_categories.items():
        for dish_name in dishes:
            recipe = find_recipe_by_name(dish_name, df)
            if recipe:
                categorized_recipes[category].append(recipe)
    
    # Get recommendations for each category
    recommendations = {
        "appetizer": [],
        "mains": [],
        "desserts": []
    }
    
    for category in ["appetizer", "mains", "desserts"]:
        # Fix Pydantic deprecation: use model_dump() instead of dict()
        user_profile_dict = user_profile.model_dump()[category]
        category_recipes = categorized_recipes[category]
        
        # Calculate similarity scores
        scored_recipes = []
        for recipe in category_recipes:
            if isinstance(recipe['flavor_profile'], str):
                recipe_profile = ast.literal_eval(recipe['flavor_profile'])
            else:
                recipe_profile = recipe['flavor_profile']
            
            similarity = calculate_similarity(user_profile_dict, recipe_profile)
            scored_recipes.append((recipe, similarity))
        
        # Sort by similarity and get top 5
        scored_recipes.sort(key=lambda x: x[1], reverse=True)
        
        for recipe, score in scored_recipes[:5]:
            if isinstance(recipe['ingredients'], str):
                ingredients = ast.literal_eval(recipe['ingredients'])
            else:
                ingredients = recipe['ingredients']
            
            if isinstance(recipe['flavor_profile'], str):
                flavor_profile = ast.literal_eval(recipe['flavor_profile'])
            else:
                flavor_profile = recipe['flavor_profile']
            
            recommendations[category].append({
                "id": int(recipe['id']),
                "name": recipe['name'],
                "ingredients": ingredients,
                "flavor_profile": flavor_profile,
                "similarity_score": round(score, 3),
                "category": category
            })
    
    return {"recommendations": recommendations}

@app.get("/api/search-recipes")
def search_recipes(query: str, limit: int = 10):
    """Search for recipes by name"""
    df = load_recipes()
    query_lower = query.lower()
    
    matches = df[df['name'].str.lower().str.contains(query_lower, na=False)]
    
    results = []
    for idx, row in matches.head(limit).iterrows():
        if isinstance(row['ingredients'], str):
            ingredients = ast.literal_eval(row['ingredients'])
        else:
            ingredients = row['ingredients']
        
        if isinstance(row['flavor_profile'], str):
            flavor_profile = ast.literal_eval(row['flavor_profile'])
        else:
            flavor_profile = row['flavor_profile']
        
        results.append({
            "id": int(row['id']),
            "name": row['name'],
            "ingredients": ingredients,
            "flavor_profile": flavor_profile
        })
    
    return {"recipes": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

