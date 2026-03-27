# 6CS007 Project and Professionalism
# Final Year Project
# Final Report

# Skill Lantern: AI-Powered Career Guidance System for Nepal

**Student Name:** Saurav Shrestha  
**Student ID:** 2408619  
**Supervisor:** Mrs. Prakriti Regmi  
**Reader:** Mr. Simon Giri  
**Submission Date:** March 6th, 2026

---

## Declaration

Declaration: I confirm that this report is my own work and that all sources of information have been cited appropriately. No part of this work has been submitted for any other academic award. The work presented herein represents the author's own effort except where due acknowledgement is made.

**Student Name:** Saurav Shrestha  
**Student ID:** 2408619  
**Signature:**  
**Date:** March 6th, 2026

---

## Abstract

Nepal's rapidly evolving job market, combined with limited access to professional career counselling services, leaves many students and early-career professionals uncertain about which career pathways align with their skills, interests, and academic backgrounds. This project presents Skill Lantern, an AI-powered career guidance system designed to provide personalised career recommendations, structured learning roadmaps, and college recommendations tailored specifically to the Nepalese context.

Skill Lantern accepts comprehensive user profile data — including academic background, technical and soft skills, areas of interest, certifications, CGPA, and career lifestyle preferences — through a multi-step registration form and returns a structured career assessment comprising career predictions with confidence scores, a three-stage learning roadmap (Beginner, Intermediate, Advanced), and college recommendations from a curated dataset of Nepalese educational institutions.

The system employs a hybrid AI architecture combining two complementary approaches: (1) an XGBoost (Extreme Gradient Boosting) machine learning classifier trained on survey-based career data from Nepalese graduates for career prediction, and (2) Meta's LLaMA 3 large language model served locally via Ollama for generating personalised roadmaps, college recommendations, and career summaries using natural language generation. When the XGBoost model is unavailable or when user profiles fall outside the training distribution, a rule-based fallback system using skill-to-career mapping provides baseline recommendations.

The technology stack comprises a FastAPI (Python) backend for AI processing and API services, a Next.js 16 frontend built with React 19, TypeScript, and Tailwind CSS 4 for the user interface, PostgreSQL via Prisma ORM for data persistence, and NextAuth.js v5 for secure authentication. The backend exposes RESTful API endpoints consumed by the frontend through a proxy middleware layer.

Model evaluation through 5-fold stratified cross-validation and an 80/20 train-test split demonstrates the XGBoost classifier's ability to predict career categories across 24 career domains. The system is positioned as a decision-support tool that augments — rather than replaces — human career counselling, providing data-driven initial guidance that students can use alongside professional advice.

---

## Table of Contents

1. Introduction
   - 1.1 Project Briefing
   - 1.2 AI Implementation
   - 1.3 Aims
   - 1.4 Objectives
   - 1.5 Artefact
   - 1.6 Academic Question
   - 1.7 Scope and Limitations of the Project
   - 1.8 Report Structure
2. Literature Review
   - 2.1 Research Papers Review
   - 2.2 Existing Systems Comparison
   - 2.3 AI Algorithm Discussion and Comparison
3. Project Methodology
4. Technology and Tools Used for the Project
5. Artefact Designs
   - 5.1 Deliverable 1: AI Model and Backend API
   - 5.2 Deliverable 2: Web Application and User Interface
   - 5.3 AI-Specific Artefact Documentation
6. Conclusion
7. Critical Evaluation of the Project
8. Evidence of Project Management
9. References and Bibliography
10. Appendices

---

## Table of Figures

*(To be updated with actual figure numbers when diagrams are inserted)*

- Figure 1: Functional Decomposition Diagram (FDD)
- Figure 2: System Architecture Diagram
- Figure 3: XGBoost Decision Tree Ensemble Visualisation
- Figure 4: Sequence Diagram — Career Prediction Flow
- Figure 5: Sequence Diagram — Full Recommendation Flow
- Figure 6: Activity Diagram — User Registration and Profile Creation
- Figure 7: Activity Diagram — Career Recommendation Generation
- Figure 8: Use Case Diagram
- Figure 9: Entity Relationship Diagram (ERD)
- Figure 10: Landing Page Wireframe
- Figure 11: Signup Form Wireframe
- Figure 12: Dashboard Wireframe
- Figure 13: Landing Page Webpage
- Figure 14: Signup Page Webpage
- Figure 15: Dashboard Page Webpage
- Figure 16: Career Distribution in Training Data
- Figure 17: Feature Importance Plot
- Figure 18: Confusion Matrix
- Figure 19: Cross-Validation Accuracy per Fold
- Figure 20: Gantt Chart

---

## 1. Introduction

### 1.1 Project Briefing

Career decision-making is one of the most consequential choices facing students and young professionals. In Nepal, this challenge is amplified by several structural factors: the absence of widely accessible, data-driven career counselling services; a rapidly diversifying job market driven by digital transformation; and socioeconomic constraints that make career missteps particularly costly. While students in developed economies may benefit from school counsellors, career services centres, and sophisticated online assessment platforms, Nepalese students frequently rely on informal advice from family, peers, or social media — sources that, while well-intentioned, lack the systematic analysis of an individual's skills, interests, and academic profile against market realities.

Skill Lantern addresses this gap by providing an AI-powered career guidance platform that analyses a user's comprehensive profile — including their gender, education level, undergraduate course, specialisation, CGPA, technical skills, soft skills, areas of interest, certifications, career lifestyle preferences, work environment preferences, location preferences, and learning style — and delivers structured career recommendations. The system does not merely suggest a single career; instead, it provides a ranked list of career predictions with associated confidence scores, a detailed three-stage learning roadmap (Beginner, Intermediate, and Advanced) with specific skills, resources, and milestones for each stage, and college recommendations drawn from a curated dataset of Nepalese educational institutions.

The platform is delivered as a full-stack web application. Users interact through a modern, responsive interface built with Next.js 16 and React 19, which guides them through a multi-step registration form to capture their profile data. Upon registration, their profile is transmitted to a FastAPI backend where the XGBoost machine learning model processes the data and returns career predictions. The user can then view a detailed dashboard presenting their top predicted careers, a personalised roadmap generated by a locally hosted LLaMA 3 large language model via Ollama, and recommendations for colleges in Nepal offering relevant programmes.

### 1.2 AI Implementation

#### AI Aspect Addressed

- **Machine Learning (Supervised Classification):** The core AI component is a multi-class classification model built using the XGBoost (Extreme Gradient Boosting) algorithm. The model is trained on labelled survey data from Nepalese graduates, where each record maps a set of input features (gender, course, CGPA, skills, interests, certifications) to a career category outcome. This constitutes a supervised learning task with a discrete categorical target variable.

- **Natural Language Processing / Generation (NLP/NLG):** The system integrates Meta's LLaMA 3 large language model, served locally via the Ollama inference server, to perform natural language generation tasks. The LLM generates personalised career roadmaps structured as three-stage learning paths, provides career summaries tailored to the user's specific profile, and produces contextualised college recommendations based on the predicted career and the user's location and budget preferences.

- **Rule-Based AI (Fallback System):** A deterministic rule-based career matching system serves as a fallback when the XGBoost model is unavailable or when the user's profile falls outside the training distribution. This system uses a manually curated mapping of 50+ skills and interests to career categories, providing baseline recommendations through weighted scoring.

#### Learning Paradigm and Justification

A supervised learning approach is employed because the career prediction task has a clearly defined target output — a discrete career category label — derived from actual career outcomes reported by graduates in the survey dataset. The availability of labelled data (survey responses mapped to career categories) makes supervised classification the natural and most appropriate paradigm. Unsupervised approaches (e.g., clustering) were considered but deemed less suitable because they would discover latent groupings in the data rather than mapping to known, actionable career categories. Reinforcement learning was not appropriate as there is no sequential decision-making process with delayed rewards involved.

The supervised classification framing also aligns naturally with standard evaluation metrics (accuracy, precision, recall, F1-score, top-k accuracy) that enable rigorous quantitative assessment of the model's predictive capability.

#### Mathematics Behind AI and Model Flow

The mathematical foundation of Skill Lantern's career prediction rests on the XGBoost algorithm, an implementation of gradient-boosted decision trees. The key mathematical concepts are:

**Gradient Boosting Framework:** XGBoost builds an additive model of the form:

$$\hat{y}_i = \sum_{k=1}^{K} f_k(x_i)$$

where each $f_k$ is a decision tree (weak learner), and $K$ is the total number of trees (set to 500 in this project). New trees are added sequentially, each one trained to correct the errors (residuals) of the previous ensemble.

**Objective Function:** The model minimises a regularised objective:

$$\mathcal{L} = \sum_{i=1}^{n} l(y_i, \hat{y}_i) + \sum_{k=1}^{K} \Omega(f_k)$$

where $l$ is the loss function and $\Omega$ is a regularisation term that penalises tree complexity. For multi-class classification, the loss function is the multi-class softmax (softprob):

$$P(y_i = c | x_i) = \frac{e^{z_c}}{\sum_{j=1}^{C} e^{z_j}}$$

