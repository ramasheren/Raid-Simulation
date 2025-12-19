import gradio as gr
import matplotlib.pyplot as plt
import pandas as pd
import json
from main import run_simulation

def launch_ui():
    def run(file, raid_type):
        try:
            metrics, sizes, times, csv_path, ratio = run_simulation(file.name, raid_type)
            rows = [{"Metric": k, "Value": json.dumps(v, indent=2) if isinstance(v, dict) else v} for k, v in metrics.items()]
            rows.append({"Metric": "Read/Write Ratio", "Value": ratio})
            rows.append({"Metric": "Total Records", "Value": sum(sizes)})
            rows.append({"Metric": "Average Recovery Time (s)", "Value": round(sum(times)/len(times), 3)})
            df_metrics = pd.DataFrame(rows)
            fig, ax = plt.subplots(figsize=(6,4))
            ax.plot(sizes, times, marker="o")
            ax.set_xlabel("File Size (Records)")
            ax.set_ylabel("Recovery Time (seconds)")
            ax.set_title("Recovery Time vs File Size")
            fig.tight_layout()
            return df_metrics, fig, csv_path
        except Exception as e:
            return pd.DataFrame([{"Metric": "Error", "Value": str(e)}]), None, None

    with gr.Blocks(title="RAID Log Analyzer") as demo:
        gr.Markdown("## Upload a log file and select RAID type")
        file_input = gr.File(type="filepath")
        raid = gr.Radio(["RAID1", "RAID5", "RAID6"], value="RAID5", label="RAID Type")
        run_btn = gr.Button("Run Simulation")
        out_table = gr.Dataframe(headers=["Metric", "Value"], label="Metrics Table")
        out_plot = gr.Plot(label="Recovery Time Plot")
        out_csv = gr.File(label="Download CSV")
        run_btn.click(run, [file_input, raid], [out_table, out_plot, out_csv])

    demo.launch(share=True)
