import gradio as gr
import pandas as pd

def test_plot():
    data = {"x": [10, 20, 30, 40, 50], "y": [0.5, 0.8, 1.2, 1.8, 2.5]}
    return pd.DataFrame(data)

with gr.Blocks() as app:
    gr.Markdown("# LinePlot Test - Static Data")
    line_plot = gr.LinePlot(
        label="Recovery Time vs File Size",
        x="x",
        y="y",
        x_title="File Size (records)",
        y_title="Recovery Time (s)"
    )
    test_btn = gr.Button("Show Plot")
    test_btn.click(fn=test_plot, inputs=[], outputs=line_plot)

app.launch()