where $z_c$ is the raw prediction (logit) for class $c$, and $C$ is the total number of career categories (24 in this project).

**Multi-class Log Loss:** The training loss for multi-class classification is:

$$L = -\sum_{i=1}^{n} \sum_{c=1}^{C} y_{ic} \log(p_{ic})$$

where $y_{ic}$ is 1 if sample $i$ belongs to class $c$ and 0 otherwise, and $p_{ic}$ is the predicted probability.

**Regularisation:** XGBoost employs L1 (reg_alpha = 0.1) and L2 (reg_lambda = 1.0) regularisation on leaf weights, along with tree structure constraints (max_depth = 8, min_child_weight = 3, gamma = 0.1) and stochastic sampling (subsample = 0.85, colsample_bytree = 0.85) to prevent overfitting.

**Feature Encoding Pipeline:** Before model training, raw categorical features undergo encoding transformations:

1. **Label Encoding:** Gender and undergraduate course are encoded using scikit-learn's LabelEncoder, mapping categorical strings to integer values.
2. **Multi-Label Binarisation:** Skills and interests (multi-select fields) are parsed from delimited strings and converted to binary feature vectors. The top 50 most frequent skills and top 30 most frequent interests in the dataset are retained as binary columns (1 = present, 0 = absent).
3. **Numerical Normalisation:** CGPA values are normalised by dividing by 100, scaling to the [0, 1] range.
4. **Binary Encoding:** Certification status and working status are encoded as binary (0/1) indicators.

**LLM Inference (LLaMA 3):** The LLaMA 3 model, a decoder-only transformer with self-attention mechanisms, generates text responses based on structured prompts. The self-attention mechanism computes:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

where $Q$, $K$, $V$ are query, key, and value projections of the input embeddings, and $d_k$ is the dimensionality of the key vectors. Temperature-controlled sampling (temperature = 0.5 for roadmaps) governs the creativity-determinism tradeoff in generated outputs.

#### Agent Description

Using the PEAS (Performance, Environment, Actuators, Sensors) model for intelligent agents, the Skill Lantern system can be characterised as a **Decision Support Agent** operating within the Career Guidance domain:

- **Performance (P):** Measured by the accuracy and relevance of career predictions (classification accuracy, top-k accuracy, confidence calibration), the quality and actionability of generated roadmaps, and user satisfaction with the overall guidance provided.

- **Environment (E):** The system operates within the domain of Nepalese higher education and early career transitions. The environment includes diverse student profiles with varying academic backgrounds (IT, Engineering, Business, Science, Commerce, Arts), skill levels, and career aspirations. The environment is partially observable (the system observes only the data provided by the user) and stochastic (career outcomes are influenced by factors beyond the observed profile).

- **Actuators (A):** The system produces structured JSON API responses containing: (1) ranked career predictions with confidence scores, (2) three-stage learning roadmaps with skills, resources, and milestones, (3) college recommendations with program details, location, and affiliation information, and (4) natural language career summaries.

- **Sensors (S):** The system receives input through the user profile submission (a structured form capturing 15+ attributes), supplemented by the college dataset (CSV with ~1,400 Nepalese institutions) and the career survey dataset used for model training.

The agent operates in a reactive mode: it processes each user profile independently, generates recommendations, and presents results. It does not maintain conversational state or adapt its model based on user feedback in real-time. However, the architecture supports future extension to incorporate feedback loops for model refinement.

### 1.3 Aims

The overarching aim of this project is to design, develop, and evaluate an AI-powered career guidance web application that provides Nepalese students and early-career professionals with personalised, data-driven career recommendations, actionable learning roadmaps, and relevant college suggestions — thereby bridging the gap between the availability of career counselling services and the needs of the target user population.

### 1.4 Objectives

1. To develop a machine learning classification model using XGBoost trained on survey data from Nepalese graduates, capable of predicting suitable career categories based on a user's academic background, skills, and interests.

2. To integrate a locally hosted large language model (LLaMA 3 via Ollama) for generating personalised career roadmaps, college recommendations, and career summaries through natural language generation.

3. To design and implement a full-stack web application with a responsive, multi-step user registration flow that captures comprehensive user profile data (education, skills, interests, certifications, preferences) for accurate career assessment.

4. To curate and integrate a dataset of Nepalese educational institutions, enabling the system to recommend colleges and programmes relevant to the user's predicted career path, location preference, and budget.

5. To implement a rule-based fallback prediction system that provides baseline career recommendations when the machine learning model is unavailable, ensuring system reliability.

6. To evaluate the machine learning model using established classification metrics (accuracy, precision, recall, F1-score, top-k accuracy, confusion matrices) through stratified cross-validation and held-out test set evaluation.

### 1.5 Artefact

The primary artefact is the Skill Lantern platform, a modular AI-powered career guidance system composed of interconnected subsystems. The platform is divided into two major deliverables:

**Artefact 1: AI Model and Backend API** — An XGBoost multi-class classification model trained on the career_recommender.csv survey dataset, deployed within a FastAPI backend. The backend exposes RESTful API endpoints for career prediction (`POST /api/predict`), roadmap generation (`POST /api/roadmap`), college recommendations (`POST /api/colleges`), and full recommendation orchestration (`POST /api/recommendations`). The LLaMA 3 integration via Ollama provides natural language generation capabilities. A rule-based fallback system ensures recommendations are always available.

**Artefact 2: Web Application and User Interface** — A Next.js 16 web application with React 19, TypeScript, and Tailwind CSS 4, featuring: a responsive landing page with animations (Framer Motion), a multi-step signup form (6 steps collecting personal info, education, skills, interests, certifications, and preferences), user authentication (NextAuth.js v5 with credential-based login and bcrypt password hashing), a career dashboard displaying predictions, roadmaps, and college recommendations, and PostgreSQL data persistence via Prisma ORM.

**Functional Decomposition Diagram (FDD):**

*(Insert Figure 1: FDD showing the decomposition of Skill Lantern into its subsystems)*

The system decomposes into the following primary subsystems:

1. **User Management Subsystem:** Registration, authentication, profile storage
2. **Career Prediction Subsystem:** XGBoost model inference, rule-based fallback, confidence scoring
3. **Roadmap Generation Subsystem:** LLaMA 3 prompt engineering, three-stage roadmap structuring
4. **College Recommendation Subsystem:** CSV data loading, location/budget filtering, LLM-enhanced explanations
5. **Recommendation Orchestration Subsystem:** Coordinates all services to produce unified career guidance

### 1.6 Academic Question

**Academic Question:** *How can a hybrid AI architecture combining gradient-boosted decision trees (XGBoost) for career classification with a large language model (LLaMA 3) for personalised content generation be effectively integrated into a web-based career guidance system to provide actionable, context-aware recommendations for Nepalese students?*

This question is addressed throughout the report by documenting: (1) the architectural decisions behind combining a structured ML classifier with a generative LLM and why this hybrid approach provides both quantitative predictions and rich, personalised guidance that neither component could deliver alone; (2) the choice of XGBoost over alternative classifiers and the justification based on performance, interpretability, and suitability for tabular survey data; (3) the integration of LLaMA 3 via Ollama for local inference and how prompt engineering is used to produce structured, actionable roadmaps; (4) the design of the rule-based fallback system and its role in ensuring system reliability; and (5) the evaluation evidence demonstrating the model's classification performance and the quality of generated recommendations.

A supervised learning approach is justified because the career prediction task has a well-defined target output — a discrete career category label — derived from actual employment outcomes reported in the survey dataset. The availability of labelled training data and the discrete nature of the prediction target make supervised multi-class classification the most appropriate AI paradigm for this component of the system.

### 1.7 Scope and Limitations of the Project

**Scope (Inclusions):**

- Career prediction based on user profile data (academic background, skills, interests, certifications, CGPA) using a trained XGBoost classification model.
- Natural language generation of personalised career roadmaps, college recommendations, and career summaries using LLaMA 3 via Ollama.
- A full-stack web application with user registration, authentication, profile management, and a career dashboard.
- College recommendations from a curated dataset of ~1,400 Nepalese educational institutions, filterable by location, budget, and degree level.
- Rule-based fallback predictions when the ML model is unavailable.
- Model evaluation using accuracy, precision, recall, F1-score, top-k accuracy, confusion matrices, and cross-validation.
- Documentation of the complete development lifecycle including feature engineering, model training, and system integration.

**Limitations and Exclusions:**

- The career prediction model is trained on a survey dataset that may not fully represent the diversity of career outcomes in Nepal. The dataset's size and sampling methodology limit the generalisability of predictions.
- Career categories are limited to 24 predefined categories. Users whose ideal careers fall outside these categories will receive the closest available match rather than a precise recommendation.
- The LLaMA 3 model runs locally via Ollama, requiring sufficient computational resources (RAM, potentially GPU) on the deployment machine. This limits scalability for concurrent users.
- The system does not incorporate real-time labour market data, salary information, or job posting analytics.
- The college dataset is static (loaded from CSV) and does not automatically update when new institutions or programmes become available.
- The system is designed for the Nepalese context; career categories, college data, and cultural assumptions may not be directly transferable to other countries.
- Large-scale production deployment with load balancing, horizontal scaling, or CDN distribution is not implemented — the system is delivered as a functional prototype.
- Advanced security features beyond basic credential-based authentication (e.g., two-factor authentication, OAuth social login providers) are not implemented.

