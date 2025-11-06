from flask import Flask, request, jsonify
import PyPDF2
import docx2txt
import io
import re

app = Flask(__name__)

def simple_similarity(text1, text2):
    words1 = set(re.findall(r'\b\w+\b', text1.lower()))
    words2 = set(re.findall(r'\b\w+\b', text2.lower()))
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    return intersection / union if union > 0 else 0

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Resume Selector</title>
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        .card { background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
        .content { padding: 40px; }
        .form-group { margin-bottom: 25px; }
        label { display: block; font-weight: 600; margin-bottom: 8px; color: #333; }
        textarea { width: 100%; height: 120px; padding: 15px; border: 2px solid #e1e5e9; border-radius: 8px; }
        input[type="file"] { width: 100%; padding: 15px; border: 2px dashed #667eea; border-radius: 8px; background: #f8f9ff; }
        button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; width: 100%; }
        button:disabled { background: #ccc; }
        .success { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 25px; border-radius: 10px; text-align: center; margin-top: 20px; }
        .error { background: #ff6b6b; color: white; padding: 20px; border-radius: 8px; text-align: center; margin-top: 20px; }
    </style>
</head>
<body>
    <div id="root"></div>
    
    <script type="text/babel">
        const { useState } = React;
        
        function App() {
            const [jobDescription, setJobDescription] = useState('');
            const [files, setFiles] = useState([]);
            const [loading, setLoading] = useState(false);
            const [result, setResult] = useState(null);
            const [error, setError] = useState('');
            
            const handleSubmit = async (e) => {
                e.preventDefault();
                
                if (!jobDescription.trim()) {
                    setError('Please enter a job description');
                    return;
                }
                
                if (files.length < 2) {
                    setError('Please select at least 2 resume files');
                    return;
                }
                
                setLoading(true);
                setError('');
                setResult(null);
                
                const formData = new FormData();
                formData.append('job_description', jobDescription);
                
                Array.from(files).forEach(file => {
                    formData.append('files', file);
                });
                
                try {
                    const response = await fetch('/select', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    
                    if (data.status === 'success') {
                        setResult(data);
                    } else {
                        setError(data.message);
                    }
                } catch (err) {
                    setError('Processing error occurred');
                } finally {
                    setLoading(false);
                }
            };
            
            return React.createElement('div', { className: 'container' },
                React.createElement('div', { className: 'card' },
                    React.createElement('div', { className: 'header' },
                        React.createElement('h1', null, '🎯 Resume Selector'),
                        React.createElement('p', null, 'Find the best matching resume using keyword analysis')
                    ),
                    React.createElement('div', { className: 'content' },
                        React.createElement('form', { onSubmit: handleSubmit },
                            React.createElement('div', { className: 'form-group' },
                                React.createElement('label', null, '📝 Job Description'),
                                React.createElement('textarea', {
                                    value: jobDescription,
                                    onChange: (e) => setJobDescription(e.target.value),
                                    placeholder: 'Enter job description here...',
                                    required: true
                                })
                            ),
                            React.createElement('div', { className: 'form-group' },
                                React.createElement('label', null, '📄 Upload Resume Files'),
                                React.createElement('input', {
                                    type: 'file',
                                    multiple: true,
                                    accept: '.pdf,.docx',
                                    onChange: (e) => setFiles(e.target.files),
                                    required: true
                                }),
                                React.createElement('small', null, 'Select 2 or more resume files (PDF or DOCX)')
                            ),
                            React.createElement('button', {
                                type: 'submit',
                                disabled: loading
                            }, loading ? '⏳ Analyzing...' : '🔍 Find Best Resume')
                        ),
                        error && React.createElement('div', { className: 'error' },
                            React.createElement('strong', null, '❌ Error: '), error
                        ),
                        result && React.createElement('div', { className: 'success' },
                            React.createElement('h3', null, '🏆 Best Match Found!'),
                            React.createElement('div', { style: { fontSize: '1.3em', margin: '10px 0' } },
                                '📄 ' + result.best_resume.name
                            ),
                            React.createElement('div', { style: { fontSize: '1.2em', margin: '10px 0' } },
                                '📊 Match Score: ' + (result.best_resume.similarity_score * 100).toFixed(1) + '%'
                            ),
                            React.createElement('p', null, 'Selected from ' + result.total_resumes + ' candidates')
                        )
                    )
                )
            );
        }
        
        ReactDOM.render(React.createElement(App), document.getElementById('root'));
    </script>
</body>
</html>
    '''

@app.route('/select', methods=['POST'])
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
        
        best_resume = max(similarities, key=lambda x: x[1])
        best_name, best_score = best_resume
        
        return jsonify({
            "status": "success",
            "best_resume": {
                "name": best_name,
                "similarity_score": float(best_score)
            },
            "total_resumes": len(names)
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Processing error: {str(e)}"})

if __name__ == '__main__':
    print("🚀 Starting Resume Selection System...")
    print("📍 Open: http://127.0.0.1:4000")
    app.run(host='127.0.0.1', port=4000, debug=False)