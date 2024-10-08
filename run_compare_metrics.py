from pathlib import Path
import papermill as pm
import geopandas as gpd
from tqdm import tqdm

# List of parameter combinations
TEMPDIR = Path('/u/aurora-r0/cabrera/opera_dist/testing')
OUT_DIR = TEMPDIR / 'out_comparison'
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR, OUT_DIR.exists()

# input nb
inputnb = TEMPDIR / '2_Compare_Metrics.ipynb'

event_table = TEMPDIR / 'dist_s1_events.geojson'
df_events = gpd.read_file(event_table)
event_names = df_events.event_name.tolist()

metric_indices = [0, 1, 2, 3, 4, 5, 6]
metric_names = [
    "cusum_prob_max",
    "cusum_vh",
    "log_ratio_vh",
    "mahalanobis_1d_max",
    "mahalanobis_2d",
    "mahalanobis_vh",
    "transformer"
    ]

# Calculate total number of runs
total_runs = sum(
    len(list(range(df_events[df_events['event_name'] == event_name]['n_tracks'].iloc[0]))) * len(metric_indices)
    for event_name in event_names
)

# Loop over all combinations of EVENT_NAME, TRACK_IDX, and METRIC_IDX
with tqdm(total=total_runs, desc="Executing notebooks", unit="run") as pbar:
    for event_name in event_names:
        track_numbers = df_events[df_events['event_name'] == event_name]['n_tracks'].iloc[0]
        track_indices = list(range(track_numbers))
        for track_idx in track_indices:
            track_list = df_events.loc[df_events['event_name'] == event_name, 'track_numbers'].str.cat(sep=' ').split()
            for metric_idx in metric_indices:
                # output path
                JPNB_OUT_DIR = OUT_DIR / event_name 
                JPNB_OUT_DIR.mkdir(parents=True, exist_ok=True)
                # Define the output notebook file name for each run
                output_notebook = JPNB_OUT_DIR / f"2_Compare_Metrics_{event_name}_track{track_list[track_idx]}_{metric_names[metric_idx]}.ipynb"
                print(f"~~ Running {output_notebook}")
                
                # Define the parameters for the current run
                parameters = {
                    "EVENT_NAME": event_name,
                    "TRACK_IDX": track_idx,
                    "METRIC_IDX": metric_idx
                }
                
                # Execute the notebook with the specified parameters
                try:
                    pm.execute_notebook(
                        inputnb,  # Path to your notebook
                        output_notebook,         # Output notebook filename
                        parameters=parameters    # Parameters for this run
                    )
                except Exception as e:
                    print(f"Error encountered with {event_name}, track {track_idx}, metric {metric_idx}: {e}")

                # Update the progress bar
                pbar.update(1)
