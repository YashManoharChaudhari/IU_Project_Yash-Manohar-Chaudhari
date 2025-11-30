from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer, util
from pydantic import BaseModel
from typing import List
import PyPDF2
import docx2txt
import io
import re

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Sentence-BERT
model = SentenceTransformer("all-MiniLM-L6-v2")

class RankedResume(BaseModel):
    name: str
    similarity_score: float
    rank: int

class ResumeRankResponse(BaseModel):
    status: str
    ranked_resumes: List[RankedResume]
    total_resumes: int

# Extract text from PDF
async def extract_pdf(content: bytes) -> str:
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
    return "".join([page.extract_text() for page in pdf_reader.pages])

# Extract text from DOCX
async def extract_docx(content: bytes) -> str:
    return docx2txt.process(io.BytesIO(content))


@app.post("/api/select", response_model=ResumeRankResponse)
async def select_resume(
    job_description: str = Form(...),
    files: List[UploadFile] = File(...)
):
    job_desc = job_description.strip()

    if not job_desc:
        return {"status": "error", "message": "Job description is required", "ranked_resumes": [], "total_resumes": 0}

    if len(files) < 2:
        return {"status": "error", "message": "Please upload at least 2 resumes", "ranked_resumes": [], "total_resumes": 0}

    resume_texts = []
    names = []

    # Extract text from resumes
    for file in files:
        if not file.filename:
            continue

        try:
            content = await file.read()

            if file.filename.lower().endswith(".pdf"):
                text = await extract_pdf(content)
            elif file.filename.lower().endswith(".docx"):
                text = await extract_docx(content)
            else:
                continue

            if len(text.strip()) > 50:
                resume_texts.append(text)
                names.append(file.filename)

        except Exception:
            continue

    if len(resume_texts) < 2:
        return {"status": "error", "message": "Could not extract enough resumes", "ranked_resumes": [], "total_resumes": 0}

    # Embed job description and resumes
    jd_emb = model.encode(job_desc, convert_to_tensor=True)
    resume_embs = model.encode(resume_texts, convert_to_tensor=True)

    # Compute cosine similarities
    sims = util.cos_sim(jd_emb, resume_embs)[0]

    ranked = []
    for i, score in enumerate(sims):
        ranked.append({
            "name": names[i],
            "similarity_score": float(score)
        })

    # Sort by similarity score and add ranks
    ranked_sorted = sorted(ranked, key=lambda x: x["similarity_score"], reverse=True)
    for i, resume in enumerate(ranked_sorted):
        resume["rank"] = i + 1

    return {
        "status": "success",
        "ranked_resumes": ranked_sorted,
        "total_resumes": len(names)
    }


# Run with: uvicorn main:app --reload