import plotly.express as px

def visualize_market_trends(data):
    fig = px.line(data, x='time', y='price', color='commodity')
    fig.show()
