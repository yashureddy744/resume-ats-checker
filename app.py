from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import json
import re
import uvicorn

app = FastAPI(title="Resume ATS Checker — AI Powered")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

class ATSRequest(BaseModel):
    resume_text: str
    job_description: str

class ATSResponse(BaseModel):
    ats_score: int
    keyword_match_score: int
    format_score: int
    experience_match_score: int
    matched_keywords: list
    missing_keywords: list
    strengths: list
    improvements: list
    overall_recommendation: str
    pass_fail: str

ATS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert ATS (Applicant Tracking System) analyzer with 
    20 years of recruiting experience. Analyze the resume against the job description
    and return ONLY a JSON response with no other text.
    
    Return exactly this JSON structure:
    {{
        "ats_score": <overall score 0-100>,
        "keyword_match_score": <score 0-100>,
        "format_score": <score 0-100>,
        "experience_match_score": <score 0-100>,
        "matched_keywords": ["keyword1", "keyword2", ...],
        "missing_keywords": ["keyword1", "keyword2", ...],
        "strengths": ["strength1", "strength2", "strength3"],
        "improvements": ["improvement1", "improvement2", "improvement3"],
        "overall_recommendation": "detailed recommendation in 2-3 sentences",
        "pass_fail": "PASS" or "FAIL"
    }}"""),
    ("human", """
    RESUME:
    {resume_text}
    
    JOB DESCRIPTION:
    {job_description}
    
    Analyze and return JSON only.
    """)
])

@app.get("/")
def root():
    return {
        "message": "Resume ATS Checker — AI Powered",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "model": "gpt-4-turbo"}

@app.post("/check-ats", response_model=ATSResponse)
async def check_ats(request: ATSRequest):
    try:
        if len(request.resume_text.strip()) < 100:
            raise HTTPException(
                status_code=400,
                detail="Resume text too short. Please provide full resume."
            )
        if len(request.job_description.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Job description too short. Please provide full JD."
            )

        chain = ATS_PROMPT | llm
        result = chain.invoke({
            "resume_text": request.resume_text,
            "job_description": request.job_description
        })

        response_text = result.content.strip()
        response_text = re.sub(r'```json\n?', '', response_text)
        response_text = re.sub(r'```\n?', '', response_text)

        parsed = json.loads(response_text)

        return ATSResponse(
            ats_score=parsed.get("ats_score", 0),
            keyword_match_score=parsed.get("keyword_match_score", 0),
            format_score=parsed.get("format_score", 0),
            experience_match_score=parsed.get("experience_match_score", 0),
            matched_keywords=parsed.get("matched_keywords", []),
            missing_keywords=parsed.get("missing_keywords", []),
            strengths=parsed.get("strengths", []),
            improvements=parsed.get("improvements", []),
            overall_recommendation=parsed.get("overall_recommendation", ""),
            pass_fail=parsed.get("pass_fail", "FAIL")
        )

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse AI response: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/quick-score")
async def quick_score(request: ATSRequest):
    result = await check_ats(request)
    return {
        "ats_score": result.ats_score,
        "pass_fail": result.pass_fail,
        "top_missing_keywords": result.missing_keywords[:5],
        "top_strength": result.strengths[0] if result.strengths else ""
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