### 1.8 Report Structure

The remainder of this report proceeds as follows. It begins with a **Literature Review** surveying research on career recommendation systems, machine learning approaches for career prediction, gradient boosting algorithms, large language models for education, and existing career guidance platforms. This is followed by a justification of the selected **Project Methodology** (Agile with Scrum principles) and a detailed presentation of the **Technology and Tools** used, including rationale for each component choice.

Subsequent chapters document the **Artefact Designs**, covering system architecture, data collection and preprocessing, model development (XGBoost training pipeline), testing evidence, and AI-specific evaluation metrics such as confusion matrices, cross-validation results, and feature importance analysis. The report then presents the **Conclusion**, explicitly linking findings back to the stated aims, objectives, and academic question. A **Critical Evaluation** and personal reflection are provided thereafter.

The final sections include **Evidence of Project Management** activities (log sheets, Gantt chart), the full **Reference and Bibliography** list, and **Appendices** containing supplementary material including mathematical derivations, user manual, and system configuration details.

---

## 2. Literature Review

This literature review surveys the current state of research in AI-powered career guidance systems, machine learning for career prediction, gradient boosting algorithms, and the application of large language models in educational contexts. The review draws from peer-reviewed journal articles, conference proceedings, and existing career guidance platforms to establish the theoretical and practical foundation upon which Skill Lantern is built.

### 2.1 Research Papers Review

#### Garg and Sharma (2021) — 'Career Recommendation System Using Machine Learning'

This study presents a career recommendation system that employs multiple machine learning classifiers — including Random Forest, Decision Trees, and Support Vector Machines — trained on student academic and skills data. The authors demonstrate that ensemble methods (particularly Random Forest) outperform single classifiers for career prediction tasks, achieving accuracy above 90% on their dataset. Their work validates the use of machine learning for career guidance and influenced Skill Lantern's decision to use XGBoost, an advanced ensemble method that builds upon the gradient boosting principles and typically outperforms Random Forest by reducing bias through sequential tree construction rather than parallel averaging.

#### Mohamed et al. (2022) — 'Student Career Prediction Using Machine Learning'

Mohamed et al. compare multiple classifiers including Naive Bayes, K-Nearest Neighbours, and Random Forest for predicting student career paths based on academic performance and skill assessments. The authors find that feature engineering — particularly the encoding of multi-select skill variables into binary features — significantly impacts prediction quality. This finding directly informed Skill Lantern's feature engineering pipeline, which uses multi-label binarisation for skills and interests, retaining the top 50 most frequent skills as binary indicator features.

#### Chen and Guestrin (2016) — 'XGBoost: A Scalable Tree Boosting System'

This foundational paper introduces XGBoost, the algorithm at the core of Skill Lantern's career prediction model. Chen and Guestrin demonstrate that XGBoost's regularised objective function, efficient handling of sparse data, and support for parallel computation make it particularly effective for structured/tabular data classification tasks. The paper's contributions include: a weighted quantile sketch for approximate tree learning, a sparsity-aware algorithm for handling missing values, and a cache-aware block structure for efficient computation. Skill Lantern leverages XGBoost's native support for multi-class classification (softprob objective), L1/L2 regularisation, and subsampling to prevent overfitting on the relatively small survey dataset.

#### Friedman (2001) — 'Greedy Function Approximation: A Gradient Boosting Machine'

Friedman's seminal paper establishes the theoretical foundation of gradient boosting, upon which XGBoost is built. The paper formalises the idea of boosting as iterative gradient descent in function space, where each successive weak learner (decision tree) is trained to approximate the negative gradient of the loss function. This mathematical framework — particularly the concept of fitting trees to pseudo-residuals — underpins the training procedure used in Skill Lantern's XGBoost model and provides the theoretical justification for the model's ability to learn complex, non-linear relationships between user profile features and career outcomes.

#### Touvron et al. (2023) — 'LLaMA: Open and Efficient Foundation Language Models'

This paper from Meta AI introduces the LLaMA family of large language models, which form the basis for the natural language generation component of Skill Lantern. The authors demonstrate that LLaMA models, despite being significantly smaller than models like GPT-3, achieve competitive performance on a wide range of NLP benchmarks when properly trained on high-quality, diverse text data. The open-source availability of LLaMA (and its successor LLaMA 3) makes it suitable for local deployment via inference servers like Ollama, avoiding the cost and privacy concerns associated with cloud-based API services — a key consideration for a student project targeting users in Nepal.

#### Vaswani et al. (2017) — 'Attention Is All You Need'

This foundational paper introduces the Transformer architecture, which underpins the LLaMA 3 model used in Skill Lantern. The key innovation — the self-attention mechanism that enables the model to capture dependencies between all positions in a sequence simultaneously — is the mathematical backbone of modern language models. The self-attention formula $\text{Attention}(Q,K,V) = \text{softmax}(QK^T / \sqrt{d_k})V$ enables LLaMA 3 to generate contextually coherent roadmaps and career summaries by attending to all relevant parts of the input prompt simultaneously.

#### Nie et al. (2022) — 'Recommendation Systems in Education: A Survey'

This survey explores the application of recommendation systems in educational contexts, covering collaborative filtering, content-based, and hybrid approaches. The authors argue that educational recommendation systems must account for domain-specific factors such as prerequisite knowledge, learning progression, and institutional constraints. Skill Lantern's design reflects several of these principles: the three-stage roadmap (Beginner, Intermediate, Advanced) represents learning progression, college recommendations incorporate location and budget constraints, and the system accounts for the user's current education level when generating recommendations.

#### Sharma and Kumar (2020) — 'Career Counselling Expert System Using Machine Learning'

Sharma and Kumar present an expert system for career counselling that combines rule-based reasoning with machine learning predictions. Their hybrid approach — using ML for initial classification and rules for domain-specific adjustments — is conceptually similar to Skill Lantern's architecture, which combines XGBoost prediction with a rule-based fallback system. The authors demonstrate that hybrid systems provide more robust recommendations than either approach alone, particularly when handling edge cases where ML models may lack confidence.

#### Prokhorenkova et al. (2018) — 'CatBoost: Unbiased Boosting with Categorical Features'

While Skill Lantern uses XGBoost rather than CatBoost, this paper provides valuable comparative context for gradient boosting algorithms. The authors identify target leakage as a significant risk when encoding categorical features in boosting models — a concern directly addressed in Skill Lantern's feature engineering by using label encoding for low-cardinality features (gender, course) and binary encoding for multi-select features (skills, interests) rather than target-based encoding methods.

#### Bhalke and Doifode (2023) — 'AI-Based Career Guidance System'

This paper presents a career guidance system for Indian students using machine learning, demonstrating the viability of survey-based career prediction in a South Asian context. The authors' dataset structure (similar features including academic background, skills, and interests) validates Skill Lantern's data collection approach. However, Bhalke and Doifode's system uses a simpler classification model without the benefit of natural language generation for roadmaps, highlighting the novelty of Skill Lantern's hybrid ML+LLM architecture.

### 2.2 Existing Systems Comparison

- **LinkedIn Career Explorer:** Provides career path exploration based on job market data and professional network analysis. LinkedIn leverages massive proprietary datasets of professional profiles and job transitions. Skill Lantern differs by targeting specifically Nepalese students who may not yet have professional network data, using academic and skills data collected at the point of career entry rather than professional trajectory data.

- **Sokanu (now CareerExplorer):** An online career assessment platform that uses psychometric testing and interest inventories to suggest career matches. While Sokanu provides detailed personality-career alignment, it does not incorporate machine learning trained on actual career outcome data. Skill Lantern's supervised learning approach, trained on graduates' actual career outcomes, provides empirically grounded predictions rather than purely psychometric ones.

- **MyNextMove (US Department of Labor):** Provides career information and interest-based exploration using the O*NET database. While comprehensive for the US context, it has no relevance to the Nepalese educational system or job market. Skill Lantern fills this gap with Nepal-specific college and career data.

- **Roadmap.sh:** Provides structured learning roadmaps for technology roles. While the roadmaps are high-quality, they are manually curated, static, and not personalised to individual user profiles. Skill Lantern generates dynamic, personalised roadmaps using LLaMA 3, adapting content based on the user's current skills, education level, and target career.

- **Shiksha.com (India):** A college and career guidance platform popular in South Asia. While Shiksha provides extensive college information for India, it has limited coverage of Nepalese institutions. Skill Lantern's curated dataset of ~1,400 Nepalese colleges addresses this regional gap.

### 2.3 AI Algorithm Discussion and Comparison

The literature reveals several algorithmic approaches for career prediction, each with distinct strengths and limitations:

**Traditional ML Classifiers (Naive Bayes, SVM, Logistic Regression):** These methods typically achieve 75–88% accuracy on career prediction benchmarks. They are computationally lightweight and interpretable but struggle with complex, non-linear feature interactions that are common in career-profile data (e.g., the interaction between specific skill combinations and career suitability).

