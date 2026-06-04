# Skill Lantern Backend

AI-powered career guidance API for Nepal.

## Features

- **Career Prediction**: XGBoost or rule-based career recommendations from a user profile
- **Gemini Refinement**: Optional Gemini-powered reranking and explanation
- **Career Roadmaps**: Structured learning paths with stages, skills, resources, and milestones
- **College Recommendations**: Nepal college suggestions based on career goals and available programs
- **Full Guidance**: Complete career assessment with roadmap, colleges, summary, and immediate actions

## Tech Stack

- **FastAPI** - Python API framework
- **Google Gemini API** - LLM inference for roadmap, summary, and recommendation refinement
- **XGBoost / scikit-learn** - Saved ML model support for career prediction
- **Pandas** - CSV loading and filtering for college/career data
- **Pydantic Settings** - Environment-based configuration

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example env file
cp .env.example .env
```

Set `GEMINI_API_KEY` in `.env`. The API can still return deterministic fallback roadmaps and college matches when Gemini is unavailable, but LLM-enhanced features require a valid key.

### 4. Prepare Data Files

These files should exist in `app/data/`:

- `colleges.csv` - Nepal colleges data
- `career_recommender.csv` - Career training data

The saved model files, if used, live in `app/models/`:

- `xgboost_model.pkl`
- `label_encoder.pkl`
- `feature_columns.pkl`
- `encoders.pkl`

### 5. Run the Server

```bash
# Development with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python directly
python -m app.main
```

## API Endpoints

### Health & Info

- `GET /` - API information
- `GET /api/health` - Health check
- `GET /api/config` - Non-sensitive configuration info

### Career Prediction

- `POST /api/career/predict` - Predict careers from user profile
- `GET /api/career/categories` - List career categories
- `GET /api/career/insights/{career}` - Get career insights

### Career Roadmap

- `POST /api/roadmap/generate` - Generate career roadmap
- `POST /api/roadmap/generate/stream` - Stream roadmap generation

### College Recommendations

- `POST /api/colleges/recommend` - Get college recommendations
- `GET /api/colleges/list` - List all colleges
- `GET /api/colleges/locations` - Get locations
- `GET /api/colleges/universities` - Get universities
- `GET /api/colleges/for-career/{career}` - Get colleges for a career

### Full Recommendations

- `POST /api/recommendations/full` - Complete career guidance
- `POST /api/recommendations/quick` - Quick career suggestions
- `POST /api/recommendations/stream` - Stream full recommendation

## API Documentation

Once running, visit:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Example Request

```bash
curl -X POST "http://localhost:8000/api/career/predict?use_llm=false" \
  -H "Content-Type: application/json" \
  -d '{
    "user_profile": {
      "education_level": "bachelors",
      "skills": ["Python", "SQL", "Machine Learning"],
      "interests": ["Data Science", "AI"],
      "specialization": "Computer Science"
    }
  }'
```

## Project Structure

```text
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   ├── schemas.py
│   │   └── career_predictor.py
│   ├── services/
│   │   ├── gemini_service.py
│   │   ├── college_service.py
│   │   ├── roadmap_service.py
│   │   └── recommendation_service.py
│   ├── routers/
│   │   ├── career.py
│   │   ├── roadmap.py
│   │   ├── colleges.py
│   │   └── recommendations.py
│   ├── prompts/
│   └── data/
├── requirements.txt
├── train_model.py
└── .env.example
```

## License

MIT
