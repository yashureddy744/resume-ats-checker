# Resume ATS Checker — AI Powered

An AI-powered Resume ATS (Applicant Tracking System) score checker 
built with GPT-4, LangChain, and FastAPI that analyzes resumes against 
job descriptions and provides detailed scoring and improvement recommendations.

## What This Project Does
- Scores your resume against any job description (0-100)
- Identifies matched and missing ATS keywords
- Gives keyword match score, format score, experience match score
- Lists specific strengths and improvement areas
- Provides PASS/FAIL recommendation
- Returns actionable feedback to improve resume

## Tech Stack
- Python, FastAPI
- LangChain, OpenAI GPT-4
- Pydantic data validation
- Docker, AWS ECS
- GitHub Actions CI/CD

## API Endpoints
- GET  /            — Health check
- POST /check-ats   — Full ATS analysis
- POST /quick-score — Quick score summary

## Sample Response
```json
{
  "ats_score": 78,
  "keyword_match_score": 82,
  "format_score": 90,
  "experience_match_score": 65,
  "matched_keywords": ["Java", "Spring Boot", "AWS", "Microservices"],
  "missing_keywords": ["Kafka", "GraphQL", "Terraform"],
  "strengths": [
    "Strong Java and Spring Boot experience matches JD",
    "AWS cloud experience aligns with requirements",
    "Microservices architecture experience is relevant"
  ],
  "improvements": [
    "Add Kafka experience to resume",
    "Mention GraphQL API experience",
    "Include Terraform IaC projects"
  ],
  "overall_recommendation": "Strong candidate with good keyword alignment...",
  "pass_fail": "PASS"
}
```

## How to Run
```bash
git clone https://github.com/yashureddy744/resume-ats-checker
cd resume-ats-checker
pip install -r requirements.txt
export OPENAI_API_KEY=your_key_here
python app.py
```

## Author
**Yashwanth Reddy Kistipati**  
Software Engineer | Java · Spring Boot · Angular · React · LangChain · AWS  
[LinkedIn](https://linkedin.com/in/yashwanth-reddy-kistipati)
