from graphviz import Digraph

# Create Digraph
dot = Digraph(comment="Conclusion & Future Vision of TradeVision AI")

# Diagram style
dot.attr(rankdir="TB", size="10,15", fontsize="16")
dot.attr('node', shape='box', style='filled', color='lightyellow',
         fontsize="14", width="4", height="1.2", fontname="Helvetica")

# Nodes
dot.node('A', "Simplified Stock Market Analysis\n• Real-time data\n• Multi-factor evaluation\n• Intuitive visualizations")
dot.node('B', "Predictive Insights\n• 30-day forecasts\n• Confidence intervals\n• Risk assessment")
dot.node('C', "User-Friendly Recommendations\n• Buy, Hold, Sell\n• Clear justification\n• Confidence scores")
dot.node('D', "Educational Value\n• Transparent explanations\n• Learning market mechanics\n• Building financial literacy")
dot.node('E', "Future Vision\n• Fundamental analysis integration\n• Sentiment analysis\n• Multi-asset coverage\n• Real-time execution\n• Personalization\n• Deep learning adaptation")

# Connect nodes vertically
dot.edge('A', 'B', arrowhead='normal', arrowsize="1.2")
dot.edge('B', 'C', arrowhead='normal', arrowsize="1.2")
dot.edge('C', 'D', arrowhead='normal', arrowsize="1.2")
dot.edge('D', 'E', arrowhead='normal', arrowsize="1.2")

# Output settings
dot.attr(dpi="300")  # High quality
dot.format = 'png'

# Save diagram
dot.render('conclusion_future_scope_diagram', cleanup=True)

print("High-quality Conclusion & Future Vision diagram saved as conclusion_future_scope_diagram.png")
