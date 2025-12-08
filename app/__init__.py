from rich import print
import numpy as np
import os
import pandas as pd

def check_if_loaded(tracker, file):
    for i in tracker:
        if file in i and i[file]:
            return 1
    return 0

def process_tracker_directory(tracker_directory):
    df = pd.read_excel(tracker_directory)

    df['Field Mapping Complete'] = np.where(df['Field Mapping Complete'] == 1, True, False)

    result = (
        df.groupby("Folder", group_keys=False)
        .apply(
            lambda g: [{row["Raw Data File Name"]: row["Field Mapping Complete"]} for _, row in g.iterrows()],
            include_groups=False
        )
        .to_dict()
    )

    return result

def run(directory, tracker_directory) -> None:
    tracker_list = process_tracker_directory(tracker_directory = tracker_directory)

    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file():
                print(f"Skipping '{entry.name}' this is not a folder")

            elif entry.is_dir():
                if entry.name in tracker_list:
                    for i in os.scandir(os.path.join(directory, entry.name)):
                        value = check_if_loaded(tracker=tracker_list[entry.name], file=i.name)
                        if value == 1:
                            pass

                            # TODO: for this one i still need to further get to the details of field mapping being completed or not
                        else:
                            print(f"[bold]{entry.name}[/bold]: '{i.name}' - [red]not yet added to the tracker[/red]")
                else:
                    print(f"[bold]{entry.name}[/bold] [red]add to the tracker[/red]")
