import gradio as gr
import matplotlib.pyplot as plt

from main import run_simulation, run_simulation_series


def run_ui(file, raid_type):
    # Single run (metrics)
    metrics, recovery_time, file_size = run_simulation(file.name, raid_type)

    # Series run (for line plot)
    sizes, times = run_simulation_series(file.name, raid_type)

    # Plot
    fig, ax = plt.subplots()
    ax.plot(sizes, times, marker="o")
    ax.set_xlabel("File Size (Records)")
    ax.set_ylabel("Recovery Time (seconds)")
    ax.set_title("Recovery Time vs File Size")

    return metrics, fig


def launch_ui():
    with gr.Blocks(title="RAID Log Analyzer") as demo:
        gr.Markdown("## Log File Analyzer & RAID Data Archiver")

        file_input = gr.File(label="Upload .txt Log File")
        raid_choice = gr.Radio(
            ["RAID1", "RAID5", "RAID6"],
            label="Select RAID Type",
            value="RAID5"
        )

        run_button = gr.Button("Run Simulation")

        metrics_output = gr.JSON(label="Performance Metrics")
        plot_output = gr.Plot(label="Recovery Time vs File Size")

        run_button.click(
            run_ui,
            inputs=[file_input, raid_choice],
            outputs=[metrics_output, plot_output]
        )

    demo.launch()
