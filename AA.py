from graphviz import Digraph

# Create Digraph
dot = Digraph(comment="Future Scope of TradeVision AI")

# Diagram style
dot.attr(rankdir="TB", size="10,15", fontsize="16")
dot.attr('node', shape='box', style='filled', color='lightcyan',
         fontsize="14", width="4", height="1.2", fontname="Helvetica")

# Nodes
dot.node('A', "Fundamental Analysis Integration\n• Earnings reports\n• Balance sheets\n• Industry comparisons")
dot.node('B', "Sentiment Analysis with NLP\n• News and social media sentiment\n• Regulatory updates")
dot.node('C', "Multi-Asset Coverage\n• Commodities\n• Forex\n• Cryptocurrencies\n• Derivatives")
dot.node('D', "Real-Time Trading Integration\n• Broker API connection\n• Seamless trade execution")
dot.node('E', "Personalization\n• Risk appetite alignment\n• Portfolio customization\n• Investment goals")
dot.node('F', "Deep Learning & Adaptive Modeling\n• Reinforcement learning\n• Adaptive algorithms\n• Continuous improvement")

# Connect nodes vertically
dot.edge('A', 'B', arrowhead='normal', arrowsize="1.2")
dot.edge('B', 'C', arrowhead='normal', arrowsize="1.2")
dot.edge('C', 'D', arrowhead='normal', arrowsize="1.2")
dot.edge('D', 'E', arrowhead='normal', arrowsize="1.2")
dot.edge('E', 'F', arrowhead='normal', arrowsize="1.2")

# Output settings
dot.attr(dpi="300")  # high quality
dot.format = 'png'

# Save diagram
dot.render('future_scope_tradevision_vertical', cleanup=True)

print("High-quality Future Scope diagram saved as future_scope_tradevision_vertical.png")