**Tree-Based Methods (Random Forest, Decision Trees):** Random Forest achieves 85–92% accuracy on similar tasks, benefiting from ensemble averaging that reduces variance. However, Random Forest treats each tree independently (bagging), missing the opportunity to correct errors sequentially.

**Gradient Boosting (XGBoost, LightGBM, CatBoost):** These methods represent the state-of-the-art for tabular data classification, typically achieving 88–95% accuracy on structured datasets. XGBoost's sequential error correction, regularisation capabilities, and native support for multi-class classification make it particularly suitable for career prediction on survey data. Skill Lantern uses XGBoost with `multi:softprob` objective, which outputs calibrated probability distributions across all 24 career categories.

**Deep Learning (Neural Networks):** While powerful for unstructured data (images, text), deep learning methods offer limited advantages over gradient boosting for tabular data with moderate dataset sizes. Grinsztajn et al. (2022) demonstrate that tree-based models consistently outperform deep learning on tabular benchmarks, supporting Skill Lantern's choice of XGBoost.

**Large Language Models (GPT, LLaMA):** LLMs excel at natural language generation but are not inherently designed for structured classification tasks. Skill Lantern's hybrid architecture leverages both paradigms: XGBoost for quantitative career prediction and LLaMA 3 for qualitative content generation (roadmaps, summaries).

The mathematical advantage of XGBoost for this task lies in its boosting objective:

$$\hat{y}_i^{(t)} = \hat{y}_i^{(t-1)} + f_t(x_i)$$

where each new tree $f_t$ is trained to minimise the second-order Taylor approximation of the loss function, enabling efficient, theoretically grounded optimisation. Combined with regularisation terms $\Omega(f) = \gamma T + \frac{1}{2}\lambda \|w\|^2$ (where $T$ is the number of leaves and $w$ are leaf weights), XGBoost achieves the balance of expressiveness and generalisation that is critical for career prediction on relatively small survey datasets.

---

## 3. Project Methodology

This project adopts an Agile-inspired iterative development methodology, structured around Scrum principles of time-boxed iterations, incremental delivery, and regular retrospection, adapted for a solo developer context. The choice of Agile over traditional Waterfall or V-Model approaches is justified by several factors specific to this project's nature:

**Uncertainty in AI Model Performance:** The career prediction component involves machine learning experimentation where model performance cannot be fully predicted upfront. The feature engineering pipeline, hyperparameter tuning, and evaluation process require iterative refinement. An Agile approach allowed rapid experimentation with different feature encoding strategies (e.g., testing various numbers of top skills to retain, experimenting with different hyperparameter configurations) without requiring a completed design specification before implementation could begin.

**Integration Complexity:** The system involves multiple interconnected components — an XGBoost model, an LLM inference server (Ollama), a FastAPI backend, a Next.js frontend, a PostgreSQL database, and third-party libraries for authentication. Incremental integration — delivering a working end-to-end slice early (e.g., getting the basic prediction API working before building the full frontend) and progressively enhancing it — reduced the risk of late-stage integration failures.

**Feedback-Driven Refinement:** Regular supervisor meetings (documented in logsheets) provided continuous feedback that guided development priorities. For example, feedback on the initial dashboard design led to iterative improvements in how career predictions and roadmaps are presented to users.

**Risk-Driven Prioritisation:** High-risk items such as XGBoost model accuracy, Ollama integration reliability, and the multi-step registration form's usability were identified early and addressed in dedicated iterations, preventing them from becoming critical blockers late in the project.

The project was structured across the academic timeline with the following major phases:

1. **Project Initiation and Proposal** — Requirements gathering, initial research, proposal submission
2. **Research and Literature Review** — Survey of career recommendation systems, ML algorithms, and LLM applications
3. **Dataset Exploration and Feature Engineering** — Analysis of career_recommender.csv, feature encoding experiments
4. **Model Development and Training** — XGBoost training pipeline implementation, hyperparameter tuning, evaluation
5. **Backend API Development** — FastAPI application, Ollama integration, API endpoint design
6. **Frontend Development** — Next.js application, registration flow, dashboard, authentication
7. **Integration Testing and Refinement** — End-to-end testing, bug fixing, UX improvements
8. **Report Writing and Final Submission** — Documentation, evaluation, report preparation

Each phase involved iterative sub-cycles of implementation, testing, and refinement. A mid-project Gantt chart (see Section 8: Evidence of Project Management) tracked progress against planned milestones.

*(Insert Figure 2: Mid-Project Gantt Chart)*

---

## 4. Technology and Tools Used for the Project

This section presents and justifies the technology choices for the Skill Lantern system. Each tool or framework was selected based on its suitability for the specific requirements of the project.

### 4.1 Programming Languages

**Python (Backend / AI):** Python was chosen for the backend and machine learning components due to its dominant position in the AI/ML ecosystem. Libraries such as scikit-learn, XGBoost, pandas, and NumPy provide mature, well-documented implementations of the algorithms and data processing pipelines required. FastAPI, the web framework, is Python-native and provides automatic request validation via Pydantic schemas, which aligns with the structured nature of user profile data.

**TypeScript (Frontend):** TypeScript was chosen over plain JavaScript for the Next.js frontend to leverage static type checking, which catches type-related errors at compile time rather than runtime. This is particularly valuable for a project involving complex data structures (user profiles with 15+ fields, career prediction responses with nested objects) and API communication between frontend and backend.

### 4.2 Backend Framework

**FastAPI:** FastAPI was selected as the Python web framework for several reasons:
- **Automatic API documentation:** Generates interactive Swagger UI (`/docs`) and ReDoc (`/redoc`) documentation, facilitating API testing and development.
- **Pydantic schema validation:** Request and response models are defined as Pydantic classes (e.g., `UserProfile`, `CareerPredictionResponse`), providing automatic type validation, serialisation, and documentation.
- **Asynchronous support:** Native `async/await` support with ASGI (Uvicorn server) enables non-blocking I/O operations — critical for the Ollama LLM inference calls, which involve network requests with potentially multi-second response times.
- **Modular router architecture:** API endpoints are organised into separate routers (`career.py`, `roadmap.py`, `colleges.py`, `recommendations.py`), promoting separation of concerns.

### 4.3 Frontend Framework

**Next.js 16 + React 19:** Next.js was selected for its server-side rendering capabilities, file-system-based routing (using the App Router), and built-in API route support. The API route proxying (`/api/auth/[...nextauth]`, `/api/users/profile`, `/api/users/recommendations`) allows the frontend to communicate with the FastAPI backend without exposing backend endpoints directly to the client. React 19 provides the component-based architecture for building the complex, multi-step signup form (1,240 lines) and the interactive dashboard (742 lines).

### 4.4 Styling and UI Components

**Tailwind CSS 4:** A utility-first CSS framework chosen for rapid, responsive UI development without the overhead of custom CSS files. Tailwind's just-in-time compiler ensures only used styles are included in the production build.

**shadcn/ui:** A component library providing pre-built, customisable UI components (accordion, buttons, forms) that follow accessibility best practices. Used for consistent styling across the application.

**Framer Motion:** An animation library for React used to add smooth transitions and scroll-based animations to the landing page, enhancing user experience without requiring manual CSS animation management.

### 4.5 Database

**PostgreSQL + Prisma ORM:** PostgreSQL was selected for its reliability, ACID compliance, and support for complex data types (JSON fields for storing prediction and roadmap data). Prisma ORM provides type-safe database queries generated from the schema definition (`schema.prisma`), automatic migration management, and integration with TypeScript types. The schema defines models for `User`, `UserProfile` (personal info, education, skills, interests, certifications, preferences), and `CareerRecommendation` (predictions JSON, roadmap JSON, colleges JSON, summary).

### 4.6 Authentication

**NextAuth.js v5:** Selected for its seamless integration with Next.js and support for credential-based authentication. Passwords are hashed using bcryptjs before storage. Session management uses encrypted JWT tokens. The library provides built-in middleware for route protection and session access in both server and client components.

### 4.7 AI/ML Tools

**XGBoost:** The gradient boosting library used for career classification. Key configuration: `XGBClassifier` with `multi:softprob` objective, 500 estimators, max_depth=8, learning_rate=0.05, subsample=0.85, colsample_bytree=0.85, min_child_weight=3, gamma=0.1, reg_alpha=0.1, reg_lambda=1.0.

**scikit-learn:** Used for data preprocessing (LabelEncoder, MultiLabelBinarizer), model evaluation (accuracy_score, classification_report, confusion_matrix, top_k_accuracy_score, cross_val_score), and train-test splitting (train_test_split with stratified sampling).

**Ollama:** A local LLM inference server that hosts Meta's LLaMA 3 model. Ollama provides a REST API (`/api/generate`, `/api/chat`) for text generation, eliminating the need for cloud-based API keys or GPU infrastructure management.

**joblib:** Used for serialising trained model artefacts (XGBoost model, label encoders, feature column lists) to `.pkl` files for deployment.

**pandas / NumPy:** Used for data loading, manipulation, and numerical operations during feature engineering and model training.

### 4.8 HTTP Client

**httpx:** An async-capable HTTP client library used for communication between the FastAPI backend and the Ollama inference server. Its async support aligns with FastAPI's asynchronous architecture.

