import gradio as gr
import matplotlib.pyplot as plt
from main import run_simulation
import tempfile
import os

def launch_ui():
    def run(file, raid_type):
        try:
            metrics, sizes, times, csv_path = run_simulation(file.name, raid_type)

            fig, ax = plt.subplots(figsize=(6,4))
            ax.plot(sizes, times, marker="o")
            ax.set_xlabel("File Size (Records)")
            ax.set_ylabel("Recovery Time (seconds)")
            ax.set_title("Recovery Time vs File Size")
            fig.tight_layout()

            return metrics, fig, csv_path
        except Exception as e:
            return {"error": str(e)}, None, None

    with gr.Blocks(title="RAID Log Analyzer") as demo:
        gr.Markdown("## Upload a log file and select RAID type")

        file_input = gr.File(type="filepath")
        raid = gr.Radio(["RAID1", "RAID5", "RAID6"], value="RAID5", label="RAID Type")
        run_btn = gr.Button("Run Simulation")

        out_json = gr.JSON(label="Metrics")
        out_plot = gr.Plot(label="Recovery Time Plot")
        out_csv = gr.File(label="Download CSV")

        run_btn.click(run, [file_input, raid], [out_json, out_plot, out_csv])

    demo.launch(share=True)
