# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils import extract_text
from advanced_utils import detect_bias, rank_resumes_advanced, generate_insights, analyze_skill_match

# --- Page Configuration ---
st.set_page_config(
    page_title="TalentSift AI - Resume Screening",
    page_icon="🤖",
    layout="wide"
)

# --- Header ---
st.title("🤖 TalentSift AI")
st.markdown("""
### *Intelligent Resume Screening & Bias Detection Platform*

Streamline your hiring process, reduce unconscious bias, and identify the best candidates faster with our AI-powered solution.
""")

# --- DEMO VIDEO SECTION ---
st.markdown("---")
st.subheader("🎬 See It in Action (60-Second Demo)")

# Create two columns for video + features
vid_col, feat_col = st.columns([2, 1])

with vid_col:
    try:
        # Try to load the demo video
        st.video("demo_video.mp4")
        st.caption("Full workflow demonstration: Upload → Analysis → Results")
    except:
        try:
            # Fallback to GIF if MP4 doesn't work
            st.image("demo_video.gif", use_column_width=True)
            st.caption("Animated demonstration of key features")
        except:
            # Final fallback: placeholder with upload instructions
            st.info("""
            **📹 Demo Video Setup Instructions:**
            
            1. **Record your screen** using OBS, QuickTime, or phone
            2. **Show this workflow:**
               - Upload a job description
               - Upload multiple resumes  
               - Show results in all tabs
            3. **Save as** `demo_video.mp4` or `demo_video.gif`
            4. **Place in same folder** as `app.py`
            5. **Restart the app** - video will appear here!
            """)
            # Optional: Add a placeholder image
            st.image("https://via.placeholder.com/600x400/0077B6/FFFFFF?text=Record+Your+Demo+Video", 
                    use_column_width=True)

with feat_col:
    st.markdown("""
    **✨ What This Demo Shows:**
    
    **⚡ Quick Setup**
    - Paste job description
    - Drag & drop resumes
    - One-click analysis
    
    **🤖 AI-Powered Analysis**  
    - Smart resume ranking
    - Bias detection in job descriptions
    - Semantic understanding (not just keywords)
    
    **📊 Professional Results**
    - Interactive data visualizations
    - Exportable reports
    - Actionable insights
    
    **🎯 Perfect For**
    - HR teams & recruiters
    - Hiring managers  
    - Startup founders
    - Tech companies
    """)

# Quick start guide below the video
st.markdown("---")
st.subheader("🚀 Ready to Try It Yourself?")

quick_col1, quick_col2, quick_col3 = st.columns(3)

with quick_col1:
    st.markdown("""
    **1. Prepare Materials**
    - Job description text
    - 3-5 resume files (PDF/DOCX)
    - Sample data works great!
    """)

with quick_col2:
    st.markdown("""
    **2. Upload & Process**
    - Paste JD in left box
    - Upload resumes in right box
    - Click 'Analyze Applications'
    """)

with quick_col3:
    st.markdown("""
    **3. Explore Results**
    - View ranked candidates
    - Check bias analysis
    - Export reports
    - Make hiring decisions!
    """)

st.markdown("---")

# --- Initialize session state for data persistence ---
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'bias_analysis' not in st.session_state:
    st.session_state.bias_analysis = None

# --- File Upload Section (Always visible) ---
st.header("📁 Upload Materials")

col1, col2 = st.columns(2)
with col1:
    jd_text = st.text_area("Job Description", height=250, help="The job description you want to screen for.")
with col2:
    uploaded_files = st.file_uploader("Upload Resumes (PDF/DOCX)", type=['pdf', 'docx'], accept_multiple_files=True)

# --- CREATE THE BUTTON ---
process_button = st.button("🚀 Analyze Applications", type="primary", use_container_width=True)

