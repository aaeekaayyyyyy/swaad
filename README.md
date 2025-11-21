# Swaad - Flavor Profile Recipe Recommendation System

A full-stack application that creates personalized flavor profiles based on your favorite dishes and recommends menu items that match your taste preferences.

## Features

- **Flavor Profile Creation**: Enter your favorite dishes in three categories (appetizers, mains, desserts) to create a personalized flavor profile
- **Menu Processing**: Upload or paste menu text to extract dish names
- **Smart Recommendations**: Get dish recommendations based on flavor profile similarity matching
- **Visual Flavor Profiles**: Interactive radar charts showing your flavor preferences

## Project Structure

```
swaad/
├── backend/
│   ├── main.py              # FastAPI backend server
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.jsx          # Main app component
│   │   └── main.jsx         # Entry point
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
└── recipes_with_flavour_profiles.csv  # Recipe data
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Install OCR for menu image scanning:
```bash
# For image upload functionality, install one of:
pip install Pillow easyocr  # Recommended - EasyOCR is more accurate
# OR
pip install Pillow pytesseract  # Alternative - requires: brew install tesseract
```

4. Make sure `recipes_with_flavour_profiles.csv` is in the project root (one level up from backend):
```bash
# The CSV should be at: ../recipes_with_flavour_profiles.csv
```

5. Run the backend server:
```bash
python main.py
```

The backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

## Usage

1. **Create Your Profile**:
   - Enter dishes you like in each category (appetizers, mains, desserts)
   - Use the search feature to find dishes from the recipe database
   - Click "Create My Flavor Profile" to generate your profile

2. **View Your Profile**:
   - See visual radar charts showing your flavor preferences
   - View detailed flavor percentages for each category

3. **Upload Menu**:
   - Paste menu text or type dish names (one per line)
   - The system will extract dish names automatically
   - Click "Get Recommendations"

4. **Get Recommendations**:
   - View recommended dishes sorted by flavor similarity
   - See match percentages and flavor profiles for each recommendation
   - Expand to see ingredients

## API Endpoints

- `POST /api/create-profile` - Create user flavor profile from liked dishes
- `POST /api/process-menu` - Extract dish names from menu text
- `POST /api/recommendations` - Get dish recommendations based on profile and menu
- `GET /api/search-recipes` - Search for recipes by name

## Technologies Used

- **Backend**: FastAPI, Pandas, NumPy, Scikit-learn
- **Frontend**: React, Vite, Recharts, Axios
- **Data**: CSV-based recipe database with flavor profiles

## Features

- **Menu Image Upload**: Upload photos of menus and automatically extract text using OCR
- **Smart Menu Parsing**: Recognizes category synonyms (appetizers/starters, mains/main course, etc.)
- **Text Input**: Still supports manual text input for menus
- **Flavor Profile Matching**: Uses cosine similarity to match user preferences with menu items

## Notes

- The system uses fuzzy matching to find recipes by name
- Flavor profiles are calculated as averages of ingredient flavors
- Recommendations are ranked by cosine similarity of flavor profiles
- Menu text extraction uses OCR for images or simple heuristics for text input
- See `OCR_SETUP.md` for detailed OCR installation instructions

## Future Enhancements

- Image upload for menu scanning (OCR integration)
- User accounts and saved profiles
- More sophisticated recipe categorization
- Enhanced menu parsing with ML models

