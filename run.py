from pathlib import Path

import click
import geopandas as gpd
import papermill as pm
from tqdm import tqdm

df_events = gpd.read_file("dist_s1_events.geojson")
ALL_EVENTS = df_events.event_name.tolist()

DISTMETRIC_NAMES = [
    "transformer",
    "mahalanobis_2d",
    "mahalanobis_vh",
    "mahalanobis_1d_max",
    "log_ratio_vh",
]


@click.option(
    "--event",
    required=True,
    type=str,
    help=(
        "Provide names of events; multiple events put in quotes separted by a space. Possible events are"
        f"{', '.join(ALL_EVENTS)}"
    ),
)
@click.option(
    "--distmetric_name",
    required=False,
    type=str,
    default="transformer",
    help=(
        "Provide names of distmetrics to use; for multiple metrics put in quotes separated by space. Possible metrics "
        f"are {', '.join(DISTMETRIC_NAMES)}"
    ),
)
@click.command()
def main(event: str, distmetric_name: str):
    events = [e.strip() for e in event.split(" ")]
    if "all_fire" in event:
        events = df_events[df_events.event_type == "fire"].event_name.tolist()
    else:
        malformed_events = [e for e in events if e not in ALL_EVENTS]
        if malformed_events:
            raise ValueError(f'At least one of the event strings is mal-formed: {",".join(malformed_events)}'
                             'Each event must be in one of the possible events.')

    distmetric_names = [d.strip() for d in distmetric_name.split(" ")]
    malformed_distmetrics = [d for d in distmetric_names if d not in DISTMETRIC_NAMES]
    if malformed_distmetrics:
        raise ValueError(f'Some of distmetric names are incorrect: {", ".join(malformed_distmetrics)}. \n'
                         f'Please use one of the following names {DISTMETRIC_NAMES}.'
                         )


    print(f'Will run on the following {len(events)} sites:\n {"\n".join(events)}')

    in_nbs = [
        "1_Generating_Metrics.ipynb",
    ]

    ipynb_out_dir = Path("out_notebooks")
    ipynb_out_dir.mkdir(exist_ok=True, parents=True)

    for event_name in tqdm(events, desc="events"):
        print(event_name)
        for distmetric_name in distmetric_names:
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
