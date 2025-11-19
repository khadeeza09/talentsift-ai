# advanced_utils.py
import pandas as pd
import re
import numpy as np
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

# --- Initialize Models (Load once, use everywhere) ---
# Load a model for sentiment/emotion classification (for bias detection)
print("Loading Bias Detection model...")
classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

# Load a model for semantic similarity (better than TF-IDF)
print("Loading Semantic Similarity model...")
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')

# --- 1. Bias Detection Function ---
def detect_bias(job_description_text):
    """
    Analyzes a job description for potentially biased language.
    Returns a DataFrame with bias analysis.
    """
    # Keywords often associated with gendered bias
    masculine_coded_words = ["aggressive", "analytical", "assertive", "athletic", "autonomous", "battle", "boast",
                             "challenge", "competent", "confident", "courageous", "decide", "decision", "decisive"]
    
    feminine_coded_words = ["collaborative", "committed", "compassionate", "connect", "cooperative", "dependable",
                            "empathy", "enthusiasm", "interpersonal", "loyal", "nurture", "pleasant", "responsive", "sensitive"]
    
    # Check for biased keywords
    masculine_counts = {word: len(re.findall(rf"\b{word}\b", job_description_text.lower())) for word in masculine_coded_words}
    feminine_counts = {word: len(re.findall(rf"\b{word}\b", job_description_text.lower())) for word in feminine_coded_words}
    
    total_masculine = sum(masculine_counts.values())
    total_feminine = sum(feminine_counts.values())
    
    # Analyze sentiment/emotion of the JD using the model
    # We'll look for high levels of 'anger' which can correlate with aggressive/biased language
    emotion_results = classifier(job_description_text[:512]) # Truncate to model's max length
    emotion_df = pd.DataFrame(emotion_results[0])
    
    # Create a summary
    bias_summary = {
        "Potentially Masculine-Coded Words": total_masculine,
        "Potentially Feminine-Coded Words": total_feminine,
        "JD Emotional Tone": emotion_df.loc[emotion_df['score'].idxmax(), 'label']
    }
    
    return bias_summary, masculine_counts, feminine_counts, emotion_df

# --- 2. Advanced Semantic Similarity ---
def rank_resumes_advanced(job_description, resumes):
    """
    Uses Sentence Transformers for much better semantic understanding than TF-IDF.
    """
    # Encode the Job Description and all resumes
    jd_embedding = semantic_model.encode(job_description, convert_to_tensor=True)
    resume_texts = [resume['text'] for resume in resumes]
    resume_embeddings = semantic_model.encode(resume_texts, convert_to_tensor=True)
    
    # Compute cosine similarities
    cosine_scores = util.pytorch_cos_sim(jd_embedding, resume_embeddings)[0]
    
    # Create results DataFrame
    results_df = pd.DataFrame({
        'Candidate': [resume['name'] for resume in resumes],
        'Semantic Similarity Score': np.round(cosine_scores.cpu().numpy() * 100, 2)
    })
    
    # Sort and rank
    results_df = results_df.sort_values('Semantic Similarity Score', ascending=False)
    results_df['Rank'] = range(1, len(results_df) + 1)
    results_df = results_df[['Rank', 'Candidate', 'Semantic Similarity Score']]
    
    return results_df

# --- 3. Generate LLM-Powered Insights ---
def generate_insights(job_description, resume_text):
    """
    Generates a concise insight for a single resume using a smaller, faster model.
    This is a placeholder. For a real project, you would use an API or a larger local model.
    """
    # This is a simplified example. In a real scenario, you would use a proper text generation model.
    # Let's create a simple rule-based insight generator for demonstration.
    
    # Check for experience level
    experience_keywords = ["year", "years", "experience", "expérience"]
    has_experience = any(keyword in resume_text.lower() for keyword in experience_keywords)
    
    # Check for education
    education_keywords = ["bachelor", "master", "phd", "degree", "diploma", "university"]
    has_education = any(keyword in resume_text.lower() for keyword in education_keywords)
    
    # Simple insight generation
    insights = []
    if has_experience:
        insights.append("Highlights relevant professional experience.")
    if has_education:
        insights.append("Possesses the required educational background.")
    
    if insights:
        return " | ".join(insights)
    else:
        return "Potential fit based on skills alignment. Review for culture add."

# --- 4. Skill Match Analysis ---
def analyze_skill_match(job_description, resume_text):
    """
    Analyze specific skill matches between JD and resume
    Returns detailed breakdown of matching and missing skills
    """
    # Comprehensive list of technical skills
    tech_skills = [
        'python', 'java', 'javascript', 'typescript', 'sql', 'nosql', 'html', 'css', 
        'react', 'angular', 'vue', 'node', 'express', 'django', 'flask', 'spring',
        'machine learning', 'deep learning', 'nlp', 'computer vision', 'ai',
        'tensorflow', 'pytorch', 'scikit-learn', 'keras', 'opencv',
        'aws', 'azure', 'google cloud', 'gcp', 'docker', 'kubernetes', 'jenkins',
        'tableau', 'power bi', 'excel', 'spark', 'hadoop', 'kafka', 'airflow',
        'git', 'github', 'gitlab', 'ci/cd', 'rest api', 'graphql', 'microservices',
        'c++', 'c#', 'ruby', 'php', 'go', 'rust', 'swift', 'kotlin'
    ]
    
    # Comprehensive list of soft skills
    soft_skills = [
        'leadership', 'communication', 'teamwork', 'collaboration', 'problem solving',
        'project management', 'agile', 'scrum', 'kanban', 'presentation', 'public speaking',
        'critical thinking', 'analytical skills', 'time management', 'adaptability',
        'creativity', 'innovation', 'mentoring', 'training', 'conflict resolution',
        'negotiation', 'decision making', 'strategic planning', 'customer service'
    ]
    
    # Convert to lowercase for case-insensitive matching
    jd_lower = job_description.lower()
    resume_lower = resume_text.lower()
    
    # Find skills mentioned in both JD and resume
    matching_tech_skills = [skill for skill in tech_skills if skill in jd_lower and skill in resume_lower]
    matching_soft_skills = [skill for skill in soft_skills if skill in jd_lower and skill in resume_lower]
    
    # Find skills required in JD but missing in resume
    jd_tech_skills = [skill for skill in tech_skills if skill in jd_lower]
    jd_soft_skills = [skill for skill in soft_skills if skill in jd_lower]
    
    missing_tech_skills = list(set(jd_tech_skills) - set(matching_tech_skills))
    missing_soft_skills = list(set(jd_soft_skills) - set(matching_soft_skills))
    
    # Calculate match percentages
    tech_match_pct = (len(matching_tech_skills) / len(jd_tech_skills) * 100) if jd_tech_skills else 0
    soft_match_pct = (len(matching_soft_skills) / len(jd_soft_skills) * 100) if jd_soft_skills else 0
    
    return {
        'technical_skills_match': round(tech_match_pct, 1),
        'soft_skills_match': round(soft_match_pct, 1),
        'matching_tech_skills': matching_tech_skills,
        'matching_soft_skills': matching_soft_skills,
        'missing_tech_skills': missing_tech_skills,
        'missing_soft_skills': missing_soft_skills,
        'jd_tech_skills_count': len(jd_tech_skills),
        'jd_soft_skills_count': len(jd_soft_skills)
    }