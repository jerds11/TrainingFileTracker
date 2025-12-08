import numpy as np
import os
import pandas as pd

def check_if_loaded(tracker_list, entry, file):
    if entry not in tracker_list:
        return 3

    tracker = tracker_list[entry]
    for i in tracker:
        if i[file]:
            return 1
    return 2

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
                pass

            elif entry.is_dir():

                # TODO: i need to update this lines of code ...
                with os.scandir(entry) as files:
                    for file in files:
                        value = check_if_loaded(
                            tracker_list=tracker_list,
                            entry=entry,
                            file=file
                        )

                        if value == 1:
                            pass
                        
                        elif value == 2:
                            pass

                        elif value == 3:
                            print("This folder exist but not yet on the tracker.")
                            