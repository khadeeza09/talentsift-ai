from graphviz import Digraph
import os

# Ensure the output directory exists
output_dir = "/mnt/data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Create mind map style diagram
app_chart = Digraph(format="png")

# Graph attributes for larger canvas and white space
app_chart.attr(
    rankdir="TB",          # Top to Bottom layout
    size="20,15",           # Bigger canvas size
    dpi="300",             # High resolution
    splines="ortho",       # Straight connectors
    nodesep="0.8",         # Space between nodes
    ranksep="1.5",         # Space between ranks
    ratio="auto",          # Auto expand to fit nodes
    margin="0.5"           # Extra margin around graph
)

# Central Node
app_chart.node(
    "A",
    "Applications of TalentSift AI",
    shape="ellipse",
    style="filled,bold",
    fillcolor="lightblue",
    fontsize="20"
)

# Application Nodes
applications = {
    "B": "Corporate Recruitment",
    "C": "University/College Placements",
    "D": "Online Job Portals",
    "E": "Government Recruitment",
    "F": "Internal Promotions",
    "G": "Diversity & Inclusion"
}

for node, label in applications.items():
    app_chart.node(
        node,
        label,
        shape="box",
        style="rounded,filled",
        fillcolor="lightgrey",
        fontsize="16"
    )
    app_chart.edge("A", node, arrowhead="vee")

# Render the diagram
app_chart_path = os.path.join(output_dir, "talentsift_applications_wide")
app_chart.render(app_chart_path, view=True)

print(f"Diagram saved at: {app_chart_path}.png")