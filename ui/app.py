import gradio as gr
import matplotlib.pyplot as plt
from main import run_simulation


def launch_ui():
    def run(file, raid_type):
        metrics, sizes, times, csv = run_simulation(file.name, raid_type)

        fig, ax = plt.subplots()
        ax.plot(sizes, times, marker="o")
        ax.set_xlabel("File Size (Records)")
        ax.set_ylabel("Recovery Time (seconds)")
        ax.set_title("Recovery Time vs File Size")

        return metrics, fig, csv

    with gr.Blocks(title="RAID Log Analyzer") as demo:
        file_input = gr.File(type="filepath")
        raid = gr.Radio(["RAID1", "RAID5", "RAID6"], value="RAID5")
        run_btn = gr.Button("Run")

        out_json = gr.JSON()
        out_plot = gr.Plot()
        out_csv = gr.File()

        run_btn.click(run, [file_input, raid], [out_json, out_plot, out_csv])

    demo.launch(share=True)
