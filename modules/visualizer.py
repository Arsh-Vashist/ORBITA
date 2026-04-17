import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# ─── 1. Original Sentiment Chart (Dark Mode Upgraded) ───
def generate_sentiment_chart(nlp_results):
    labels = []
    scores = []
    colors = []

    for article in nlp_results["articles"]:
        labels.append(article["source"])
        scores.append(article["sentiment_score"])
        if article["sentiment_score"] >= 0.05:
            colors.append("#2ecc71")  # green
        elif article["sentiment_score"] <= -0.05:
            colors.append("#e74c3c")  # red
        else:
            colors.append("#95a5a6")  # grey

    fig = go.Figure(go.Bar(
        x=labels, y=scores, marker_color=colors,
        text=[f"{s:.2f}" for s in scores], textposition="outside"
    ))

    fig.update_layout(
        title="Sentiment Score per News Source",
        xaxis_title="News Source",
        yaxis_title="Sentiment Score (-1 to +1)",
        yaxis=dict(range=[-1, 1]),
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent for Dark Mode
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dfe6e9"),     # Light text
        height=450
    )
    return fig

# ─── 2. Original Bias Spectrum (Dark Mode Upgraded) ───
def generate_bias_spectrum(nlp_results):
    sources = []
    scores = []
    biases = []

    for article in nlp_results["articles"]:
        sources.append(article["source"])
        scores.append(article["sentiment_score"])
        biases.append(article["bias"])

    fig = go.Figure()

    # Background color zones adapted for Dark Theme
    fig.add_shape(type="rect", x0=-1, x1=-0.05, y0=-0.5, y1=0.5,
                  fillcolor="rgba(231, 76, 60, 0.15)", line_width=0)
    fig.add_shape(type="rect", x0=-0.05, x1=0.05, y0=-0.5, y1=0.5,
                  fillcolor="rgba(255, 255, 255, 0.05)", line_width=0)
    fig.add_shape(type="rect", x0=0.05, x1=1, y0=-0.5, y1=0.5,
                  fillcolor="rgba(46, 204, 113, 0.15)", line_width=0)

    fig.add_trace(go.Scatter(
        x=scores, y=[0] * len(scores),
        mode="markers+text", text=sources, textposition="top center",
        marker=dict(size=14, color=scores, colorscale="RdYlGn", cmin=-1, cmax=1, showscale=False),
        hovertext=[f"{s}<br>Score: {sc:.2f}<br>Bias: {b}" for s, sc, b in zip(sources, scores, biases)]
    ))

    fig.update_layout(
        title="Bias Spectrum — News Sources",
        xaxis=dict(range=[-1, 1], title="← Against | Neutral | Pro →"),
        yaxis=dict(visible=False),
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dfe6e9"),
        annotations=[
            dict(x=-0.5, y=0.45, text="Critical", showarrow=False, font=dict(color="#e74c3c", size=13)),
            dict(x=0, y=0.45, text="Neutral", showarrow=False, font=dict(color="#95a5a6", size=13)),
            dict(x=0.5, y=0.45, text="Supportive", showarrow=False, font=dict(color="#2ecc71", size=13))
        ]
    )
    return fig

# ─── 3. Original Entity Chart (Dark Mode Upgraded) ───
def generate_entity_chart(nlp_results):
    person_counts = {}
    org_counts = {}

    for article in nlp_results["articles"]:
        for person in article["entities"].get("PERSON", []):
            person_counts[person] = person_counts.get(person, 0) + 1
        for org in article["entities"].get("ORG", []):
            org_counts[org] = org_counts.get(org, 0) + 1

    top_persons = sorted(person_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    top_orgs = sorted(org_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    fig = go.Figure()

    if top_persons:
        fig.add_trace(go.Bar(name="People", x=[p[0] for p in top_persons], y=[p[1] for p in top_persons], marker_color="#3498db"))
    if top_orgs:
        fig.add_trace(go.Bar(name="Organizations", x=[o[0] for o in top_orgs], y=[o[1] for o in top_orgs], marker_color="#9b59b6"))

    fig.update_layout(
        title="Top Mentioned People & Organizations",
        xaxis_title="Entity", yaxis_title="Mentions",
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dfe6e9"),
        height=450
    )
    return fig

# ─── 4. Original Wordcloud (Dark Mode Upgraded) ───
def generate_wordcloud(keywords):
    if not keywords:
        text = "No Keywords Found"
    else:
        text = " ".join(keywords * 10)
        
    wc = WordCloud(width=800, height=400,
                   background_color="#1e1e2e", # Dark background
                   colormap="viridis").generate(text)

    buffer = BytesIO()
    plt.figure(figsize=(10, 5), facecolor="#1e1e2e")
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(buffer, format="png", facecolor="#1e1e2e")
    plt.close()
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    return img_base64

# ─── 5. NEW: Speedometer / Gauge Chart ───
def generate_speedometer(sentiment_score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = sentiment_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        number = {'font': {'size': 40, 'color': '#a29bfe'}},
        gauge = {
            'axis': {'range': [-1, 1], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#ffffff", 'thickness': 0.25},
            'bgcolor': "#1e1e2e",
            'borderwidth': 0,
            'steps': [
                {'range': [-1, -0.05], 'color': '#e74c3c'},
                {'range': [-0.05, 0.05], 'color': '#34495e'},
                {'range': [0.05, 1], 'color': '#2ecc71'}
            ],
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dfe6e9"),
        height=350,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    return fig

# ─── 6. NEW: Bias Radar Chart ───
def generate_radar_chart(nlp_results):
    overall = nlp_results.get("overall_sentiment", 0)
    
    emotionality = min(abs(overall) * 2.5 + 0.2, 1.0) 
    factual = max(1.0 - emotionality, 0.3)
    polarity = min(abs(overall) * 2, 1.0)
    
    categories = ['Emotional Tone', 'Factual Grounding', 'Polarity/Bias', 'Sensationalism']
    values = [emotionality, factual, polarity, emotionality * 0.8]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]], 
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(162, 155, 254, 0.4)',
        line=dict(color='#a29bfe'),
        name='Stance Dimensions'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], showticklabels=False),
            bgcolor="#1e1e2e"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dfe6e9"),
        height=350,
        margin=dict(l=40, r=40, t=30, b=30)
    )
    return fig

# ─── 7. Helper: Save Charts ───
def save_charts(nlp_results):
    generate_sentiment_chart(nlp_results).write_html("sentiment_chart.html")
    generate_bias_spectrum(nlp_results).write_html("bias_spectrum.html")
    generate_entity_chart(nlp_results).write_html("entity_chart.html")
    print("Charts saved to HTML files.")