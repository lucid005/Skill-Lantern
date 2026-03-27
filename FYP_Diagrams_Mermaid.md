# Skill Lantern — FYP Report Diagrams (Mermaid Live Editor Code)

> **How to use:** Copy each code block into [Mermaid Live Editor](https://mermaid.live) to render and export as PNG/SVG for your report.

---

## Figure 1: Functional Decomposition Diagram (FDD)

```mermaid
graph TD
    A["<b>Skill Lantern</b><br/>AI-Powered Career Guidance System"]

    A --> B["<b>User Management<br/>Subsystem</b>"]
    A --> C["<b>Career Prediction<br/>Subsystem</b>"]
    A --> D["<b>Roadmap Generation<br/>Subsystem</b>"]
    A --> E["<b>College Recommendation<br/>Subsystem</b>"]
    A --> F["<b>Recommendation<br/>Orchestration Subsystem</b>"]

    B --> B1["User Registration<br/>(Multi-step Signup)"]
    B --> B2["Authentication<br/>(NextAuth.js v5)"]
    B --> B3["Profile Storage<br/>(PostgreSQL / Prisma)"]

    C --> C1["XGBoost Model<br/>Inference"]
    C --> C2["Rule-Based<br/>Fallback"]
    C --> C3["Confidence<br/>Scoring"]
    C --> C4["Feature<br/>Encoding"]

    D --> D1["LLaMA 3 Prompt<br/>Engineering"]
    D --> D2["3-Stage Roadmap<br/>Structuring"]
    D --> D3["JSON Response<br/>Parsing"]

    E --> E1["CSV Data<br/>Loading"]
    E --> E2["Location / Budget<br/>Filtering"]
    E --> E3["LLM-Enhanced<br/>Explanations"]

    F --> F1["Career Prediction<br/>Coordination"]
    F --> F2["Roadmap<br/>Coordination"]
    F --> F3["College<br/>Coordination"]
    F --> F4["Summary<br/>Generation"]

    style A fill:#4F46E5,stroke:#3730A3,color:#fff,stroke-width:2px
    style B fill:#7C3AED,stroke:#6D28D9,color:#fff
    style C fill:#7C3AED,stroke:#6D28D9,color:#fff
    style D fill:#7C3AED,stroke:#6D28D9,color:#fff
    style E fill:#7C3AED,stroke:#6D28D9,color:#fff
    style F fill:#7C3AED,stroke:#6D28D9,color:#fff
```

---

## Figure 2: System Architecture Diagram

```mermaid
graph TB
    subgraph PL["<b>Presentation Layer</b>"]
        Browser["🌐 Browser"]
        NextJS["<b>Next.js 16 Frontend</b><br/>React 19 · TypeScript · Tailwind CSS 4"]
        Pages["Pages:<br/>Landing · Signup · Login · Dashboard"]
    end

    subgraph AL["<b>Application Layer</b>"]
        FastAPI["<b>FastAPI Backend</b><br/>Python · Uvicorn ASGI"]

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
            M1["CareerPredictor<br/>(XGBoost)"]
            M2["Rule-Based<br/>Fallback"]
        end
    end

    subgraph DL["<b>Data Layer</b>"]
        PG["PostgreSQL<br/>(via Prisma ORM)"]
        CSV1["career_recommender.csv"]
        CSV2["colleges.csv"]
        PKL["Model Artefacts<br/>(.pkl files)"]
        Ollama["Ollama Server<br/>(LLaMA 3)"]
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

## Figure 3: Sequence Diagram — Career Prediction Flow

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

## Figure 4: Sequence Diagram — Full Recommendation Flow

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

    User->>Frontend: Click "Get Recommendations"
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

## Figure 5: Activity Diagram — User Registration and Profile Creation

```mermaid
flowchart TD
    Start(["▶ Start"]) --> A["Enter Personal Info<br/>(Name, Gender, DOB, City)"]
    A --> B["Enter Education Details<br/>(Course, Specialisation, College, CGPA)"]
    B --> C["Select Technical Skills<br/>(Multi-Select)"]
    C --> D["Select Soft Skills<br/>(Multi-Select)"]
    D --> E["Select Interests<br/>(Multi-Select)"]
    E --> F["Enter Certifications"]
    F --> G["Set Career Preferences<br/>(Lifestyle, Work Env, Location, Learning Style)"]
    G --> H{"All Fields<br/>Valid?"}

    H -->|No| I["Display Validation<br/>Errors"]
    I --> A

    H -->|Yes| J["Submit Registration"]
    J --> K["Hash Password<br/>(bcrypt)"]
    K --> L["Create User Account<br/>(PostgreSQL)"]
    L --> M["Store User Profile<br/>(PostgreSQL)"]
    M --> N["Send Profile to<br/>FastAPI Backend"]
    N --> O["Generate Career<br/>Recommendations"]
    O --> P["Save Recommendations<br/>to Database"]
    P --> Q["Redirect to<br/>Dashboard"]
    Q --> End(["⏹ End"])

    style Start fill:#10B981,stroke:#059669,color:#fff
    style End fill:#EF4444,stroke:#DC2626,color:#fff
    style H fill:#F59E0B,stroke:#D97706,color:#fff
```

---

## Figure 6: Activity Diagram — Career Recommendation Generation

```mermaid
flowchart TD
    Start(["▶ Start"]) --> A["Receive User Profile"]
    A --> B{"XGBoost Model<br/>Loaded?"}

    B -->|Yes| C["Encode Features<br/>(Gender, Course, CGPA,<br/>Skills, Interests)"]
    C --> D["Run XGBoost<br/>predict_proba()"]
    D --> E["Get Top-K Careers<br/>with Confidence Scores"]

    B -->|No| F["Run Rule-Based<br/>Fallback"]
    F --> G["Score Careers by<br/>Skill-Career Mapping"]
    G --> H["Normalise Confidence<br/>Scores"]
    H --> E

    E --> I["Select Top Career"]
    I --> J{"Ollama<br/>Available?"}

    J -->|Yes| K["Generate Roadmap<br/>via LLaMA 3"]
    K --> L["Parse Roadmap<br/>JSON Response"]
    L --> M["Query College<br/>Dataset (CSV)"]

    J -->|No| M

    M --> N["Filter Colleges by<br/>Location / Budget / Programme"]
    N --> O{"Ollama<br/>Available?"}

    O -->|Yes| P["Generate College<br/>Explanations via LLaMA 3"]
    P --> Q["Generate Career<br/>Summary via LLaMA 3"]
    Q --> R["Assemble Full<br/>Recommendation Response"]

    O -->|No| R

    R --> S["Return to Frontend"]
    S --> End(["⏹ End"])

    style Start fill:#10B981,stroke:#059669,color:#fff
    style End fill:#EF4444,stroke:#DC2626,color:#fff
    style B fill:#F59E0B,stroke:#D97706,color:#fff
    style J fill:#F59E0B,stroke:#D97706,color:#fff
    style O fill:#F59E0B,stroke:#D97706,color:#fff
```

---

## Figure 7: Use Case Diagram

```mermaid
flowchart LR
    subgraph Actors
        Student(["👤 Student<br/>(Primary Actor)"])
        Admin(["👤 Admin<br/>(Future Actor)"])
    end

    subgraph System["<b>Skill Lantern System</b>"]
        UC1["Register &<br/>Create Profile"]
        UC2["Login"]
        UC3["Logout"]
        UC4["View Career<br/>Predictions"]
        UC5["View Career<br/>Roadmap"]
        UC6["View College<br/>Recommendations"]
        UC7["View Career<br/>Summary"]
        UC8["Update Profile"]
        UC9["Manage Users"]
        UC10["Update College<br/>Dataset"]
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

    style System fill:#EEF2FF,stroke:#6366F1,stroke-width:2px
```

---

## Figure 8: Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    User {
        string id PK "cuid()"
        string name
        string email UK
        datetime emailVerified
        string image
        string password
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
        json predictions "Array of career + confidence"
        string topCareer
        json roadmap "stages, tools, job_roles"
        json colleges "recommendations list"
        string summary
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
        string token_type
        string scope
        string id_token
        string session_state
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

## Figure 9: Class Diagram

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
        +predict(UserProfile) List~PredictedCareer~
        +rule_based_predict(skills, interests) List~PredictedCareer~
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
        +preferences: str
        +cgpa: float
        +certifications: List~str~
        +location: str
    }

    class CareerPredictionResponse {
        +predictions: List~PredictedCareer~
        +user_profile_summary: dict
        +message: str
    }

    class PredictedCareer {
        +career: str
        +confidence: float
        +description: str
    }

    class RoadmapResponse {
        +career: str
        +overview: str
        +stages: List~RoadmapStage~
        +tools_and_technologies: List~str~
        +job_roles: List~str~
        +growth_paths: List~str~
    }

    class RoadmapStage {
        +level: str
        +duration: str
        +skills: List~str~
        +resources: List~str~
        +milestones: List~str~
    }

    class FullRecommendationResponse {
        +predicted_careers: List~PredictedCareer~
        +selected_career: str
        +roadmap: RoadmapResponse
        +colleges: CollegeRecommendationResponse
        +summary: str
        +immediate_actions: List~str~
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
    FullRecommendationResponse *-- RoadmapResponse : contains
```

---

## Figure 10: XGBoost Training Pipeline Flow

```mermaid
flowchart LR
    A["📂 career_recommender.csv"] --> B["Load &<br/>Clean Data"]
    B --> C["Extract Job Titles<br/>& Map to 24<br/>Career Categories"]
    C --> D["Remove Students /<br/>Unemployed / Rare<br/>Categories"]
    D --> E["Feature Engineering"]

    subgraph FE["Feature Engineering"]
        E1["Gender →<br/>LabelEncoder"]
        E2["UG Course →<br/>LabelEncoder"]
        E3["CGPA →<br/>Normalise /100"]
        E4["Skills →<br/>Top 50 Binary"]
        E5["Interests →<br/>Top 30 Binary"]
        E6["Certifications →<br/>Binary 0/1"]
    end

    E --> FE

    FE --> F["Stratified Split<br/>80% Train / 20% Test"]
    F --> G["5-Fold Cross<br/>Validation"]
    F --> H["Train XGBoost<br/>(500 trees, depth=8,<br/>lr=0.05, softprob)"]
    H --> I["Evaluate:<br/>Accuracy, Top-3,<br/>Top-5, F1, CM"]
    I --> J["Save Artefacts<br/>(model.pkl,<br/>encoders.pkl)"]

    style A fill:#3B82F6,stroke:#2563EB,color:#fff
    style J fill:#10B981,stroke:#059669,color:#fff
```

---

## Figure 11: Data Flow Diagram (DFD Level 0 — Context)

```mermaid
flowchart LR
    Student(["👤 Student"])
    Admin(["👤 Admin"])

    subgraph System["<b>Skill Lantern System</b>"]
        SL["Career Guidance<br/>Processing"]
    end

    CollegeCSV[("colleges.csv")]
    CareerCSV[("career_recommender.csv")]
    DB[("PostgreSQL<br/>Database")]
    LLM["Ollama /<br/>LLaMA 3"]

    Student -->|"Profile Data<br/>(skills, interests, education)"| SL
    SL -->|"Career Predictions,<br/>Roadmap, Colleges"| Student

    Admin -->|"Update College<br/>Dataset"| CollegeCSV

    CareerCSV -->|"Training Data"| SL
    CollegeCSV -->|"College Records"| SL
    SL <-->|"User & Recommendation<br/>Data"| DB
    SL <-->|"NLG Prompts /<br/>Responses"| LLM

    style System fill:#EEF2FF,stroke:#6366F1,stroke-width:2px
    style SL fill:#4F46E5,stroke:#3730A3,color:#fff
```

---

## Figure 12: Deployment Diagram

```mermaid
graph TB
    subgraph Client["<b>Client Machine</b>"]
        Browser["🌐 Web Browser"]
    end

    subgraph Server["<b>Development / Deployment Machine</b>"]
        subgraph FrontendServer["<b>Frontend Server (Port 3000)</b>"]
            Next["Next.js 16<br/>Node.js Runtime"]
            NextAuth["NextAuth.js v5<br/>Session Management"]
            Prisma["Prisma Client<br/>ORM"]
        end

        subgraph BackendServer["<b>Backend Server (Port 8000)</b>"]
            UVICORN["Uvicorn ASGI Server"]
            FAPI["FastAPI Application"]
            XGB["XGBoost Model<br/>(in-memory)"]
        end

        subgraph OllamaServer["<b>Ollama Server (Port 11434)</b>"]
            OLL["Ollama Runtime"]
            LLAMA["LLaMA 3 Model"]
        end

        subgraph Database["<b>PostgreSQL (Port 5432)</b>"]
            PG["PostgreSQL Database"]
        end

        subgraph FileSystem["<b>File System</b>"]
            CSV1["career_recommender.csv"]
            CSV2["colleges.csv"]
            PKL1["xgboost_model.pkl"]
            PKL2["label_encoder.pkl"]
            PKL3["encoders.pkl"]
        end
    end

    Browser -->|"HTTPS"| Next
    Next -->|"Internal API Calls"| FAPI
    Next --> NextAuth --> Prisma --> PG
    UVICORN --> FAPI
    FAPI -->|"httpx async"| OLL
    OLL --> LLAMA
    FAPI --> XGB
    XGB --> PKL1
    FAPI --> CSV1
    FAPI --> CSV2

    style Client fill:#F3F4F6,stroke:#9CA3AF,stroke-width:2px
    style Server fill:#FFF7ED,stroke:#FB923C,stroke-width:2px
    style FrontendServer fill:#000,stroke:#333,color:#fff
    style BackendServer fill:#009688,stroke:#00796B,color:#fff
    style OllamaServer fill:#FF6F00,stroke:#E65100,color:#fff
    style Database fill:#336791,stroke:#234B6E,color:#fff
```

---

## Figure 13: Gantt Chart

```mermaid
gantt
    title Skill Lantern — Project Timeline
    dateFormat  YYYY-MM-DD
    axisFormat  %b %Y

    section Planning
    Project Initiation & Proposal       :done, p1, 2025-06-01, 6w
    Literature Review                   :done, p2, 2025-07-13, 8w

    section AI Development
    Dataset Analysis & Feature Engineering :done, a1, 2025-08-17, 6w
    Model Training & Evaluation          :done, a2, 2025-09-28, 6w
    Hyperparameter Tuning               :done, a3, 2025-10-26, 3w

    section Backend
    FastAPI API Development              :done, b1, 2025-10-12, 8w
    Ollama / LLaMA 3 Integration         :done, b2, 2025-11-09, 4w
    Service Layer & Orchestration        :done, b3, 2025-11-23, 4w

    section Frontend
    Next.js Setup & Landing Page         :done, f1, 2025-11-09, 4w
    Multi-Step Registration Form         :done, f2, 2025-12-07, 4w
    Authentication (NextAuth.js)         :done, f3, 2025-12-21, 3w
    Dashboard & Results Display          :done, f4, 2026-01-04, 4w

    section Testing & Docs
    Integration Testing                  :done, t1, 2026-01-18, 4w
    Bug Fixes & UX Refinement            :done, t2, 2026-02-01, 3w
    Draft Report                         :done, d1, 2026-01-25, 5w
    Final Report & Submission            :active, d2, 2026-02-22, 2w
```

---

## Figure 14: Landing Page Wireframe (Low-Fidelity)

```mermaid
block-beta
    columns 3

    block:header:3
        columns 3
        logo["🔦 Skill Lantern"] space:1 nav["Home | Features | Contact | Login"]
    end

    space:3

    block:hero:3
        columns 1
        h1["AI-Powered Career Guidance<br/>for Nepal"]
        subtitle["Discover your ideal career path with<br/>machine learning recommendations"]
        cta["[ Get Started → ]"]
    end

    space:3

    block:features:3
        columns 3
        f1["🎯<br/>Career Prediction<br/>XGBoost ML Model"]
        f2["🗺️<br/>Learning Roadmap<br/>3-Stage Path"]
        f3["🏫<br/>College Finder<br/>1,400+ Institutions"]
    end

    space:3

    block:footer:3
        columns 1
        foot["© 2026 Skill Lantern | Privacy | Terms"]
    end
```

---

## Figure 15: Signup Form Wireframe (Multi-Step)

```mermaid
flowchart LR
    subgraph Step1["Step 1: Personal Info"]
        S1F1["Full Name: [________]"]
        S1F2["Gender: [Dropdown ▼]"]
        S1F3["Date of Birth: [__/__/____]"]
        S1F4["City/Region: [________]"]
    end

    subgraph Step2["Step 2: Education"]
        S2F1["Course Category: [Dropdown ▼]"]
        S2F2["Course: [________]"]
        S2F3["Specialisation: [________]"]
        S2F4["College Name: [________]"]
        S2F5["CGPA: [____]"]
    end

    subgraph Step3["Step 3: Skills"]
        S3F1["Technical Skills:<br/>☐ Python  ☐ JavaScript<br/>☐ React  ☐ SQL<br/>☐ Machine Learning<br/>☐ ...more"]
    end

    subgraph Step4["Step 4: Interests"]
        S4F1["Interests:<br/>☐ Web Development<br/>☐ Data Science<br/>☐ Cybersecurity<br/>☐ AI/ML<br/>☐ ...more"]
    end

    subgraph Step5["Step 5: Certifications"]
        S5F1["Has Certifications? [Yes/No]"]
        S5F2["Certification Details:<br/>[________________]"]
    end

    subgraph Step6["Step 6: Preferences"]
        S6F1["Career Lifestyle: [Dropdown ▼]"]
        S6F2["Work Environment: [Dropdown ▼]"]
        S6F3["Location Pref: [Dropdown ▼]"]
        S6F4["Learning Style: [Dropdown ▼]"]
    end

    Step1 -->|"Next →"| Step2
    Step2 -->|"Next →"| Step3
    Step3 -->|"Next →"| Step4
    Step4 -->|"Next →"| Step5
    Step5 -->|"Next →"| Step6
    Step6 -->|"Submit ✓"| Done(["Registration<br/>Complete"])

    style Done fill:#10B981,stroke:#059669,color:#fff
```

---

## Figure 16: Dashboard Wireframe

```mermaid
flowchart TD
    subgraph Header["<b>Dashboard Header</b>"]
        Logo["🔦 Skill Lantern"]
        Welcome["Welcome, Saurav"]
        Logout["Logout"]
    end

    subgraph Predictions["<b>Career Predictions</b>"]
        P1["🥇 Software Engineer<br/>Confidence: 42%<br/>████████░░"]
        P2["🥈 Web Developer<br/>Confidence: 28%<br/>█████░░░░░"]
        P3["🥉 Data Scientist<br/>Confidence: 15%<br/>███░░░░░░░"]
    end

    subgraph Roadmap["<b>Career Roadmap</b>"]
        Tab1["Beginner"]
        Tab2["Intermediate"]
        Tab3["Advanced"]
        Content["Duration: 3-6 months<br/>Skills: HTML, CSS, JS, Git<br/>Resources: freeCodeCamp, MDN<br/>Milestones: Build portfolio site"]
    end

    subgraph Colleges["<b>College Recommendations</b>"]
        C1["📍 Kathmandu Engineering College<br/>Location: Kathmandu<br/>Programme: BCS, BIT"]
        C2["📍 Tribhuvan University<br/>Location: Kirtipur<br/>Programme: BSc CSIT"]
    end

    Header --> Predictions
    Predictions --> Roadmap
    Roadmap --> Colleges
```

---

## Figure 17: XGBoost Ensemble Visualisation (Conceptual)

```mermaid
flowchart LR
    Input["📊 User Features<br/>(85+ features)"]

    Input --> T1["🌲 Tree 1"]
    Input --> T2["🌲 Tree 2"]
    Input --> T3["🌲 Tree 3"]
    Input --> TN["🌲 ... Tree 500"]

    T1 -->|"Residual<br/>Correction"| T2
    T2 -->|"Residual<br/>Correction"| T3
    T3 -->|"Residual<br/>Correction"| TN

    T1 --> Sum["∑ Weighted<br/>Sum"]
    T2 --> Sum
    T3 --> Sum
    TN --> Sum

    Sum --> Softmax["Softmax<br/>P(class_i)"]
    Softmax --> Output["📋 24 Career<br/>Probabilities"]

    Output --> Top["Top-K<br/>Predictions"]

    style Input fill:#3B82F6,stroke:#2563EB,color:#fff
    style Sum fill:#F59E0B,stroke:#D97706,color:#fff
    style Softmax fill:#8B5CF6,stroke:#7C3AED,color:#fff
    style Output fill:#10B981,stroke:#059669,color:#fff
```

---

## Figure 18: State Diagram — User Session

```mermaid
stateDiagram-v2
    [*] --> Unauthenticated

    Unauthenticated --> Registration : Click Sign Up
    Registration --> ProfileCreation : Submit Credentials
    ProfileCreation --> Authenticated : Complete 6-Step Form

    Unauthenticated --> Authenticated : Login (valid credentials)
    Unauthenticated --> Unauthenticated : Login (invalid credentials)

    Authenticated --> ViewingPredictions : Open Dashboard
    ViewingPredictions --> ViewingRoadmap : Click Roadmap Tab
    ViewingRoadmap --> ViewingColleges : Click Colleges Tab
    ViewingColleges --> ViewingPredictions : Click Predictions Tab

    Authenticated --> Unauthenticated : Logout
    Authenticated --> Unauthenticated : Session Expired

    state Authenticated {
        [*] --> Dashboard
        Dashboard --> ViewingPredictions
        Dashboard --> ViewingRoadmap
        Dashboard --> ViewingColleges
    }
```

---

## Figure 19: Component Diagram — Frontend Architecture

```mermaid
graph TB
    subgraph NextApp["<b>Next.js 16 App (App Router)</b>"]
        subgraph MainRoutes["(main) Routes"]
            Landing["page.tsx<br/>Landing Page"]
            Features["features/page.tsx"]
            HowItWorks["howitworks/page.tsx"]
            Contact["contact/page.tsx"]
        end

        subgraph AuthRoutes["(auth) Routes"]
            Login["login/page.tsx"]
            Signup["signup/page.tsx<br/>(1240 lines, 6 steps)"]
        end

        subgraph DashRoutes["(dashboard) Routes"]
            Dashboard["dashboard/page.tsx<br/>(742 lines)"]
        end

        subgraph APIRoutes["API Routes"]
            AuthAPI["api/auth/[...nextauth]<br/>route.ts"]
            SignupAPI["api/auth/signup<br/>route.ts"]
            UsersAPI["api/users<br/>route.ts"]
            ProfileAPI["api/users/profile<br/>route.ts"]
            RecsAPI["api/users/recommendations<br/>route.ts"]
        end

        subgraph Components["Shared Components"]
            Navbar["Navbar.tsx"]
            Footer["Footer.tsx"]
            Motion["MotionAnimations.tsx"]
            Session["SessionProvider.tsx"]
        end

        subgraph Hooks["Custom Hooks"]
            H1["useCareerPrediction.ts"]
            H2["useRecommendations.ts"]
        end

        subgraph Lib["Lib / Utilities"]
            Auth["auth.ts"]
            DB["db.ts"]
            CareerAPI["api/career-api.ts"]
            RecsAPILib["api/recommendations-api.ts"]
            RoadmapAPI["api/roadmap-api.ts"]
        end
    end

    Landing --> Navbar
    Landing --> Footer
    Landing --> Motion
    Dashboard --> H1
    Dashboard --> H2
    H1 --> CareerAPI
    H2 --> RecsAPILib
    AuthRoutes --> AuthAPI
    Signup --> SignupAPI
    Dashboard --> RecsAPI
    AuthAPI --> Auth
    UsersAPI --> DB

    style NextApp fill:#000,stroke:#333,color:#fff
    style MainRoutes fill:#1E293B,stroke:#475569,color:#fff
    style AuthRoutes fill:#1E293B,stroke:#475569,color:#fff
    style DashRoutes fill:#1E293B,stroke:#475569,color:#fff
    style APIRoutes fill:#1E3A5F,stroke:#2563EB,color:#fff
```

---

## Figure 20: Backend Router Architecture

```mermaid
graph LR
    subgraph FastAPI["<b>FastAPI App (main.py)</b>"]
        App["FastAPI()"]
        CORS["CORS Middleware"]
        Lifespan["Lifespan Handler<br/>(Startup / Shutdown)"]
    end

    subgraph Routers["<b>API Routers (/api)</b>"]
        R1["career.py<br/>POST /api/predict"]
        R2["roadmap.py<br/>POST /api/roadmap"]
        R3["colleges.py<br/>POST /api/colleges"]
        R4["recommendations.py<br/>POST /api/recommendations/full"]
    end

    subgraph Services["<b>Services</b>"]
        S1["OllamaService<br/>(ollama_service.py)"]
        S2["CollegeService<br/>(college_service.py)"]
        S3["RecommendationService<br/>(recommendation_service.py)"]
        S4["RoadmapService<br/>(roadmap_service.py)"]
    end

    subgraph AI["<b>AI Models</b>"]
        M1["CareerPredictor<br/>(career_predictor.py)"]
        M2["Schemas<br/>(schemas.py)"]
    end

    subgraph Prompts["<b>Prompt Templates</b>"]
        P1["roadmap_prompts.py"]
        P2["college_prompts.py"]
        P3["summary_prompts.py"]
    end

    App --> CORS
    App --> Lifespan
    App --> Routers

    R1 --> M1
    R2 --> S4
    R3 --> S2
    R4 --> S3

    S3 --> M1
    S3 --> S1
    S3 --> S2
    S3 --> S4
    S4 --> S1
    S4 --> P1
    S2 --> S1
    S2 --> P2
    S3 --> P3

    style FastAPI fill:#009688,stroke:#00796B,color:#fff
    style Routers fill:#00796B,stroke:#004D40,color:#fff
    style Services fill:#E65100,stroke:#BF360C,color:#fff
    style AI fill:#4A148C,stroke:#311B92,color:#fff
```
