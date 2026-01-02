# Skill Lantern AI Backend

Career recommendation system powered by machine learning.

## Architecture

```
ai/
├── api/                    # FastAPI application
│   ├── main.py            # Application entry point
│   ├── routes/            # API endpoints
│   └── schemas/           # Pydantic models
├── core/                   # Core business logic
│   ├── career_matcher.py  # Rule-based career matching
│   ├── ml_predictor.py    # XGBoost prediction
│   └── guide_generator.py # Career guide generation
├── training/              # Model training scripts
│   ├── train_xgboost.py   # Train XGBoost model
│   ├── preprocess.py      # Data preprocessing
│   └── evaluate.py        # Model evaluation
├── data/                  # Datasets
│   ├── raw/               # Original data files
│   └── processed/         # Cleaned data
├── models/                # Saved models
│   ├── trained/           # Trained model files
│   └── configs/           # Model configurations
├── config/                # Configuration files
│   ├── careers.yaml       # Career definitions
│   └── settings.py        # App settings
└── utils/                 # Utility functions
```

## Setup

### 1. Create Virtual Environment

```bash
# Navigate to ai folder
cd ai

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
```

### 4. Run the API Server

```bash
# Development mode
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Or use the run script
python run.py
```

### 5. Train the Model

```bash
# Prepare your data in data/raw/career_dataset.csv
# Then run training
python -m training.train_xgboost
```

## API Endpoints

- `POST /api/v1/predict` - Get career recommendations
- `GET /api/v1/careers` - List all available careers
- `GET /api/v1/health` - Health check

## Model Training

The system uses a hybrid approach:

1. **Rule-Based Matcher**: Fast, explainable career matching based on defined rules
2. **XGBoost Classifier**: ML model trained on career data for improved accuracy
3. **LLM Generator** (Optional): Generate personalized career guides

## Data Format

Your training data should have these columns:

```csv
math_score,science_score,english_score,gpa,programming,communication,analytical_thinking,...,career_label
85,90,75,3.7,4,3,5,...,Software Engineer
```

See `data/sample_data.csv` for an example.
