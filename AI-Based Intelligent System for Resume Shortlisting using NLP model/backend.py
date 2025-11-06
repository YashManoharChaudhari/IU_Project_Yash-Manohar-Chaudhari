from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import docx2txt
import io
import re

app = Flask(__name__)
CORS(app)

def simple_similarity(text1, text2):
    words1 = set(re.findall(r'\b\w+\b', text1.lower()))
    words2 = set(re.findall(r'\b\w+\b', text2.lower()))
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    return intersection / union if union > 0 else 0

@app.route('/api/select', methods=['POST'])
def select_resume():
    try:
        job_desc = request.form.get('job_description', '').strip()
        files = request.files.getlist('files')
        
        if not job_desc:
            return jsonify({"status": "error", "message": "Job description is required"})
        
        if len(files) < 2:
            return jsonify({"status": "error", "message": "Please upload at least 2 resume files"})
        
        resume_texts = []
        names = []
        
        for file in files:
            if not file.filename:
                continue
                
            try:
                content = file.read()
                
                if file.filename.lower().endswith('.pdf'):
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
                    text = "".join([page.extract_text() for page in pdf_reader.pages])
                elif file.filename.lower().endswith('.docx'):
                    text = docx2txt.process(io.BytesIO(content))
                else:
                    continue
                
                if len(text.strip()) > 50:
                    resume_texts.append(text)
                    names.append(file.filename)
                    
            except Exception as e:
                print(f"Error processing {file.filename}: {e}")
                continue
        
        if len(resume_texts) < 2:
            return jsonify({"status": "error", "message": "Could not extract text from enough resume files"})
        
        similarities = []
        for i, resume_text in enumerate(resume_texts):
            similarity = simple_similarity(job_desc, resume_text)
            similarities.append((names[i], similarity))
        
        # Sort by similarity score (highest first)
        ranked_resumes = sorted(similarities, key=lambda x: x[1], reverse=True)
        
        return jsonify({
            "status": "success",
            "ranked_resumes": [
                {"name": name, "similarity_score": float(score)}
                for name, score in ranked_resumes
            ],
            "total_resumes": len(names)
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Processing error: {str(e)}"})

if __name__ == '__main__':
    print("🚀 Backend running on: http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False)