### 4.9 Development Tools

**IDE:** Visual Studio Code with Python and TypeScript extensions.  
**Version Control:** Git for source code management.  
**Package Managers:** pip (Python, with virtualenv) and npm (Node.js, for Next.js frontend).

---

## 5. Artefact Designs

### 5.1 Deliverable 1: AI Model and Backend API

#### Software Requirements Specification (SRS)

**Functional Requirements:**

- **FR1:** The system shall accept user profile data via a POST API endpoint and return career predictions with confidence scores.
- **FR2:** The XGBoost model shall classify users into one of 24 predefined career categories and return the top-k predictions ranked by confidence.
- **FR3:** The system shall provide a rule-based fallback prediction when the XGBoost model is unavailable, using a skill-to-career mapping dictionary covering 50+ skills.
- **FR4:** The system shall generate a three-stage career roadmap (Beginner, Intermediate, Advanced) for the top predicted career using LLaMA 3 via Ollama.
- **FR5:** Each roadmap stage shall include: duration estimate, skills to learn, learning resources, and milestones.
- **FR6:** The system shall recommend Nepalese colleges relevant to the predicted career, filtered by the user's location preference, budget range, and degree level.
- **FR7:** The system shall provide a comprehensive recommendation endpoint that orchestrates career prediction, roadmap generation, college recommendations, and summary generation in a single request.
- **FR8:** The system shall expose a health check endpoint reporting the status of the API server, Ollama connection, and XGBoost model availability.

**Non-Functional Requirements:**

- **NFR1:** The career prediction API shall respond within 2 seconds for individual prediction requests.
- **NFR2:** The full recommendation endpoint (including LLM generation) shall respond within 60 seconds.
- **NFR3:** The backend shall handle CORS configuration for frontend communication.
- **NFR4:** All API responses shall conform to defined Pydantic schema models for type safety.

#### System Architecture Diagram

*(Insert Figure 2: System Architecture Diagram)*

The system follows a three-tier architecture:

1. **Presentation Layer (Frontend):** Next.js 16 application with React 19 components, communicating with the backend via API route proxies.
2. **Application Layer (Backend):** FastAPI application with four routers (career, roadmap, colleges, recommendations), three services (OllamaService, CollegeService, RecommendationService), and one ML model module (CareerPredictor).
3. **Data Layer:** PostgreSQL database (via Prisma ORM) for user and recommendation storage; CSV files for college data and career training data; .pkl files for serialised ML model artefacts.

The communication flow is:
```
Browser → Next.js Frontend → API Route Proxy → FastAPI Backend → {XGBoost Model, Ollama/LLaMA 3, College CSV}
                                                    ↕
                                              PostgreSQL (via Prisma)
```

#### Design and Modelling Diagrams

**Sequence Diagram 1: Career Prediction Flow**

*(Insert Figure 4: Sequence Diagram — Career Prediction Flow)*

1. User submits profile via frontend form.
2. Frontend sends POST request to Next.js API route (`/api/users/recommendations`).
3. API route forwards the user profile to FastAPI backend (`POST /api/predict`).
4. Backend's CareerPredictor loads the XGBoost model, encodes the user's features (gender, course, CGPA, skills, interests), and runs prediction.
5. If model is unavailable, the rule-based fallback system scores careers based on skill-to-career mapping.
6. Backend returns top-k career predictions with confidence scores.
7. Frontend displays results on the dashboard.

**Sequence Diagram 2: Full Recommendation Flow**

*(Insert Figure 5: Sequence Diagram — Full Recommendation Flow)*

1. Frontend sends POST to `/api/recommendations/full` with user profile + preferences.
2. Backend orchestrates: (a) Career prediction via XGBoost, (b) Roadmap generation via Ollama/LLaMA 3, (c) College recommendations via CollegeService + Ollama, (d) Summary generation via Ollama.
3. Each stage runs sequentially; results from career prediction inform roadmap and college queries.
4. Aggregated response returned to frontend.

**Activity Diagram 1: User Registration and Profile Creation**

*(Insert Figure 6: Activity Diagram)*

Start → Enter personal info (name, gender, DOB, city) → Enter education (course, specialisation, college, CGPA) → Select technical skills (multi-select) → Select interests (multi-select) → Enter certifications → Set preferences (career lifestyle, work environment, location, learning style) → Submit → Create account → Store profile → Generate recommendations → Display dashboard → End

**Activity Diagram 2: Career Recommendation Generation**

*(Insert Figure 7: Activity Diagram)*

Start → Receive user profile → Check if XGBoost model loaded → [Yes] Encode features → Run XGBoost prediction → Get top-k careers with confidence → [No] Run rule-based fallback → Score careers by skill matching → Get top careers → Select top career → Generate roadmap via LLaMA 3 → Parse roadmap JSON → Query college dataset → Filter by location/budget/programme → Generate college explanations via LLaMA 3 → Generate career summary → Assemble full recommendation response → Return to frontend → End

**Use Case Diagram**

*(Insert Figure 8: Use Case Diagram)*

Actors: Student (primary), Admin (future)

Use Cases:
- Register and create profile
- Login / Logout
- View career predictions
- View career roadmap
- View college recommendations
- View career summary
- Update profile

**Entity Relationship Diagram (ERD)**

*(Insert Figure 9: ERD)*

- **User** (id, name, email, password, createdAt, updatedAt) — 1:1 → **UserProfile** (fullName, gender, dateOfBirth, cityRegion, courseCategory, course, specialisation, schoolCollegeName, cgpa, interests[], technicalSkills[], softSkills[], hasCertification, certifications, careerLifestyle, workEnvironment, locationPreference, learningStyle)
- **User** — 1:N → **CareerRecommendation** (predictions JSON, topCareer, roadmap JSON, colleges JSON, summary, immediateActions[], hasFullDetails)
- **User** — 1:N → **Account** (provider, providerAccountId, access_token, ...)
- **User** — 1:N → **Session** (sessionToken, expires)

#### Testing

**Functional Testing Evidence:**

| Test Case | Description | Expected Result | Status |
|-----------|-------------|-----------------|--------|
| TC1 | Submit valid user profile to `/api/predict` | Returns career predictions with confidence scores | Pass |
| TC2 | Submit profile with missing optional fields | Returns predictions using available data | Pass |
| TC3 | Request prediction when XGBoost model not loaded | Falls back to rule-based prediction | Pass |
| TC4 | Request full recommendation with all services active | Returns predictions + roadmap + colleges + summary | Pass |
| TC5 | Request roadmap for a specific career | Returns 3-stage roadmap with skills, resources, milestones | Pass |
| TC6 | Request college recommendations with location filter | Returns colleges in specified location | Pass |
| TC7 | Submit profile with invalid CGPA (> 100) | Returns validation error | Pass |
| TC8 | Health check endpoint | Reports status of API, Ollama, and model | Pass |
| TC9 | Request colleges with budget filter | Returns colleges within budget range | Pass |
| TC10 | Submit profile with skills not in training data | Rule-based fallback provides recommendations | Pass |

### 5.2 Deliverable 2: Web Application and User Interface

#### Software Requirements Specification (SRS)

**Functional Requirements:**

- **FR9:** The web application shall provide a multi-step registration form collecting personal information, education details, skills, interests, certifications, and career preferences.
- **FR10:** The web application shall authenticate users via email and password with bcrypt hashing.
- **FR11:** The dashboard shall display the user's top predicted careers with confidence percentages, career descriptions, and visual indicators.
- **FR12:** The dashboard shall display a career roadmap with three stages (Beginner, Intermediate, Advanced), each showing duration, skills, resources, and milestones.
- **FR13:** The dashboard shall display recommended colleges with name, location, university affiliation, programmes offered, and contact information.
- **FR14:** The landing page shall provide information about the system's features, how it works, and contact details.
- **FR15:** The application shall be responsive and function correctly on desktop and mobile screen sizes.

**Non-Functional Requirements:**

- **NFR5:** Pages shall load within 3 seconds on a standard internet connection.
- **NFR6:** The registration form shall validate inputs client-side before submission.
- **NFR7:** Passwords shall be hashed using bcrypt before database storage.

#### Design and Modelling Diagrams

**Wireframes:**

*(Insert Figure 10: Landing Page Wireframe)*  
*(Insert Figure 11: Signup Form Wireframe)*  
*(Insert Figure 12: Dashboard Wireframe)*

**Implemented Webpages:**

*(Insert Figure 13: Landing Page Webpage — Screenshot)*  
*(Insert Figure 14: Signup Page Webpage — Screenshot)*  
*(Insert Figure 15: Dashboard Page Webpage — Screenshot)*

The landing page features a hero section with animated text (using Framer Motion), sections explaining the system's features and how it works, and navigation to the registration form. The signup page implements a 6-step form with progress indicators, form validation, and multi-select dropdowns for skills and interests. The dashboard displays career predictions as ranked cards with confidence bars, a tabbed roadmap view, and a college recommendations section with detailed cards.

#### Testing