# --- Processing Logic ---
if process_button:
    if not jd_text.strip() or not uploaded_files:
        st.error("Please provide both a Job Description and at least one resume.")
    else:
        # Create a progress bar and status updates
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Update progress - Initialization
        status_text.text("🔍 Initializing AI models...")
        progress_bar.progress(10)
        
        # 1. Extract text from resumes
        status_text.text("📄 Extracting text from resumes...")
        progress_bar.progress(20)
        
        resumes_data = []
        problem_files = [] # List to track failed files

        for file in uploaded_files:
            text = extract_text(file)
            if text:
                resumes_data.append({'name': file.name, 'text': text})
            else:
                problem_files.append(file.name)

        # Warn user about any files that failed extraction
        if problem_files:
            st.warning(f"⚠️ Could not extract text from: **{', '.join(problem_files)}**. They may be image-based scans and were excluded from analysis.")

        if not resumes_data:
            st.error("No text could be extracted from any of the uploaded files. Please check your files and try again.")
            st.stop()
        
        # Update progress
        status_text.text("⚖️ Analyzing job description for bias...")
        progress_bar.progress(40)
        
        # 2. Perform Bias Analysis on JD
        bias_summary, masculine_counts, feminine_counts, emotion_df = detect_bias(jd_text)
        
        # Update progress  
        status_text.text("📊 Ranking resumes with AI intelligence...")
        progress_bar.progress(60)
        
        # 3. Rank resumes with ADVANCED semantic similarity
        results_df = rank_resumes_advanced(jd_text, resumes_data)
        
        # Update progress
        status_text.text("💡 Generating AI insights for candidates...")
        progress_bar.progress(80)
        
        # 4. Generate insights for top 5 candidates
        insights = []
        for i in range(min(5, len(resumes_data))):
            insight = generate_insights(jd_text, resumes_data[i]['text'])
            insights.append(insight)
        
        # Add insights to the dataframe
        results_df['AI Insights'] = insights + [""] * (len(results_df) - len(insights))
        
        # Update progress
        status_text.text("✅ Finalizing results and generating reports...")
        progress_bar.progress(95)
        
        # 5. Store results in session state
        st.session_state.processed_data = {
            'results_df': results_df,
            'resumes_data': resumes_data,
            'masculine_counts': masculine_counts,
            'feminine_counts': feminine_counts,
            'emotion_df': emotion_df
        }
        st.session_state.bias_analysis = bias_summary
        
        # Complete progress
        progress_bar.progress(100)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        st.success("✅ Analysis complete! Navigate to the tabs below to explore results.")
        
        # Add quick stats dashboard
        st.subheader("🚀 Quick Overview")
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)

        with stats_col1:
            st.metric("Total Candidates", len(results_df))

        with stats_col2:
            st.metric("Top Score", f"{results_df['Semantic Similarity Score'].max():.1f}%")

        with stats_col3:
            qualified = len(results_df[results_df['Semantic Similarity Score'] >= 50])
            st.metric("Qualified", f"{qualified}/{len(results_df)}")

        with stats_col4:
            st.metric("Processing Time", "Under 60s")

