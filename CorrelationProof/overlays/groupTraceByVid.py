import os
import re
from shutil import copyfile


def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def main():
    # get all user folders in Traces
    userfolders = [trace.path for trace in os.scandir('Experiment Data/Traces/')]
    for user in userfolders:
        user_id = user.split('Traces/')[1]
        
        # remove videos if they don't have ID (just in case)
        regex = r"_([0-9]+)\.csv"
        vid_ids = [{'filename': filename, 'id': re.findall(regex, filename)} for filename in os.listdir(user)]
        vid_ids = [item for item in vid_ids if len(item["id"]) > 0]

        for vid_id in vid_ids:
            # copy over to grouped by videos directory
            base_dir = f"CorrelationProof/overlays/GroupByVideos/{vid_id['id'][0]}"
            mkdir(base_dir)
            copyfile(f"{user}/{vid_id['filename']}", f"{base_dir}/{user_id}.csv")


if __name__ == '__main__':
    main()
