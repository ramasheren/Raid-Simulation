import gradio as gr
from main import run_simulation
import tempfile

results = []

def run(file, raid):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        metrics, recovery_time, file_size = run_simulation(tmp_path, raid)

        results.append((file_size, recovery_time))
        points = [{"x": fs, "y": rt} for fs, rt in results]

        return metrics, points

    except Exception as e:
        return {"error": str(e)}, []

with gr.Blocks() as app:
    gr.Markdown("# RAID Log File Analyzer")

    file_input = gr.File(file_types=[".txt"], label="Upload Log File")
    raid_choice = gr.Dropdown(["RAID1", "RAID5", "RAID6"], value="RAID5", label="Select RAID Type")
    run_btn = gr.Button("Run Simulation")

    metrics_output = gr.JSON(label="Performance Metrics")
    chart_output = gr.LinePlot(label="Recovery Time vs File Size")

    run_btn.click(
        run,
        inputs=[file_input, raid_choice],
        outputs=[metrics_output, chart_output]
    )

app.launch()

