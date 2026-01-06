# Skill Lantern Backend

AI-Powered Career Guidance System for Nepal

## Features

- **Career Prediction**: XGBoost-based career recommendations based on user profile
- **Career Roadmap**: LLaMA-generated learning paths with stages, skills, and resources
- **College Recommendations**: Nepal college suggestions based on career goals
- **Full Guidance**: Complete career assessment with actionable next steps

## Tech Stack

- **FastAPI** - Modern Python web framework
- **XGBoost** - Machine learning for career prediction
- **Ollama/LLaMA** - Local LLM for roadmap and recommendation generation
- **Pandas** - Data processing for college CSV

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

# Edit .env with your settings
```

### 4. Install Ollama (Required for LLM features)

Download and install Ollama from: https://ollama.ai/

Then pull the LLaMA model:
```bash
ollama pull llama3
```

### 5. Prepare Data Files

Place these files in `app/data/`:
- `colleges.csv` - Nepal colleges data
- `career_recommender.csv` - Career training data

### 6. Run the Server

```bash
# Development (with auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python directly
python -m app.main
```

## API Endpoints

### Health & Info
- `GET /` - API information
- `GET /api/health` - Health check

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
- `GET /api/colleges/for-career/{career}` - Get colleges for career

### Full Recommendations
- `POST /api/recommendations/full` - Complete career guidance
- `POST /api/recommendations/quick` - Quick career suggestions
- `POST /api/recommendations/stream` - Stream full recommendation

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Example Request

```bash
curl -X POST "http://localhost:8000/api/career/predict" \
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

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Settings
│   ├── models/
│   │   ├── schemas.py       # Pydantic models
│   │   └── career_predictor.py  # XGBoost predictor
│   ├── services/
│   │   ├── ollama_service.py    # LLM integration
│   │   ├── college_service.py   # College data handling
│   │   ├── roadmap_service.py   # Roadmap generation
│   │   └── recommendation_service.py  # Orchestration
│   ├── routers/
│   │   ├── career.py
│   │   ├── roadmap.py
│   │   ├── colleges.py
│   │   └── recommendations.py
│   ├── prompts/
│   │   ├── roadmap_prompts.py
│   │   ├── college_prompts.py
│   │   └── summary_prompts.py
│   └── data/
│       ├── colleges.csv
│       └── career_recommender.csv
├── requirements.txt
├── .env.example
└── README.md
```

## License

MIT