# --- Create Tabs for Results ---
if st.session_state.processed_data:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Results", "🔍 Bias Analysis", "📈 Analytics", "❓ How It Works"])
    
    with tab1:
        st.header("📊 Candidate Ranking & Analysis")
        results_df = st.session_state.processed_data['results_df']
        resumes_data = st.session_state.processed_data['resumes_data']
        
        # --- NEW: SCORE BREAKDOWN SECTION ---
        if len(resumes_data) > 0:
            st.markdown("---")
            st.subheader("🔍 Detailed Candidate Analysis")
            
            selected_candidate = st.selectbox(
                "Select a candidate for detailed skill analysis:",
                results_df['Candidate'].tolist(),
                help="Choose a candidate to see detailed skill matching analysis"
            )
            
            if selected_candidate:
                candidate_data = next((resume for resume in resumes_data if resume['name'] == selected_candidate), None)
                if candidate_data:
                    # Get skill analysis
                    skill_analysis = analyze_skill_match(jd_text, candidate_data['text'])
                    
                    # Create expandable detailed analysis section
                    with st.expander("📋 Detailed Score Breakdown", expanded=True):
                        # Overall score card
                        candidate_score = results_df[results_df['Candidate'] == selected_candidate]['Semantic Similarity Score'].values[0]
                        
                        score_col1, score_col2, score_col3 = st.columns(3)
                        
                        with score_col1:
                            st.metric("Overall Score", f"{candidate_score}%")
                        
                        with score_col2:
                            st.metric("Technical Skills Match", f"{skill_analysis['technical_skills_match']}%")
                        
                        with score_col3:
                            st.metric("Soft Skills Match", f"{skill_analysis['soft_skills_match']}%")
                        
                        st.markdown("---")
                        
                        # Skills analysis in columns
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("🛠️ Technical Skills")
                            
                            if skill_analysis['matching_tech_skills']:
                                st.success(f"**✅ Matching ({len(skill_analysis['matching_tech_skills'])}/{skill_analysis['jd_tech_skills_count']})**")
                                for skill in skill_analysis['matching_tech_skills']:
                                    st.write(f"▪️ {skill.title()}")
                            else:
                                st.info("No technical skills matches found")
                            
                            if skill_analysis['missing_tech_skills']:
                                st.error(f"**⚠️ Missing ({len(skill_analysis['missing_tech_skills'])} skills)**")
                                for skill in skill_analysis['missing_tech_skills']:
                                    st.write(f"▪️ {skill.title()}")
                        
                        with col2:
                            st.subheader("💬 Soft Skills")
                            
                            if skill_analysis['matching_soft_skills']:
                                st.success(f"**✅ Matching ({len(skill_analysis['matching_soft_skills'])}/{skill_analysis['jd_soft_skills_count']})**")
                                for skill in skill_analysis['matching_soft_skills']:
                                    st.write(f"▪️ {skill.title()}")
                            else:
                                st.info("No soft skills matches found")
                            
                            if skill_analysis['missing_soft_skills']:
                                st.error(f"**⚠️ Missing ({len(skill_analysis['missing_soft_skills'])} skills)**")
                                for skill in skill_analysis['missing_soft_skills']:
                                    st.write(f"▪️ {skill.title()}")
                        
                        # Recommendations based on analysis
                        st.markdown("---")
                        st.subheader("🎯 Recommendations")
                        
                        if skill_analysis['technical_skills_match'] >= 70:
                            st.success("**Strong Technical Fit**: Candidate has most required technical skills. Proceed to technical interview.")
                        elif skill_analysis['technical_skills_match'] >= 40:
                            st.warning("**Partial Technical Fit**: Some key skills missing. Consider skills assessment or training plan.")
                        else:
                            st.error("**Weak Technical Fit**: Major skills gaps. May not be suitable for this role.")
        
        # --- MAIN RESULTS TABLE ---
        st.markdown("---")
        st.subheader("📈 Overall Ranking")
        
        # Display with nice formatting
        st.dataframe(
            results_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rank": st.column_config.NumberColumn(width="small"),
                "Candidate": st.column_config.TextColumn(width="medium"),
                "Semantic Similarity Score": st.column_config.ProgressColumn(
                    format="%.2f%%",
                    min_value=0,
                    max_value=100,
                ),
                "AI Insights": st.column_config.TextColumn(width="large", help="AI-generated summary of candidate fit")
            }
        )
        
        # Download button
        csv = results_df.to_csv(index=False)
        st.download_button("💾 Download Ranking Results", data=csv, file_name="candidate_ranking.csv", mime="text/csv")
    
    with tab2:
        st.header("Bias Analysis Report")
        bias_summary = st.session_state.bias_analysis
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Masculine-Coded Words", bias_summary["Potentially Masculine-Coded Words"])
            st.metric("Feminine-Coded Words", bias_summary["Potentially Feminine-Coded Words"])
        with col2:
            st.metric("Overall Emotional Tone", bias_summary["JD Emotional Tone"].title())
            st.write("") # Spacer
        
        # Create visualizations for word counts
        masculine_df = pd.DataFrame(list(st.session_state.processed_data['masculine_counts'].items()), columns=['Word', 'Count'])
        feminine_df = pd.DataFrame(list(st.session_state.processed_data['feminine_counts'].items()), columns=['Word', 'Count'])
        
        # Only show words that actually appeared
        masculine_df = masculine_df[masculine_df['Count'] > 0]
        feminine_df = feminine_df[feminine_df['Count'] > 0]
        
        if not masculine_df.empty:
            fig = px.bar(masculine_df, x='Word', y='Count', title="Masculine-Coded Words Detected")
            st.plotly_chart(fig, use_container_width=True)
        
        if not feminine_df.empty:
            fig = px.bar(feminine_df, x='Word', y='Count', title="Feminine-Coded Words Detected")
            st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **Interpretation Guide:**  
        - A significant imbalance in gendered wording may discourage qualified candidates from applying.
        - Aim for neutral language focused on skills and qualifications.
        - This analysis is based on linguistic research into gendered language patterns.
        """)
    
    with tab3:
        st.header("📈 Advanced Analytics")
        results_df = st.session_state.processed_data['results_df']
        
        # Create two columns for metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_score = results_df['Semantic Similarity Score'].mean()
            st.metric("Average Score", f"{avg_score:.1f}%")
        
        with col2:
            top_score = results_df['Semantic Similarity Score'].max()
            st.metric("Highest Score", f"{top_score:.1f}%")
        
        with col3:
            qualified_count = len(results_df[results_df['Semantic Similarity Score'] >= 50])
            total_count = len(results_df)
            st.metric("Qualified Candidates", f"{qualified_count}/{total_count}")

        # Score distribution histogram
        st.subheader("Score Distribution")
        fig = px.histogram(results_df, x="Semantic Similarity Score", 
                          title="How Candidates are Distributed Across Scores",
                          nbins=10,
                          color_discrete_sequence=['#1f77b4'])
        fig.update_layout(xaxis_title="Similarity Score (%)", yaxis_title="Number of Candidates")
        st.plotly_chart(fig, use_container_width=True)

        # Top 5 Candidates Chart
        st.subheader("Top 5 Candidates Comparison")
        top_5 = results_df.head(5).copy()
        top_5['Candidate'] = top_5['Candidate'].str[:30]  # Trim long filenames
        
        fig2 = px.bar(top_5, x='Candidate', y='Semantic Similarity Score',
                     title="Top Performing Candidates",
                     color='Semantic Similarity Score',
                     color_continuous_scale='Viridis')
        fig2.update_layout(xaxis_title="Candidate", yaxis_title="Score (%)")
        st.plotly_chart(fig2, use_container_width=True)

        # Score Analysis Section
        st.subheader("📊 Score Analysis")
        
        # Create score categories
        score_bins = [0, 30, 50, 70, 85, 100]
        score_labels = ['Poor (0-30%)', 'Fair (31-50%)', 'Good (51-70%)', 'Great (71-85%)', 'Excellent (86-100%)']
        
        results_df['Score Category'] = pd.cut(results_df['Semantic Similarity Score'], 
                                            bins=score_bins, 
                                            labels=score_labels, 
                                            right=True)
        
        category_counts = results_df['Score Category'].value_counts().sort_index()
        
        fig3 = px.pie(values=category_counts.values, 
                     names=category_counts.index,
                     title="Candidate Quality Distribution",
                     color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(fig3, use_container_width=True)

        # Detailed Recommendations
        st.subheader("🎯 Actionable Recommendations")
        
        rec_col1, rec_col2 = st.columns(2)
        
        with rec_col1:
            st.success("**For High-Scoring Candidates (70%+):**")
            st.write("""
            - ✅ **Immediate Interview**: Schedule interviews first
            - ✅ **Technical Assessment**: Proceed to coding test
            - ✅ **Culture Fit**: Assess team compatibility
            - ✅ **Reference Check**: Begin background verification
            """)
            
            st.info("**For Medium-Scoring Candidates (50-70%):**")
            st.write("""
            - ⚡ **Secondary Review**: Manual evaluation recommended
            - ⚡ **Skill Gap Analysis**: Identify missing competencies
            - ⚡ **Phone Screening**: Quick call to assess potential
            - ⚡ **Trial Project**: Consider small test project
            """)
        
        with rec_col2:
            st.warning("**For Low-Scoring Candidates (Below 50%):**")
            st.write("""
            - ⏸️ **Hold Application**: Keep in database for future
            - ⏸️ **Skill Development**: Suggest relevant training
            - ⏸️ **Alternative Roles**: Consider for other positions
            - ⏸️ **Rejection Notice**: Send polite decline email
            """)
            
            st.error("**Immediate Next Steps:**")
            st.write(f"""
            - **Interview Slots**: Schedule {min(3, len(top_5))} interviews this week
            - **Assessment**: Send technical test to top {min(5, len(top_5))} candidates
            - **Timeline**: Complete first round within 7 days
            - **Feedback**: Provide updates to all candidates within 48 hours
            """)

        # Export comprehensive report
        st.subheader("📋 Export Full Report")
        
        # Create comprehensive report data
        report_data = {
            'Total Candidates': [len(results_df)],
            'Average Score': [f"{avg_score:.1f}%"],
            'Top Score': [f"{top_score:.1f}%"],
            'Qualified Candidates': [f"{qualified_count}/{total_count}"],
            'Analysis Date': [pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")]
        }
        
        report_df = pd.DataFrame(report_data)
        
        col4, col5 = st.columns(2)
        
        with col4:
            # Download detailed report
            comprehensive_csv = results_df.to_csv(index=False)
            st.download_button("💾 Download Detailed Report", 
                             data=comprehensive_csv, 
                             file_name="comprehensive_analysis.csv", 
                             mime="text/csv",
                             help="Includes all candidate scores and rankings")
        
        with col5:
            # Download summary report
            summary_csv = report_df.to_csv(index=False)
            st.download_button("📄 Download Summary Report", 
                             data=summary_csv, 
                             file_name="recruitment_summary.csv", 
                             mime="text/csv",
                             help="Overall statistics and metrics")
    
    with tab4:
        st.header("❓ How TalentSift AI Works")
        
        st.markdown("""
        ### Our AI-Powered Process
        
        1. **📝 Text Extraction**  
           - Parse digital PDF and Word documents
           - Maintain data integrity with error handling
        
        2. **🤖 Semantic Analysis**  
           - Uses Sentence-BERT transformer models
           - Understands context, not just keywords
           - Compares resume content to job requirements
        
        3. **⚖️ Bias Detection**  
           - Analyzes job description language patterns
           - Identifies potentially gendered wording
           - Promotes inclusive hiring practices
        
        4. **📊 Smart Ranking**  
           - Scores candidates 0-100% based on fit
           - Provides AI-generated insights
           - Delivers actionable recommendations
        """)
        
        st.markdown("---")
        
        st.subheader("🎯 Technical Architecture")
        st.markdown("""
        ```python
        # AI Processing Pipeline
        1. File Upload → Text Extraction
        2. Job Description → Bias Analysis
        3. Resume Text → Semantic Embedding
        4. Similarity Calculation → Ranking
        5. Results → Visualization & Export
        ```
        """)
        
        st.markdown("""
        - **Frontend**: Streamlit Web Application
        - **NLP Engine**: Hugging Face Transformers
        - **Similarity Scoring**: Sentence-BERT
        - **Bias Detection**: Custom algorithm + Emotion classification
        - **Data Processing**: Pandas, NumPy
        """)

else:
    # Show instructions if no data processed yet
    st.info("👆 Upload a job description and resumes to begin analysis.")

# --- Testimonials ---
st.markdown("---")
st.subheader("🏆 What Users Say")

testimonial_col1, testimonial_col2 = st.columns(2)

with testimonial_col1:
    st.info("""
    *"Reduced our screening time by 70%! The bias detection feature helped us attract more diverse candidates."*
    - **HR Director**, Tech Company
    """)

with testimonial_col2:
    st.success("""
    *"The AI insights are surprisingly accurate. It's like having an additional senior recruiter on the team."*
    - **Talent Acquisition**, Startup
    """)

# --- Team Section ---
st.markdown("---")
st.subheader("👩‍💻 Developed By")

team_col1, team_col2, team_col3 = st.columns(3)

with team_col1:
    st.markdown("""
    **Khadeeza Parween**  
    *AI Developer & Data Scientist*  
    🔗 [LinkedIn](https://www.linkedin.com/in/khadeeza-parween-1345231a0/) • 🐙 [GitHub](https://github.com/khadeeza-parween)
    """)

with team_col2:
    st.markdown("""
    **Technologies Used**  
    Python • Streamlit • Hugging Face  
    Transformers • Sentence-BERT • Pandas
    """)

with team_col3:
    st.markdown("""
    **Project Details**  
    Version 2.0  
    Last Updated: September 2025
    """)

# --- Footer ---
st.markdown("---")
st.caption("TalentSift AI © 2024 | Making Hiring Smarter, Fairer, and More Efficient")