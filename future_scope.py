from graphviz import Digraph

# Create Digraph
dot = Digraph(comment="Future Scope of TalentSift AI")

# A4 landscape, high DPI
dot.attr(size="11.7,8.3")  # exact A4 width x height in inches
dot.attr(dpi="300")
dot.attr(overlap="false")
dot.attr(splines="true")
dot.attr(rankdir="LR")  # left-to-right layout for radial appearance

# Central node (core idea)
dot.node("A", "Future Scope of TalentSift AI", shape="oval", style="filled", color="skyblue", width="2.5", height="1.5")

# Main branches around center
main_nodes = {
    "B": ("Integration with ATS Platforms", "lightgreen"),
    "C": ("Advanced Bias Detection", "lightcoral"),
    "D": ("Multi-language Support", "gold"),
    "E": ("Predictive Analytics", "violet"),
    "F": ("Real-time Interview Assistance", "orange")
}

for node_id, (label, color) in main_nodes.items():
    dot.node(node_id, label, shape="box", style="rounded,filled", color=color, width="2", height="1.2")
    dot.edge("A", node_id)

# Sub-branches for each main branch
sub_nodes = {
    "B": [("B1", "Seamless Hiring Workflow"), ("B2", "API-based Integration")],
    "C": [("C1", "Detect Gender Bias"), ("C2", "Detect Racial Bias"), ("C3", "Ensure Fair Ranking")],
    "D": [("D1", "Regional Language Support"), ("D2", "Global Candidate Reach")],
    "E": [("E1", "Candidate Success Rate"), ("E2", "Attrition Prediction"), ("E3", "Skill Gap Analysis")],
    "F": [("F1", "AI-based Feedback"), ("F2", "Candidate Behavior Insights")]
}

for parent, children in sub_nodes.items():
    parent_color = main_nodes[parent][1]
    for child_id, child_label in children:
        dot.node(child_id, child_label, style="filled", color=parent_color, width="1.7", height="0.9")
        dot.edge(parent, child_id)

# Export PDF and PNG
dot.render("future_scope_mindmap_A4_full_radial", format="pdf", view=True)
dot.render("future_scope_mindmap_A4_full_radial", format="png", view=False)
