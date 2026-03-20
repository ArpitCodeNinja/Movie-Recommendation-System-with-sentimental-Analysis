import gradio as gr
from tensorflow.keras.models import load_model
import joblib
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "model.keras")
tokenizer_path = os.path.join(BASE_DIR, "tokenizer.pkl")

print(f"Loading model from: {model_path}")
model = load_model(model_path)

print(f"Loading tokenizer from: {tokenizer_path}")
tokenizer = joblib.load(tokenizer_path)

def predictive_system(review):
    """
    Predicts the sentiment of a movie review using the loaded model.
    """
    try:
        # Preprocess the input text
        sequences = tokenizer.texts_to_sequences([review])
        padded_sequence = pad_sequences(sequences, maxlen=200)
        
        # Make prediction
        prediction = model.predict(padded_sequence)
        
        # Determine sentiment and format output with HTML for styling
        # Determine sentiment with a "Neutral" threshold range
        score = prediction[0][0]
        if score > 0.65:
            return '<span class="positive">Positive Sentiment 😊</span>'
        elif score < 0.35:
            return '<span class="negative">Negative Sentiment 😞</span>'
        else:
            return '<span class="neutral">Neutral Sentiment 😐</span>'
    except Exception as e:
        return f'<span style="color: red;">Error: {str(e)}</span>'

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&family=Space+Grotesk:wght@300;500;700&display=swap');

:root {
    --aura-1: #6d28d9;
    --aura-2: #db2777;
    --aura-3: #2563eb;
    --deep-aura: #020205;
}

.gradio-container {
    background: var(--deep-aura) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    perspective: 1200px;
    background-image: 
        radial-gradient(at 0% 0%, rgba(109, 40, 217, 0.25) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(219, 39, 119, 0.2) 0px, transparent 50%),
        radial-gradient(at 50% 50%, rgba(37, 99, 235, 0.1) 0px, transparent 70%) !important;
    background-attachment: fixed !important;
}

.input-box, .output-box {
    background: rgba(4, 4, 15, 0.85) !important;
    backdrop-filter: blur(40px) saturate(180%) !important;
    border: 3px solid transparent !important;
    border-radius: 30px !important;
    padding: 30px !important;
    transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1) !important;
    box-shadow: 0 0 50px rgba(109, 40, 217, 0.1) !important;
    background-image: linear-gradient(rgba(4, 4, 15, 0.9), rgba(4, 4, 15, 0.9)), 
                      conic-gradient(from 0deg, #ff007f, #00f2ff, #7000ff, #ff007f) !important;
    background-origin: border-box !important;
    background-clip: padding-box, border-box !important;
    animation: aura-flow 6s linear infinite !important;
}

@keyframes aura-flow {
    from { filter: hue-rotate(0deg); }
    to { filter: hue-rotate(360deg); }
}

.input-box:hover, .output-box:hover {
    transform: translateZ(60px) rotateX(4deg) rotateY(-4deg);
    box-shadow: 0 0 80px rgba(0, 242, 255, 0.3) !important;
    filter: brightness(1.2);
}

.output-box {
    min-height: 220px;
    animation-direction: reverse !important;
}

.submit-btn {
    background: linear-gradient(135deg, #ff007f, #7000ff, #00f2ff) !important;
    background-size: 200% auto !important;
    color: white !important;
    border: none !important;
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 900 !important;
    text-transform: uppercase !important;
    letter-spacing: 6px !important;
    padding: 22px !important;
    border-radius: 50px !important;
    transition: all 0.5s !important;
    animation: btn-shine 3s linear infinite !important;
    box-shadow: 0 10px 40px rgba(255, 0, 127, 0.4) !important;
}

@keyframes btn-shine {
    to { background-position: 200% center; }
}

.submit-btn:hover {
    letter-spacing: 12px !important;
    transform: scale(1.05) translateY(-5px);
    box-shadow: 0 15px 60px rgba(112, 0, 255, 0.6) !important;
}

.title-container h1 {
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 900 !important;
    font-size: 4.5rem !important;
    letter-spacing: -4px !important;
    color: white !important;
    text-shadow: 0 0 30px rgba(255, 255, 255, 0.2);
    animation: float 6s ease-in-out infinite;
    text-align: center;
}

@keyframes float {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(1deg); }
}

.positive { color: #00ff88 !important; text-shadow: 0 0 40px #00ff88; font-size: 3rem !important; font-weight: 900; }
.negative { color: #ff3333 !important; text-shadow: 0 0 40px #ff3333; font-size: 3rem !important; font-weight: 900; }
.neutral { color: #ffcc00 !important; text-shadow: 0 0 40px #ffcc00; font-size: 3rem !important; font-weight: 900; }

.footer p {
    color: rgba(255, 255, 255, 0.5) !important;
    font-size: 1.1rem;
    font-weight: 600;
    margin-top: 60px;
    letter-spacing: 2px;
    text-align: center;
}
"""

# HTML components
title_html = """
<div class="title-container" style="margin-bottom: 60px;">
    <h1>TEXT SENTIMENTAL ANALYSIS</h1>
</div>
"""

footer_html = """
<div class="footer">
    <p>Made by Arpit | Made with ❤️ for movie lovers</p>
</div>
"""

# Build the Gradio Blocks interface
with gr.Blocks(theme=gr.themes.Soft(), css=custom_css) as app:
    gr.HTML(title_html)

    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(
                label="Enter your movie review:",
                placeholder="Type your review here... e.g., 'This movie was absolutely amazing!'",
                lines=4,
                elem_classes="input-box"
            )
            submit_btn = gr.Button("Analyze Sentiment", elem_classes="submit-btn")

        with gr.Column():
            output_text = gr.HTML(
                label="Sentiment Analysis Result:",
                elem_classes="output-box"
            )

    gr.HTML(footer_html)

    # Click and submit actions
    submit_btn.click(
        fn=predictive_system,
        inputs=input_text,
        outputs=output_text
    )
    input_text.submit(
        fn=predictive_system,
        inputs=input_text,
        outputs=output_text
    )

if __name__ == "__main__":
    app.launch(share=False)