| Test Case | Description | Expected Result | Status |
|-----------|-------------|-----------------|--------|
| TC11 | Register new user with valid data | Account created, redirected to login | Pass |
| TC12 | Register with existing email | Error message displayed | Pass |
| TC13 | Login with valid credentials | Redirected to dashboard | Pass |
| TC14 | Login with incorrect password | Error message displayed | Pass |
| TC15 | Access dashboard without authentication | Redirected to login page | Pass |
| TC16 | Submit signup form with empty required fields | Validation errors displayed | Pass |
| TC17 | Multi-step form navigation (next/back) | Form state preserved across steps | Pass |
| TC18 | Responsive layout on mobile viewport | Elements stack vertically, no overflow | Pass |
| TC19 | Dashboard displays predictions from API | Career cards rendered with correct data | Pass |
| TC20 | Dashboard roadmap tab switching | Stage content updates correctly | Pass |

### 5.3 AI-Specific Artefact Documentation

#### Data Collection

The career prediction model is trained on the `career_recommender.csv` dataset, a survey-based dataset collecting responses from graduates primarily in Nepal and South Asia. The dataset contains the following key columns:

- **Demographics:** Gender
- **Education:** Undergraduate course, CGPA/Percentage
- **Skills:** Multi-select skills field (e.g., "Python, Machine Learning, SQL")
- **Interests:** Multi-select interests field
- **Certifications:** Whether additional certifications were completed
- **Working Status:** Whether the respondent is currently employed
- **Job Title:** The respondent's current/first job title (used as the target variable)

**Data Preprocessing Pipeline:** The `train_model.py` script (521 lines) implements the complete preprocessing pipeline:

1. **Target Variable Extraction:** Job titles are extracted from the survey and mapped to 24 standardised career categories using a keyword-matching function (`categorize_career()`). Records with no clear career (students, unemployed, NA responses) are filtered out.

2. **Rare Category Removal:** Career categories with fewer than 3 samples are removed to ensure minimum representation for training.

3. **Feature Engineering:**
   - Gender: Label-encoded (categorical → integer)
   - Undergraduate Course: Label-encoded
   - CGPA: Normalised by dividing by 100 → [0, 1]
   - Certifications: Binary (1 = yes, 0 = no)
   - Working Status: Binary (1 = yes, 0 = no)
   - Skills: Top 50 most frequent skills extracted and encoded as binary columns (1 = present, 0 = absent)
   - Interests: Top 30 most frequent interests encoded as binary columns

4. **Data Split:** 80% training, 20% testing with stratified sampling to preserve class distribution.

The college dataset (`colleges.csv`) contains ~1,400 records of Nepalese educational institutions with fields including: college name, location, affiliated university, programmes offered, ownership type (government/private), phone, and email.

*(Insert Figure 16: Career Category Distribution in Training Data)*

#### Model Development

**XGBoost Classifier Configuration:**

The career prediction model uses scikit-learn-compatible XGBoost with the following hyperparameters:

| Parameter | Value | Justification |
|-----------|-------|---------------|
| n_estimators | 500 | Sufficient ensemble size for convergence |
| max_depth | 8 | Allows moderately deep trees to capture feature interactions |
| learning_rate | 0.05 | Low rate for gradual, stable learning |
| subsample | 0.85 | Stochastic sampling to reduce overfitting |
| colsample_bytree | 0.85 | Feature sampling per tree for diversity |
| min_child_weight | 3 | Minimum samples in leaf to prevent overly specific splits |
| gamma | 0.1 | Minimum loss reduction for further partitioning |
| reg_alpha | 0.1 | L1 regularisation on leaf weights |
| reg_lambda | 1.0 | L2 regularisation on leaf weights |
| objective | multi:softprob | Multi-class softmax probability output |
| eval_metric | mlogloss | Multi-class log loss for evaluation |

**Training Pipeline:**

```
Data Loading → Preprocessing → Feature Engineering → Stratified Split (80/20)
    → 5-Fold Cross-Validation → Full Model Training → Evaluation → Model Saving
```

The pipeline saves four artefacts:
1. `xgboost_model.pkl` — Trained XGBoost classifier
2. `label_encoder.pkl` — Career category label encoder
3. `feature_columns.pkl` — List of feature column names (for inference alignment)
4. `encoders.pkl` — Gender encoder, course encoder, top skills list, top interests list

**Rule-Based Fallback System:**

The `CareerPredictor` class (528 lines) implements a rule-based fallback that activates when the XGBoost model is not loaded. This system uses a manually curated dictionary mapping 50+ skills and interests to career categories. For each user profile, it:
1. Iterates through the user's skills and interests
2. Retrieves matching careers from the mapping dictionary
3. Scores careers by frequency of matches (more matching skills/interests = higher score)
4. Returns the top-k highest-scoring careers with normalised confidence scores

#### Optimisation and Evaluation

**Overfitting Prevention:** Multiple regularisation strategies are employed:
- L1 / L2 regularisation (reg_alpha=0.1, reg_lambda=1.0)
- Tree complexity constraints (max_depth=8, min_child_weight=3, gamma=0.1)
- Stochastic sampling (subsample=0.85, colsample_bytree=0.85)
- The relatively low learning rate (0.05) with 500 estimators allows gradual learning

**Cross-Validation:** 5-fold stratified cross-validation provides a robust estimate of model generalisation, accounting for the relatively small dataset size. The cross-validation uses a simplified model configuration (100 estimators, max_depth=6) to reduce computation time while providing a representative accuracy estimate.

**Evaluation Metrics:**

The model is evaluated using:
- **Overall Accuracy:** Percentage of correctly classified test samples
- **Top-3 Accuracy:** Whether the correct career appears in the top 3 predictions
- **Top-5 Accuracy:** Whether the correct career appears in the top 5 predictions
- **Per-Class Precision, Recall, F1-Score:** Via scikit-learn's classification_report
- **Confusion Matrix:** Distribution of predictions across all career categories
- **Feature Importance:** XGBoost's built-in feature importance scores indicating which features most influence predictions

*(Insert Figure 17: Feature Importance Plot — Top 15 Features)*

*(Insert Figure 18: Confusion Matrix)*

*(Insert Figure 19: Cross-Validation Accuracy per Fold)*

#### AI Integration into the Application

The AI models are integrated into the application through a RESTful API architecture. The FastAPI backend exposes four primary endpoints:

1. **POST /api/predict** — Accepts a `UserProfile` JSON payload, runs XGBoost prediction (or rule-based fallback), and returns a `CareerPredictionResponse` containing an array of `PredictedCareer` objects (career name, confidence score, description).

2. **POST /api/roadmap** — Accepts a career name and user profile, constructs a structured prompt for LLaMA 3, sends it to Ollama's `/api/generate` endpoint, parses the JSON response, and returns a `RoadmapResponse` with overview, stages (Beginner/Intermediate/Advanced), tools, job roles, and growth paths.

3. **POST /api/colleges** — Accepts a career name, location preference, budget range, and degree level. The `CollegeService` loads the CSV dataset, filters by relevant criteria, and returns matching `CollegeInfo` objects. If Ollama is available, LLaMA 3 generates contextual explanations for why each college is recommended.

4. **POST /api/recommendations/full** — The orchestration endpoint that calls all three services in sequence: prediction → roadmap → colleges → summary, returning a unified `FullRecommendationResponse`.

**Backend Startup Lifecycle:**

On application startup (via the FastAPI `lifespan` handler), the system:
1. Loads the college CSV dataset into memory via `CollegeService`
2. Loads the career survey dataset via `CareerPredictor`
3. Attempts to load the XGBoost model from `.pkl` files; falls back to rule-based if unavailable
4. Checks Ollama health by querying `/api/tags`; logs available models
5. Configures CORS middleware for frontend communication

**LLaMA 3 Integration Architecture:**

The `OllamaService` class (239 lines) manages all communication with the Ollama inference server. It provides:
- `generate()` — Single-response generation with configurable temperature and max tokens
- `generate_stream()` — Streaming generation for real-time output
- `chat()` — Chat-completion API for multi-turn conversations
- `parse_json_response()` — Robust JSON extraction from LLM responses, handling markdown code blocks and embedded JSON

Prompt engineering uses structured system prompts that instruct LLaMA 3 to produce JSON-formatted responses. For example, the roadmap prompt specifies the exact JSON schema expected (stages with level, duration, skills, resources, milestones), ensuring parseable outputs for frontend rendering.

**Sample API Request (Career Prediction):**
```json
{
  "user_profile": {
    "name": "Ram Sharma",
    "gender": "Male",
    "education_level": "bachelors",
    "ug_course": "Computer Science",
    "specialization": "Software Engineering",
    "skills": ["python", "javascript", "react", "sql"],
    "interests": ["web development", "machine learning"],
    "cgpa": 78.5,
    "certifications": ["AWS Cloud Practitioner"],
    "location": "Nepal"
  }
}
```

**Sample API Response (Career Prediction):**
```json
{
  "predictions": [
    {"career": "Software Engineer", "confidence": 0.42, "description": "..."},
    {"career": "Web Developer", "confidence": 0.28, "description": "..."},
    {"career": "Data Scientist", "confidence": 0.15, "description": "..."}
  ],
  "user_profile_summary": {"skills_count": 4, "interests_count": 2},
  "message": "Prediction successful"
}
```

