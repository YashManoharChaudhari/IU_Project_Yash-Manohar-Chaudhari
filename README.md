# IU_Project_Yash-Manohar-Chaudhari
## ABSTRACT


Companies receive hundreds of resumes for a single available post in today’s competitive market, which makes the manual process of resume shortlisting feel like a laborious and time-consuming procedure. Recruiters may sometimes overlook qualified candidates due to human bias and fatigue. To solve this issue, this project aims to develop an AI-based intelligent system for resume shortlisting using Natural Language Processing (NLP).
This system will automatically extract information from the resumes such as qualifications, work experience and skills and compare it with the requirements mentioned in the job description. We will be using an NLP model such as Sentence-BERT(S-BERT). This system will analyze and match the similarity between the candidates resume and job description and based on this result it will rank the candidates based on relevance rather than just keyword matching.
The aim of building this intelligent system is to make the hiring process automated and simple, increase accuracy and minimize errors in candidate selection. The outcome of this project is an efficient and user-friendly tool to help the HR department in finding the best candidate quickly and objectively, saving time and upgrading the hiring process.

## 🎯 Goals of the Project

### 1. Automation of Resume Screening  
To develop an intelligent system that automates the process of shortlisting resumes, reducing the need for manual intervention by recruiters.  

### 2. Accurate Candidate–Job Matching  
To use advanced NLP models such as Sentence-BERT (S-BERT) to analyze and measure the semantic similarity between resumes and job descriptions for precise candidate matching.  

### 3. Reduction of Human Bias and Errors  
To minimize subjective bias, fatigue, and human errors in the recruitment process by introducing an objective, data-driven selection mechanism.  

### 4. Efficient Information Extraction  
To automatically extract key details such as qualifications, experience, and skills from unstructured resume text using NLP techniques.  

### 5. Candidate Ranking System  
To design a ranking algorithm that scores and orders candidates based on their relevance to the job requirements.  

### 6. Enhanced Recruitment Efficiency  
To significantly reduce the time and effort spent on initial candidate screening, enabling HR departments to focus on strategic decision-making.  

### 7. User-Friendly Interface  
To provide a simple and intuitive interface for HR professionals to upload job descriptions and resumes, view rankings, and access shortlisting results easily.  


## 🛠️ Tech Stack

| Category               | Technology / Tool            | Purpose                                                                                 |
|------------------------|-----------------------------|-----------------------------------------------------------------------------------------|
| **Programming Language** | Python 3.x                 | Primary language for AI, NLP, and backend development                                   |
| **Frontend**            | React                  | Interactive and user-friendly interface                                                |
| **Backend**             | Flask                      | Lightweight backend for handling requests and processing resumes                        |
| **NLP & Embeddings**    | Sentence-BERT (S-BERT)     | Semantic similarity computation between resumes and job descriptions                                                                         |
| **API**                 | Flask / FastAPI            | Web API for uploading resumes and job descriptions                                       |
| **Deployment**          | Docker                     | Containerize application for easy deployment                                           |
|                        |  AWS         | Cloud hosting platforms                                                                |
| **Version Control**     | Git                        | Version control                                                                        |
|                        | GitHub                     | Repository hosting, issue tracking, and collaboration                                   |

## Project Risks
1. Data Quality Risk:
The performance of NLP models like Sentence-BERT is heavily dependent on the quality and consistency of training and testing data. Inaccurate, incomplete, or biased data can lead to unreliable candidate rankings.

2. Model Drift Risk:
Over time, as job requirements and resume formats evolve, the model’s accuracy may degrade unless it is regularly retrained with updated datasets.

3. Security and Privacy Risk:
Resumes often contain sensitive personal information. Inadequate encryption or poor access control could expose candidate data to unauthorized users.

4. Scalability Risk:
The system may face processing delays or failures when handling large volumes of resumes simultaneously if server resources or APIs are not optimized.

5. User Adoption Risk:
HR personnel may hesitate to adopt the AI system due to lack of trust or understanding of its recommendations, highlighting the need for model transparency and explainability.

## Project Status
1. Conception Phase - Done
2. Development Phase - Done
3. Finalization Phase - Under Progress
