from graphviz import Digraph

# Create Digraph
dot = Digraph(comment="Limitations in Handling Market Anomalies")

# Diagram style
dot.attr(rankdir="TB", size="10,12", fontsize="16")
dot.attr('node', shape='box', style='filled', color='mistyrose',
         fontsize="14", width="4", height="1.2", fontname="Helvetica")

# Nodes
dot.node('A', "Regulatory Changes\n• New rules\n• Policy shifts")
dot.node('B', "Extreme Volatility Events\n• Flash crashes\n• Sudden market swings")
dot.node('C', "Economic Crises\n• Recessions\n• Global financial disruptions")
dot.node('D', "Behavioral Biases\n• Herd behavior\n• Panic selling\n• Irrational exuberance")
dot.node('E', "Unpredictable Events\n• Geopolitical shocks\n• Natural disasters\n• Black swan events")

# Connect nodes vertically
dot.edge('A', 'B', arrowhead='normal', arrowsize="1.2")
dot.edge('B', 'C', arrowhead='normal', arrowsize="1.2")
dot.edge('C', 'D', arrowhead='normal', arrowsize="1.2")
dot.edge('D', 'E', arrowhead='normal', arrowsize="1.2")

# Output settings
dot.attr(dpi="300")  # High quality
dot.format = 'png'

# Save diagram
dot.render('limitations_market_anomalies_vertical', cleanup=True)

print("High-quality Limitations in Market Anomalies diagram saved as limitations_market_anomalies_vertical.png")
