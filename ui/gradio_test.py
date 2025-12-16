import gradio as gr
import pandas as pd

# --- Test function that returns static data ---
def test_plot():
    # Static data for testing
    data = {
        "x": [10, 20, 30, 40, 50],      # File size (records)
        "y": [0.5, 0.8, 1.2, 1.8, 2.5] # Recovery time (seconds)
    }
    df = pd.DataFrame(data)
    return df

# --- Gradio App ---
with gr.Blocks() as app:
    gr.Markdown("# LinePlot Test - Static Data")

    line_plot = gr.LinePlot(
        label="Recovery Time vs File Size",
        x="x",
        y="y",
        x_title="File Size (records)",
        y_title="Recovery Time (s)"
    )

    # Static button to display plot
    test_btn = gr.Button("Show Plot")
    test_btn.click(fn=test_plot, inputs=[], outputs=line_plot)

app.launch()
