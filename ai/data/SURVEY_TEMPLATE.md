# Skill Lantern - Data Collection Survey Template

This document provides the structure for creating a Google Form to collect real training data from students in Nepal.

## Survey Structure

### Section 1: Basic Information
*(Optional - for tracking only)*

1. **Email** (Optional)
   - Type: Short answer
   - Purpose: Follow-up if needed

2. **Age Group**
   - Type: Multiple choice
   - Options: 15-18, 19-22, 23-26, 27+

3. **Gender** (Optional)
   - Type: Multiple choice
   - Options: Male, Female, Other, Prefer not to say

---

### Section 2: Academic Performance
*(Required)*

4. **Mathematics Score (0-100)**
   - Type: Linear scale or Short answer (number)
   - Description: "Enter your average/latest math score"

5. **Science Score (0-100)**
   - Type: Linear scale or Short answer (number)
   - Description: "Enter your average/latest science score"

6. **English Score (0-100)**
   - Type: Linear scale or Short answer (number)
   - Description: "Enter your average/latest English score"

7. **Overall GPA (0-4.0)**
   - Type: Short answer (number)
   - Description: "Enter your GPA. If percentage, convert: 90%+ = 4.0, 80-89% = 3.5, 70-79% = 3.0, 60-69% = 2.5"

8. **Current Academic Level**
   - Type: Multiple choice
   - Options:
     - SEE/SLC Student
     - +2 / Higher Secondary
     - Bachelor's Degree
     - Master's Degree
     - Already Working

---

### Section 3: Skills Assessment
*(Required - Rate 1-5: 1=Very Low, 5=Very High)*

9. **Programming / Coding**
   - Type: Linear scale 1-5

10. **Communication Skills**
    - Type: Linear scale 1-5

11. **Analytical Thinking**
    - Type: Linear scale 1-5

12. **Problem Solving**
    - Type: Linear scale 1-5

13. **Creativity**
    - Type: Linear scale 1-5

14. **Leadership**
    - Type: Linear scale 1-5

15. **Teamwork**
    - Type: Linear scale 1-5

16. **Attention to Detail**
    - Type: Linear scale 1-5

17. **Time Management**
    - Type: Linear scale 1-5

18. **Stress Management**
    - Type: Linear scale 1-5

19. **Empathy / Understanding Others**
    - Type: Linear scale 1-5

20. **Technical / Computer Skills**
    - Type: Linear scale 1-5

21. **Presentation Skills**
    - Type: Linear scale 1-5

22. **Project Management**
    - Type: Linear scale 1-5

23. **Dedication / Persistence**
    - Type: Linear scale 1-5

24. **Integrity / Ethics**
    - Type: Linear scale 1-5

25. **Patience**
    - Type: Linear scale 1-5

---

### Section 4: Interests
*(Required - Rate 1-5: 1=Not Interested, 5=Very Interested)*

26. **Technology & Computers**
    - Type: Linear scale 1-5

27. **Engineering & Building Things**
    - Type: Linear scale 1-5

28. **Healthcare & Medicine**
    - Type: Linear scale 1-5

29. **Business & Entrepreneurship**
    - Type: Linear scale 1-5

30. **Arts & Design**
    - Type: Linear scale 1-5

31. **Education & Teaching**
    - Type: Linear scale 1-5

32. **Research & Discovery**
    - Type: Linear scale 1-5

33. **Helping Others / Social Work**
    - Type: Linear scale 1-5

34. **Finance & Money Management**
    - Type: Linear scale 1-5

35. **Law & Legal Matters**
    - Type: Linear scale 1-5

36. **Construction & Infrastructure**
    - Type: Linear scale 1-5

37. **Environment & Nature**
    - Type: Linear scale 1-5

---

### Section 5: Career Choice
*(Required - This is the training label)*

38. **What is your chosen/current career or the career you are pursuing?**
    - Type: Dropdown or Multiple choice
    - Options:
      - Software Engineer / Developer
      - Data Scientist / Analyst
      - Doctor (MBBS)
      - Civil Engineer
      - Graphic Designer
      - Business Analyst
      - Chartered Accountant (CA)
      - Teacher / Educator
      - Marketing Manager
      - Nurse
      - Mechanical Engineer
      - Architect
      - Lawyer
      - Journalist
      - Pharmacist
      - Banker
      - Entrepreneur
      - Chef / Hospitality
      - Pilot
      - Other (please specify)

39. **If "Other", please specify:**
    - Type: Short answer
    - Conditional: Show only if "Other" selected

40. **How confident are you in your career choice?**
    - Type: Linear scale 1-5
    - Description: "1 = Not sure at all, 5 = Very confident"

---

## Google Form Setup Instructions

1. Go to [Google Forms](https://forms.google.com)
2. Create a new form titled "Skill Lantern - Career Survey"
3. Add the sections and questions as listed above
4. Enable "Collect email addresses" if you want to follow up
5. Enable "Limit to 1 response" to prevent duplicates

### Sharing Strategy

1. **Schools & Colleges**: Contact +2 and bachelor's level institutions in Nepal
2. **Social Media**: Share on Facebook groups for students in Nepal
3. **University Forums**: Post in TU, KU, PU student groups
4. **Career Counseling Centers**: Partner with guidance counselors
5. **Alumni Networks**: Reach out to recent graduates

### Target: 500+ Responses

---

## Data Export

1. In Google Forms, go to "Responses" tab
2. Click the Google Sheets icon to create a spreadsheet
3. Download as CSV
4. Rename columns to match the training data format:
   - `math_score`, `science_score`, `english_score`, `gpa`
   - `skill_programming`, `skill_communication`, etc.
   - `interest_technology`, `interest_engineering`, etc.
   - `career_label`
5. Save to `ai/data/raw/survey_data.csv`

---

## Data Processing Script

After collecting data, run:

```bash
cd ai
python -m training.process_survey_data
```

This will:
1. Load the raw survey data
2. Clean and validate entries
3. Map responses to the correct format
4. Merge with existing training data
5. Save to `data/processed/career_dataset.csv`
