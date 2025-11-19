from graphviz import Digraph

# Create Digraph
dot = Digraph(comment="TradeVision AI: Actionable Recommendations")

# Style settings
dot.attr(rankdir="TB", size="10,15", fontsize="16")  # Bigger diagram
dot.attr('node', shape='box', style='filled', color='lightblue2',
         fontsize="14", width="4", height="1", fontname="Helvetica")

# Nodes
dot.node('A', "1. Data Collection\n• Historical market data\n• Price trends\n• Volume\n• Technical indicators")
dot.node('B', "2. Multi-Factor Analysis\n• Technical indicators\n• Trend analysis\n• Pattern recognition")
dot.node('C', "3. Recommendation Engine\n• AI decision model\n• Signal processing")
dot.node('D', "4. Actionable Recommendations\n• Strong Buy\n• Buy\n• Hold\n• Sell\n• Strong Sell")
dot.node('E', "5. Supporting Metrics\n• Detailed metrics\n• Visual explanations")

# Edges (top-to-bottom)
dot.edge('A', 'B', arrowhead='normal', arrowsize="1.2")
dot.edge('B', 'C', arrowhead='normal', arrowsize="1.2")
dot.edge('C', 'D', arrowhead='normal', arrowsize="1.2")
dot.edge('D', 'E', arrowhead='normal', arrowsize="1.2")

# Output settings
dot.attr(dpi="300")  # High resolution
dot.format = 'png'  # Output format

# Save diagram
dot.render('actionable_recommendations_diagram_high_quality', cleanup=True)

print("High-quality vertical diagram saved as actionable_recommendations_diagram_high_quality.png")
