# Skill Lantern — Mid-Year Report Diagrams (Mermaid Code)

> **How to use:** Copy each code block into [Mermaid Live Editor](https://mermaid.live), render it, then export as **PNG** and paste into the DOCX report at the corresponding placeholder.

---

## 1. System Architecture Diagram

```mermaid
graph TB
    subgraph PL["Presentation Layer"]
        Browser["🌐 Browser"]
        NextJS["Next.js 16 Frontend\nReact 19 · TypeScript · Tailwind CSS 4"]
        Pages["Pages:\nLanding · Signup · Login · Dashboard"]
    end

    subgraph AL["Application Layer"]
        FastAPI["FastAPI Backend\nPython · Uvicorn ASGI"]

        subgraph Routers["API Routers"]
            R1["/api/predict"]
            R2["/api/roadmap"]
            R3["/api/colleges"]
            R4["/api/recommendations"]
            R5["/api/health"]
        end

        subgraph Services["Services"]
            S1["OllamaService"]
            S2["CollegeService"]
            S3["RecommendationService"]
            S4["RoadmapService"]
        end

        subgraph Models["AI Models"]
            M1["CareerPredictor\n(XGBoost)"]
            M2["Rule-Based\nFallback"]
        end
    end

    subgraph DL["Data Layer"]
        PG["PostgreSQL\n(via Prisma ORM)"]
        CSV1["career_recommender.csv"]
        CSV2["colleges.csv"]
        PKL["Model Artefacts\n(.pkl files)"]
        Ollama["Ollama Server\n(LLaMA 3)"]
    end

    Browser --> NextJS
    NextJS --> Pages
    NextJS -->|"API Route Proxy"| FastAPI
    FastAPI --> Routers
    Routers --> Services
    Routers --> Models

    S1 -->|"httpx async"| Ollama
    S2 --> CSV2
    M1 --> PKL
    M1 --> CSV1
    NextJS -->|"Prisma Client"| PG

    style PL fill:#EEF2FF,stroke:#6366F1,stroke-width:2px
    style AL fill:#FEF3C7,stroke:#F59E0B,stroke-width:2px
    style DL fill:#ECFDF5,stroke:#10B981,stroke-width:2px
    style FastAPI fill:#009688,stroke:#00796B,color:#fff
    style NextJS fill:#000,stroke:#333,color:#fff
    style Ollama fill:#FF6F00,stroke:#E65100,color:#fff
    style PG fill:#336791,stroke:#234B6E,color:#fff
```

---

## 2. Use Case Diagram

```mermaid
flowchart LR
    subgraph Actors[" "]
        Student(["👤 Student\n(Primary Actor)"])
        Admin(["👤 Admin\n(Future Actor)"])
    end

    subgraph System["Skill Lantern System"]
        UC1["Register &\nCreate Profile"]
        UC2["Login"]
        UC3["Logout"]
        UC4["View Career\nPredictions"]
        UC5["View Career\nRoadmap"]
        UC6["View College\nRecommendations"]
        UC7["View Career\nSummary"]
        UC8["Get Full\nRecommendations"]
        UC9["Manage Users"]
        UC10["Update College\nDataset"]
    end

    Student --- UC1
    Student --- UC2
    Student --- UC3
    Student --- UC4
    Student --- UC5
    Student --- UC6
    Student --- UC7
    Student --- UC8

    Admin --- UC9
    Admin --- UC10

    UC1 -. "<<includes>>" .-> UC2
    UC4 -. "<<includes>>" .-> UC2
    UC5 -. "<<extends>>" .-> UC4
    UC6 -. "<<extends>>" .-> UC4
    UC7 -. "<<extends>>" .-> UC4
    UC8 -. "<<includes>>" .-> UC4
    UC8 -. "<<includes>>" .-> UC5
    UC8 -. "<<includes>>" .-> UC6

    style System fill:#EEF2FF,stroke:#6366F1,stroke-width:2px
```

---

## 3. Activity Diagram — User Registration and Profile Creation

```mermaid
flowchart TD
    Start(["▶ Start"]) --> A["Enter Personal Info\n(Name, Email, Password,\nGender, DOB, City)"]
    A --> B["Enter Education Details\n(Course Category, Course,\nSpecialisation, College, CGPA)"]
    B --> C["Select Technical Skills\n(Multi-Select Checkboxes)"]
    C --> D["Select Soft Skills\n(Multi-Select)"]
    D --> E["Select Interests\n(Multi-Select Checkboxes)"]
    E --> F["Enter Certifications\n(Yes/No + Details)"]
    F --> G["Set Career Preferences\n(Lifestyle, Work Env,\nLocation, Learning Style)"]
    G --> H{"All Fields\nValid?"}

    H -->|No| I["Display Validation\nErrors"]
    I --> A

    H -->|Yes| J["Submit Registration"]
    J --> K["Hash Password\n(bcryptjs)"]
    K --> L["Create User Account\n(PostgreSQL via Prisma)"]
    L --> M["Store User Profile\n(PostgreSQL via Prisma)"]
    M --> N["Send Profile to\nFastAPI Backend"]
    N --> O["Generate Career\nPredictions (XGBoost)"]
    O --> P["Save Predictions\nto Database"]
    P --> Q["Redirect to\nDashboard"]
    Q --> End(["⏹ End"])

    style Start fill:#10B981,stroke:#059669,color:#fff
    style End fill:#EF4444,stroke:#DC2626,color:#fff
    style H fill:#F59E0B,stroke:#D97706,color:#fff
```

---

## 4. Activity Diagram — Career Recommendation Generation

```mermaid
flowchart TD
    Start(["▶ Start"]) --> A["Receive User Profile\nfrom Frontend"]
    A --> B{"XGBoost Model\nLoaded?"}

    B -->|Yes| C["Encode Features\n(Gender, Course, CGPA,\nSkills, Interests)"]
    C --> D["Run XGBoost\npredict_proba()"]
    D --> E["Get Probability Distribution\nacross 24 Career Categories"]
    E --> F["Sort & Select\nTop-K Predictions"]

    B -->|No| G["Run Rule-Based\nFallback System"]
    G --> H["Score Careers using\n50+ Skill-to-Career Mappings"]
    H --> I["Normalise Confidence\nScores"]
    I --> F

    F --> J["Return Career Predictions\nwith Confidence Scores"]
    J --> End(["⏹ End"])

    style Start fill:#10B981,stroke:#059669,color:#fff
    style End fill:#EF4444,stroke:#DC2626,color:#fff
    style B fill:#F59E0B,stroke:#D97706,color:#fff
```

---

## 5. Activity Diagram — Full Recommendation Flow (Prediction + Roadmap + Colleges)

```mermaid
flowchart TD
    Start(["▶ Start"]) --> A["Receive User Profile\n& Preferences"]

    A --> B["Step 1: Career Prediction"]
    B --> C{"XGBoost\nAvailable?"}
    C -->|Yes| D["XGBoost predict_proba()"]
    C -->|No| E["Rule-Based Fallback"]
    D --> F["Top Careers +\nConfidence Scores"]
    E --> F

    F --> G["Select Top Career"]
    G --> H["Step 2: Roadmap Generation"]
    H --> I{"Ollama\nAvailable?"}
    I -->|Yes| J["Send Roadmap Prompt\nto LLaMA 3"]
    J --> K["Parse 3-Stage Roadmap\n(Beginner, Intermediate, Advanced)"]
    I -->|No| L["Skip Roadmap\n(Graceful Degradation)"]

    K --> M["Step 3: College Recommendations"]
    L --> M
    M --> N["Filter colleges.csv by\nCareer, Location, Budget"]
    N --> O{"Ollama\nAvailable?"}
    O -->|Yes| P["Generate College\nExplanations via LLaMA 3"]
    O -->|No| Q["Return Colleges\nwithout LLM Explanations"]

    P --> R["Step 4: Career Summary"]
    Q --> R
    R --> S{"Ollama\nAvailable?"}
    S -->|Yes| T["Generate Personalised\nSummary via LLaMA 3"]
    S -->|No| U["Skip Summary"]

    T --> V["Assemble Full\nRecommendation Response"]
    U --> V
    V --> W["Return to Frontend\n& Save to PostgreSQL"]
    W --> End(["⏹ End"])

    style Start fill:#10B981,stroke:#059669,color:#fff
    style End fill:#EF4444,stroke:#DC2626,color:#fff
    style C fill:#F59E0B,stroke:#D97706,color:#fff
    style I fill:#F59E0B,stroke:#D97706,color:#fff
    style O fill:#F59E0B,stroke:#D97706,color:#fff
    style S fill:#F59E0B,stroke:#D97706,color:#fff
```

---

## 6. Sequence Diagram — Career Prediction Flow

```mermaid
sequenceDiagram
    actor User
    participant Frontend as Next.js Frontend
    participant APIRoute as API Route Proxy<br/>(/api/users/recommendations)
    participant Backend as FastAPI Backend<br/>(/api/predict)
    participant Predictor as CareerPredictor
    participant XGBoost as XGBoost Model
    participant Fallback as Rule-Based Fallback

    User->>Frontend: Submit profile form
    Frontend->>APIRoute: POST /api/users/recommendations
    APIRoute->>Backend: POST /api/predict (UserProfile JSON)

    Backend->>Predictor: predict(user_profile)

    alt XGBoost Model Loaded
        Predictor->>Predictor: Encode features<br/>(gender, course, CGPA, skills, interests)
        Predictor->>XGBoost: model.predict_proba(features)
        XGBoost-->>Predictor: Probability distribution (24 classes)
        Predictor->>Predictor: Sort by confidence, select top-k
    else Model Not Available
        Predictor->>Fallback: rule_based_predict(skills, interests)
        Fallback->>Fallback: Score careers by skill-career mapping
        Fallback-->>Predictor: Top careers with normalised scores
    end

    Predictor-->>Backend: List[PredictedCareer]
    Backend-->>APIRoute: CareerPredictionResponse (JSON)
    APIRoute-->>Frontend: Career predictions
    Frontend-->>User: Display predictions on Dashboard
```

---

## 7. Sequence Diagram — Full Recommendation Flow

```mermaid
sequenceDiagram
    actor User
    participant Frontend as Next.js Frontend
    participant APIRoute as API Route Proxy
    participant Backend as FastAPI Backend
    participant RecService as RecommendationService
    participant Predictor as CareerPredictor
    participant Ollama as Ollama / LLaMA 3
    participant ColService as CollegeService
    participant DB as PostgreSQL

    User->>Frontend: Click "Get Full Details"
    Frontend->>APIRoute: POST /api/users/recommendations
    APIRoute->>Backend: POST /api/recommendations/full

    Backend->>RecService: get_full_recommendation(profile, preferences)

    Note over RecService: Step 1: Career Prediction
    RecService->>Predictor: predict(user_profile)
    Predictor-->>RecService: Top careers + confidence scores

    Note over RecService: Step 2: Roadmap Generation
    RecService->>Ollama: generate(roadmap_prompt)
    Ollama-->>RecService: 3-stage roadmap JSON

    Note over RecService: Step 3: College Recommendations
    RecService->>ColService: get_colleges(career, location, budget)
    ColService-->>RecService: Filtered college list
    RecService->>Ollama: generate(college_explanation_prompt)
    Ollama-->>RecService: College explanations

    Note over RecService: Step 4: Career Summary
    RecService->>Ollama: generate(summary_prompt)
    Ollama-->>RecService: Personalised summary text

    RecService-->>Backend: FullRecommendationResponse
    Backend-->>APIRoute: JSON response
    APIRoute-->>Frontend: Full recommendation data

    Frontend->>DB: Save recommendation (via API route)
    DB-->>Frontend: Confirmation

    Frontend-->>User: Display Dashboard<br/>(Predictions + Roadmap + Colleges)
```

---

## 8. Entity Relationship (ER) Diagram

```mermaid
erDiagram
    User {
        string id PK "cuid()"
        string name
        string email UK
        datetime emailVerified
        string image
        string password "bcrypt hashed"
        datetime createdAt
        datetime updatedAt
    }

    UserProfile {
        string id PK "cuid()"
        string userId FK UK
        string fullName
        string gender
        datetime dateOfBirth
        string cityRegion
        string courseCategory
        string course
        string specialization
        string schoolCollegeName
        float cgpa
        string_array interests
        string_array technicalSkills
        string_array softSkills
        boolean hasCertification
        string certifications
        string careerLifestyle
        string workEnvironment
        string locationPreference
        string learningStyle
        datetime createdAt
        datetime updatedAt
    }

    CareerRecommendation {
        string id PK "cuid()"
        string userId FK
        json predictions "career + confidence array"
        string topCareer
        json roadmap "stages + tools + roles"
        json colleges "college recommendations"
        string summary "LLM-generated text"
        string_array immediateActions
        boolean hasFullDetails
        datetime createdAt
        datetime updatedAt
    }

    Account {
        string id PK "cuid()"
        string userId FK
        string type
        string provider
        string providerAccountId
        string refresh_token
        string access_token
        int expires_at
    }

    Session {
        string id PK "cuid()"
        string sessionToken UK
        string userId FK
        datetime expires
    }

    VerificationToken {
        string identifier
        string token UK
        datetime expires
    }

    User ||--o| UserProfile : "has one"
    User ||--o{ CareerRecommendation : "has many"
    User ||--o{ Account : "has many"
    User ||--o{ Session : "has many"
```

---

## 9. Class Diagram

```mermaid
classDiagram
    class CareerPredictor {
        -model: XGBClassifier
        -model_loaded: bool
        -label_encoder: LabelEncoder
        -feature_columns: list
        -encoders: dict
        -career_data: DataFrame
        -skill_career_map: dict
        +load_model() bool
        +load_career_data() bool
        +predict(UserProfile, top_n) List~PredictedCareer~
        +rule_based_predict(skills, interests) List~PredictedCareer~
        +get_career_insights(career_name) dict
        -_build_skill_career_map() dict
        -_encode_features(UserProfile) ndarray
    }

    class OllamaService {
        -base_url: str
        -model: str
        -timeout: float
        +check_health() bool
        +list_models() list
        +generate(prompt, system_prompt, temperature, max_tokens) str
        +generate_stream(prompt, system_prompt, temperature) AsyncGenerator
        +chat(messages, temperature) str
        +parse_json_response(response) dict
    }

    class CollegeService {
        -college_data: DataFrame
        -data_loaded: bool
        +load_data() bool
        +get_colleges(career, location, budget, degree) List~CollegeInfo~
        -_filter_by_programme(career) DataFrame
        -_filter_by_location(location) DataFrame
    }

    class RecommendationService {
        -career_predictor: CareerPredictor
        -ollama_service: OllamaService
        -college_service: CollegeService
        -roadmap_service: RoadmapService
        +get_full_recommendation(profile, preferences) FullRecommendationResponse
    }

    class RoadmapService {
        -ollama_service: OllamaService
        +generate_roadmap(career, profile) RoadmapResponse
        -_build_prompt(career, profile) str
    }

    class UserProfile {
        +name: str
        +gender: str
        +education_level: EducationLevel
        +ug_course: str
        +specialization: str
        +skills: List~str~
        +interests: List~str~
        +cgpa: float
        +certifications: List~str~
        +location: str
    }

    class PredictedCareer {
        +career: str
        +confidence: float
        +description: str
    }

    class CareerPredictionResponse {
        +predictions: List~PredictedCareer~
        +user_profile_summary: dict
        +message: str
    }

    class FullRecommendationResponse {
        +predicted_careers: List~PredictedCareer~
        +selected_career: str
        +roadmap: RoadmapResponse
        +colleges: CollegeRecommendationResponse
        +summary: str
        +immediate_actions: List~str~
    }

    class RoadmapResponse {
        +career: str
        +overview: str
        +stages: List~RoadmapStage~
        +tools_and_technologies: List~str~
        +job_roles: List~str~
    }

    class RoadmapStage {
        +level: str
        +duration: str
        +skills: List~str~
        +resources: List~str~
        +milestones: List~str~
    }

    RecommendationService --> CareerPredictor : uses
    RecommendationService --> OllamaService : uses
    RecommendationService --> CollegeService : uses
    RecommendationService --> RoadmapService : uses
    RoadmapService --> OllamaService : uses
    CareerPredictor ..> UserProfile : accepts
    CareerPredictor ..> PredictedCareer : returns
    CareerPredictor ..> CareerPredictionResponse : returns
    RoadmapService ..> RoadmapResponse : returns
    RoadmapResponse *-- RoadmapStage : contains
    RecommendationService ..> FullRecommendationResponse : returns
```

---

## 10. Gantt Chart (Mid-Year Timeline)

```mermaid
gantt
    title Skill Lantern — Mid-Year Project Timeline
    dateFormat YYYY-MM-DD
    axisFormat %b %Y
    todayMarker stroke-width:3px,stroke:#f00

    section Planning
    Project Initiation & Proposal        :done, p1, 2025-06-01, 2025-07-12
    Literature Review                    :done, p2, 2025-07-13, 2025-09-06

    section AI Development
    Dataset Analysis & Feature Eng.      :done, a1, 2025-08-17, 2025-09-27
    XGBoost Model Training & Tuning      :done, a2, 2025-09-28, 2025-11-08
    Model Evaluation (Cross-Val)         :done, a3, 2025-10-26, 2025-11-15

    section Backend Development
    FastAPI API Development              :done, b1, 2025-10-12, 2025-12-06
    Ollama / LLaMA 3 Integration         :done, b2, 2025-11-09, 2025-12-06
    Service Layer & Orchestration        :done, b3, 2025-11-23, 2025-12-20

    section Frontend Development
    Next.js Setup & Landing Page         :done, f1, 2025-11-09, 2025-12-06
    Multi-Step Registration Form         :done, f2, 2025-12-07, 2026-01-03
    Authentication (NextAuth.js v5)      :done, f3, 2025-12-21, 2026-01-10
    Dashboard & Results Display          :done, f4, 2026-01-04, 2026-01-31
    Database Integration (Prisma)        :done, f5, 2026-01-11, 2026-02-01

    section Testing & Refinement
    Integration Testing                  :done, t1, 2026-01-18, 2026-02-14
    Bug Fixes & UX Refinement            :active, t2, 2026-02-01, 2026-03-14

    section Documentation
    Mid-Year Report                      :active, d1, 2026-02-22, 2026-03-14

    section Remaining Work
    Comprehensive Model Evaluation       :r1, 2026-03-15, 2026-03-28
    UI Responsiveness & Polish           :r2, 2026-03-15, 2026-03-28
    User Acceptance Testing              :r3, 2026-03-22, 2026-04-05
    Final Report & Submission            :r4, 2026-03-29, 2026-04-18
    Presentation Preparation             :r5, 2026-04-12, 2026-04-18
```

---

## Instructions for Exporting

1. Go to **[mermaid.live](https://mermaid.live)**
2. Paste one code block at a time (without the triple backticks)
3. The diagram renders on the right panel
4. Click the **Export** button (download icon) → choose **PNG** or **SVG**
5. Insert the exported image into the DOCX report at the matching red `[INSERT SCREENSHOT: ...]` placeholder
