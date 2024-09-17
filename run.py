from pathlib import Path

import click
import papermill as pm
from tqdm import tqdm
import geopandas as gpd

df_event = gpd.read_file("dist_s1_events.geojson")


@click.option(
    "--event",
    required=True,
    type=str,
    help=(
        "Provide names of events; multiple events put in quotes separted by string; the possible events are"
        f"{','.join(df_event.event_name.tolist())}"
    ),
)
@click.option(
    "--distmetric_name",
    required=False,
    type=str,
    default="transformer",
    help=(
        "Provide names of distmetrics to use"
    ),
)
@click.command()
def main(event: str, distmetric_name):
    events = events = [e.strip() for e in event.split(" ")]
    if "all_fire" in event:
        events = df_event[df_event.event_type == "fire"].event_name.tolist()


    print(f'Will run on the following {len(events)} sites:\n {"\n".join(events)}')

    in_nbs = [
        "1_Generating_Metrics.ipynb",
    ]

    ipynb_out_dir = Path("out_notebooks")
    ipynb_out_dir.mkdir(exist_ok=True, parents=True)

    for event_name in tqdm(events, desc="events"):
        print(event_name)
        out_site_nb_dir = ipynb_out_dir / event_name
        out_site_nb_dir.mkdir(exist_ok=True, parents=True)
        for in_nb in in_nbs:
            print(in_nb)
            pm.execute_notebook(
                in_nb,
                output_path=out_site_nb_dir / in_nb,
                parameters=dict(EVENT_NAME=event_name, DISTMETRIC_NAME=distmetric_name),
            )


if __name__ == "__main__":
    main()
