from graphviz import Digraph

# Create a Digraph with higher DPI for better quality
dot = Digraph(comment="TalentSift AI Flowchart", format="png")
dot.attr(rankdir="TB", size="8")
dot.attr(dpi="300")   # << increase resolution (default is ~96)

# Nodes
dot.node("A", "Start\n(Upload Resume + Job Description)", shape="oval", style="filled", color="lightblue")
dot.node("B", "Preprocessing\n(Clean & extract text)", shape="box", style="filled", color="lightyellow")
dot.node("C", "NLP Model\n(Sentence-BERT embeddings)", shape="box", style="filled", color="lightpink")
dot.node("D", "Ranking Engine\n(Compare resumes with JD)", shape="box", style="filled", color="lightgreen")
dot.node("E", "Bias Detection\n(Check fairness & bias)", shape="box", style="filled", color="lightcoral")
dot.node("F", "Visualization Layer\n(Streamlit + Plotly results)", shape="box", style="filled", color="lightgrey")
dot.node("G", "Output\n(Ranked resumes + Bias report)", shape="oval", style="filled", color="lightblue")

# Edges
dot.edges(["AB", "BC", "CD", "DE", "EF", "FG"])

# Save and auto-open the flowchart in your project folder
file_path = r"C:\Users\khade\OneDrive\Desktop\AI_resume_screner\talentsift_ai_flowchart"
dot.render(file_path, view=True)