#### Comparing Algorithm Performance

**XGBoost vs Rule-Based Fallback:**

| Metric | XGBoost Model | Rule-Based Fallback |
|--------|---------------|---------------------|
| Approach | Trained classifier with learned feature interactions | Deterministic skill-career mapping |
| Training Required | Yes (offline training on survey data) | No (manually curated mappings) |
| Confidence Calibration | Probability-based (softmax over classes) | Frequency-based (normalised match counts) |
| Handles Feature Interactions | Yes (tree splits capture combinations) | No (independent skill matching) |
| Handles Unknown Skills | Limited (only trained features) | Flexible (all mapped skills) |
| Primary Strength | Empirically grounded predictions | Always-available baseline |
| Primary Weakness | Requires sufficient training data per class | Cannot capture skill interactions |

The XGBoost model provides empirically grounded predictions based on patterns learned from actual career outcomes, while the rule-based system provides interpretable, deterministic recommendations based on domain knowledge. The hybrid approach ensures that the system always produces recommendations, even in degraded states.

#### AI Testing — Accuracy Visualisations

*(Insert Figure 17: Feature Importance Plot)*

Feature importance analysis reveals which input features most strongly influence the XGBoost model's career predictions. Typically, skill-related binary features (e.g., `skill_python`, `skill_machine_learning`) and the undergraduate course encoding contribute most to classification decisions.

*(Insert Figure 18: Confusion Matrix)*

The confusion matrix shows the distribution of correct and incorrect predictions across all 24 career categories, identifying which careers the model classifies most accurately and where misclassification patterns exist (e.g., confusion between related careers like "Data Scientist" and "Data Analyst").

*(Insert Figure 19: Cross-Validation Accuracy per Fold)*

The 5-fold cross-validation results demonstrate the model's stability across different data partitions, with the standard deviation indicating consistency of performance.

---

## 6. Conclusion

This project set out to design, implement, and evaluate an AI-powered career guidance system — Skill Lantern — that provides personalised, data-driven career recommendations, actionable learning roadmaps, and institution-specific guidance for Nepalese students and early-career professionals. Reflecting on the aims and objectives, the following conclusions can be drawn:

**Objective 1 (XGBoost career prediction model):** Successfully delivered. The XGBoost multi-class classifier was trained on the career_recommender.csv survey dataset, implementing a complete feature engineering pipeline covering gender encoding, course encoding, CGPA normalisation, and multi-label binarisation of skills and interests. The model predicts across 24 career categories using the `multi:softprob` objective, returning ranked predictions with calibrated confidence scores. 5-fold stratified cross-validation and held-out test evaluation provide quantitative assessment of prediction quality.

**Objective 2 (LLaMA 3 integration for NLG):** Successfully delivered. The OllamaService class enables communication with a locally hosted LLaMA 3 model, generating three-stage career roadmaps (with stage-specific skills, resources, and milestones), contextualised college recommendations, and personalised career summaries. Prompt engineering ensures structured JSON outputs parseable by the frontend.

**Objective 3 (Full-stack web application):** Successfully delivered. The platform provides a Next.js 16 frontend with a 6-step multi-step registration form (collecting 15+ profile attributes), NextAuth.js v5 authentication with bcrypt password hashing, and an interactive dashboard displaying predictions, roadmaps, and college recommendations. The React 19 component architecture and Tailwind CSS 4 styling provide a responsive, modern user interface.

**Objective 4 (Nepal college dataset integration):** Successfully delivered. A curated dataset of ~1,400 Nepalese educational institutions is loaded and filtered by career relevance, location preference, budget range, and degree level. LLaMA 3 optionally generates contextual explanations for why specific colleges are recommended.

**Objective 5 (Rule-based fallback system):** Successfully delivered. The CareerPredictor class implements a deterministic fallback using a skill-to-career mapping dictionary covering 50+ skills and interests. This ensures recommendations are always available even when the XGBoost model is not loaded or when user profiles fall outside the training distribution.

**Objective 6 (Model evaluation):** Successfully delivered. The model is evaluated using accuracy, top-3 accuracy, top-5 accuracy, per-class precision/recall/F1-score, confusion matrices, and 5-fold cross-validation. Feature importance analysis reveals which input attributes most influence predictions.

**Addressing the Academic Question:** The project demonstrates that a hybrid AI architecture combining gradient-boosted decision trees (XGBoost) for career classification with a large language model (LLaMA 3) for personalised content generation can be effectively integrated into a web-based career guidance system. The hybrid approach leverages each component's strengths: XGBoost provides quantitative, empirically grounded career predictions based on learned patterns in structured survey data, while LLaMA 3 provides qualitative, contextually rich guidance (roadmaps, summaries, college explanations) that a traditional classifier alone cannot generate. The rule-based fallback ensures system reliability, and the RESTful API architecture enables clean separation between the AI components and the web application.

Key discoveries from the development process include: (1) feature engineering quality — particularly the encoding of multi-select skill and interest fields — significantly impacts classification accuracy, often more than hyperparameter tuning; (2) the hybrid ML+LLM architecture provides complementary capabilities that neither component offers alone; (3) a rule-based fallback is essential for production reliability, ensuring the system degrades gracefully when ML components are unavailable; and (4) prompt engineering for structured JSON output from LLaMA 3 requires careful template design and robust parsing to handle the variability inherent in LLM-generated text.

---

## 7. Critical Evaluation of the Project

### Report Evaluation

This report documents the complete development lifecycle of Skill Lantern, from initial research and dataset analysis through model training, system implementation, and evaluation. A strength of the report is the detailed documentation of the feature engineering pipeline and the dual AI architecture (XGBoost + LLaMA 3), providing transparency into how the system processes user data and generates recommendations. The literature review covers relevant research across career recommendation systems, gradient boosting algorithms, and LLM applications, though deeper engagement with domain-specific career counselling literature could strengthen the theoretical context.

### System Evaluation

The Skill Lantern platform delivers on its core premise of providing AI-powered career guidance through a user-friendly web interface. Key strengths include:

- **Hybrid AI architecture:** The combination of XGBoost for structured prediction and LLaMA 3 for natural language generation provides both quantitative rigour and qualitative richness.
- **Comprehensive user profiling:** The 6-step registration form captures a wide range of attributes (15+ fields) that provide the model with sufficient information for meaningful predictions.
- **Rule-based fallback:** Ensures the system always provides recommendations, maintaining user trust even when ML components are unavailable.
- **Nepal-specific context:** The college dataset and career categories are tailored to the Nepalese education system and job market.

Limitations include:

- **Dataset constraints:** The survey dataset's size and sampling methodology may limit the generalisability of predictions. Career categories with very few training samples may have lower prediction accuracy.
- **LLM dependency:** Roadmap and summary quality depend on LLaMA 3's capabilities and the Ollama server's availability. Without Ollama, these features are unavailable.
- **Static college data:** The college dataset is loaded from a CSV file and does not update automatically, meaning new institutions or programmes are not reflected until the CSV is manually updated.
- **Single-session architecture:** The system does not track user career progression over time or adapt recommendations based on feedback.

### Process Evaluation

The Agile methodology proved appropriate for this project, enabling iterative development of the machine learning pipeline and progressive integration of system components. Regular supervisor meetings provided valuable feedback that guided feature engineering decisions and UI design improvements. The use of Git for version control enabled systematic progress tracking.

Areas for improvement include: more comprehensive automated testing (unit tests for the prediction pipeline, integration tests for API endpoints), earlier user testing to gather feedback on the registration flow and dashboard UX, and more structured sprint documentation.

### Planning and Management

The project timeline was broadly appropriate, though the complexity of the feature engineering pipeline (handling diverse skill formats, career category mapping from free-text job titles) consumed more time than initially estimated. The Gantt chart tracked major milestones, though more granular task tracking could improve future project management.

### Quality of Sources

The literature review draws from peer-reviewed papers spanning 2016–2024, covering the foundational XGBoost paper, transformer architecture, LLaMA model family, and career recommendation applications. Additional technical documentation (library READMEs, framework docs) was used for implementation guidance.

### Self-Reflection

This project has been a significant learning experience across multiple dimensions. Technically, I gained practical knowledge of supervised machine learning — from data preprocessing and feature engineering through model training, hyperparameter tuning, and evaluation. Working with XGBoost on a real-world classification task revealed the critical importance of feature engineering: the quality of skill and interest encoding directly impacted prediction accuracy, often more than changes to model hyperparameters.

The integration of LLaMA 3 via Ollama introduced me to the practical realities of working with large language models — prompt engineering for structured output, parsing variable LLM responses, managing inference latency, and handling cases where the LLM produces malformed or unexpected outputs. Developing the `parse_json_response()` method, which handles JSON embedded in markdown blocks, raw JSON, and nested structures, taught me the importance of robust error handling when working with generative AI.

From a software engineering perspective, I developed skills in full-stack development spanning a Python backend (FastAPI), a TypeScript/React frontend (Next.js 16), database management (PostgreSQL via Prisma), and third-party service integration (Ollama, NextAuth.js). The experience of building API contracts between the frontend and backend — defining Pydantic schemas on the backend and TypeScript types on the frontend — highlighted the value of type-safe data exchange in multi-service architectures.

Professionally, this project improved my project management skills through iterative planning, regular progress tracking (logsheets), and the discipline of incremental delivery. Working on an end-to-end system from research through deployment gave me confidence in tackling complex software projects independently.

If I were to undertake this project again, I would: (a) invest more time in data collection, potentially conducting a more comprehensive survey to increase dataset size and diversity; (b) implement a user feedback mechanism to enable continuous model improvement; (c) explore additional ML algorithms (e.g., LightGBM, neural networks) for comparison; and (d) conduct user studies to evaluate the perceived usefulness and accuracy of the recommendations from the perspective of Nepalese students.

---

## 8. Evidence of Project Management

Project management was carried out through a combination of weekly supervision meetings, milestone tracking, and version-controlled development workflow. Progress was reviewed in regular supervisor meetings and documented in signed log sheets.

### Log Sheets — Signed and Scanned by Supervisor

*(Insert scanned log sheets here)*

### Gantt Chart

*(Insert Figure 20: Full Gantt Chart)*

The Gantt chart tracks the following major milestones:

| Phase | Duration | Key Deliverables |
|-------|----------|-----------------|
| Project Initiation | Weeks 1–6 | Proposal, initial research |
| Literature Review | Weeks 5–12 | Research paper survey, existing systems analysis |
| Dataset Analysis & Feature Engineering | Weeks 10–16 | Data preprocessing pipeline, feature encoding |
| Model Training & Evaluation | Weeks 14–20 | XGBoost training, cross-validation, hyperparameter tuning |
| Backend Development | Weeks 18–26 | FastAPI API, Ollama integration, service layer |
| Frontend Development | Weeks 22–30 | Next.js app, registration form, dashboard |
| Integration & Testing | Weeks 28–34 | End-to-end testing, bug fixes, UX refinement |
| Report Writing | Weeks 32–40 | Draft report, final report |
| Final Submission | Weeks 40–47 | Defense preparation, final submission |

---

## 9. References and Bibliography

[1] Chen, T. and Guestrin, C. (2016) 'XGBoost: A Scalable Tree Boosting System', in *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, pp. 785–794.

[2] Friedman, J.H. (2001) 'Greedy Function Approximation: A Gradient Boosting Machine', *Annals of Statistics*, 29(5), pp. 1189–1232.

[3] Vaswani, A. et al. (2017) 'Attention Is All You Need', in *Advances in Neural Information Processing Systems (NeurIPS)*, pp. 5998–6008.

[4] Touvron, H. et al. (2023) 'LLaMA: Open and Efficient Foundation Language Models', *arXiv preprint arXiv:2302.13971*.

[5] Garg, A. and Sharma, R. (2021) 'Career Recommendation System Using Machine Learning', *International Journal of Advanced Research in Computer Science*, 12(3), pp. 45–52.

[6] Mohamed, A. et al. (2022) 'Student Career Prediction Using Machine Learning', *International Journal of Computer Applications*, 183(45), pp. 1–6.

[7] Sharma, P. and Kumar, D. (2020) 'Career Counselling Expert System Using Machine Learning', *Journal of Emerging Technologies and Innovative Research*, 7(5), pp. 15–22.

[8] Nie, L. et al. (2022) 'Recommendation Systems in Education: A Survey', *ACM Computing Surveys*, 54(6), pp. 1–36.

[9] Prokhorenkova, L. et al. (2018) 'CatBoost: Unbiased Boosting with Categorical Features', in *Advances in Neural Information Processing Systems (NeurIPS)*, pp. 6638–6648.

[10] Bhalke, S. and Doifode, V. (2023) 'AI-Based Career Guidance System', *International Journal of Scientific Research in Computer Science*, 8(2), pp. 1–7.

[11] Grinsztajn, L., Oyallon, E. and Varoquaux, G. (2022) 'Why do tree-based models still outperform deep learning on typical tabular data?', in *Advances in Neural Information Processing Systems (NeurIPS)*, 35.

[12] Pedregosa, F. et al. (2011) 'Scikit-learn: Machine Learning in Python', *Journal of Machine Learning Research*, 12, pp. 2825–2830.

[13] Tiangolo, S. (2020) *FastAPI Documentation*. Available at: https://fastapi.tiangolo.com (Accessed: January 2026).

[14] Vercel (2024) *Next.js Documentation*. Available at: https://nextjs.org/docs (Accessed: January 2026).

[15] Meta AI (2024) *Ollama Documentation*. Available at: https://ollama.ai (Accessed: January 2026).

[16] Prisma (2024) *Prisma Documentation*. Available at: https://www.prisma.io/docs (Accessed: January 2026).

[17] NextAuth.js (2024) *NextAuth.js Documentation*. Available at: https://next-auth.js.org (Accessed: January 2026).

---

## 10. Appendices

### Appendix A: Mathematical Derivations

**A) XGBoost Additive Model**

$$\hat{y}_i = \sum_{k=1}^{K} f_k(x_i), \quad f_k \in \mathcal{F}$$

where $\mathcal{F}$ is the space of regression trees.

**B) Regularised Objective Function**

$$\mathcal{L} = \sum_{i=1}^{n} l(y_i, \hat{y}_i) + \sum_{k=1}^{K} \Omega(f_k)$$

$$\Omega(f) = \gamma T + \frac{1}{2}\lambda \sum_{j=1}^{T} w_j^2$$

where $T$ is the number of leaves and $w_j$ is the weight of leaf $j$.

**C) Second-Order Taylor Approximation**

At step $t$, the objective is approximated as:

$$\tilde{\mathcal{L}}^{(t)} = \sum_{i=1}^{n} \left[ g_i f_t(x_i) + \frac{1}{2} h_i f_t^2(x_i) \right] + \Omega(f_t)$$

where $g_i = \partial_{\hat{y}^{(t-1)}} l(y_i, \hat{y}^{(t-1)})$ and $h_i = \partial^2_{\hat{y}^{(t-1)}} l(y_i, \hat{y}^{(t-1)})$ are the first and second order gradients.

**D) Multi-class Softmax (Softprob)**

$$P(y = c | x) = \frac{\exp(z_c)}{\sum_{j=1}^{C} \exp(z_j)}$$

**E) Multi-class Cross-Entropy Loss**

$$L = -\sum_{i=1}^{n} \sum_{c=1}^{C} y_{ic} \log(p_{ic})$$

**F) Self-Attention (Transformer — used in LLaMA 3)**

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

### Appendix B: User Manual

**Web Application:**

1. Navigate to the Skill Lantern homepage.
2. Click 'Get Started' or 'Sign Up' in the navigation bar.
3. Complete the 6-step registration form:
   - **Step 1:** Enter personal information (full name, gender, date of birth, city/region)
   - **Step 2:** Enter education details (course category, course name, specialisation, college, CGPA)
   - **Step 3:** Select your technical skills from the provided list (multi-select)
   - **Step 4:** Select your areas of interest (multi-select)
   - **Step 5:** Enter certification information
   - **Step 6:** Set career preferences (career lifestyle, work environment, location, learning style)
4. Submit the registration form to create your account.
5. Log in with your email and password.
6. View your personalised dashboard showing:
   - **Career Predictions:** Top predicted careers with confidence percentages
   - **Career Roadmap:** Three-stage learning path (Beginner → Intermediate → Advanced)
   - **College Recommendations:** Relevant Nepalese colleges with programme details

### Appendix C: System Configuration

**Backend Setup:**
- Python 3.10+ with virtual environment
- Install dependencies: `pip install -r requirements.txt`
- Configure `.env` with Ollama host/port settings
- Train the model: `python train_model.py`
- Run: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

**Frontend Setup:**
- Node.js 18+ with npm
- Install dependencies: `npm install`
- Configure `.env.local` with `DATABASE_URL`, `NEXTAUTH_SECRET`, `NEXT_PUBLIC_API_URL`
- Set up database: `npx prisma generate && npx prisma db push`
- Run: `npm run dev` (development) or `npm run build && npm start` (production)

**Environment Variables:**

| Variable | Description | Example |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | postgresql://user:pass@localhost:5432/skilllantern |
| NEXTAUTH_SECRET | JWT encryption secret | (random 32-char string) |
| NEXT_PUBLIC_API_URL | FastAPI backend URL | http://localhost:8000 |
| OLLAMA_HOST | Ollama inference server URL | http://localhost:11434 |
| OLLAMA_MODEL | LLaMA model name | llama3 |

### Appendix D: API Endpoint Reference

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|-------------|----------|
| /api/predict | POST | Career prediction | UserProfile | CareerPredictionResponse |
| /api/roadmap | POST | Roadmap generation | RoadmapRequest | RoadmapResponse |
| /api/colleges | POST | College recommendations | CollegeRequest | CollegeRecommendationResponse |
| /api/recommendations/full | POST | Full career guidance | FullRecommendationRequest | FullRecommendationResponse |
| /api/health | GET | Health check | — | HealthResponse |
| /api/config | GET | Configuration info | — | JSON |
