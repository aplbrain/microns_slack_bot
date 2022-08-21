import numpy as np
import pandas as pd
from caveclient import CAVEclient
from joblib import Parallel, delayed
from neuvue_queue_task_assignment.neuvue_constants import (BOX_PATH_TASKGEN,
                                                           EXTENSION_NAMESPACE,
                                                           NEUVUE_QUEUE_URL)
from neuvueclient import NeuvueQueue
from tqdm.auto import tqdm

# https://github.com/aplbrain/MICrONS_minnie65_task_assignment_scripts/blob/extension-analysis/notebooks/extension_analysis.ipynb

cave = CAVEclient("minnie65_phase3_v1")
neuvue = NeuvueQueue(NEUVUE_QUEUE_URL)


merge_num = None
total_synapse_num = None

#########################################
#           Number of Edits             #
#########################################


def get_tasks_for_extension_namespace(namespace):
    tasks = neuvue.get_tasks(sieve={
        'namespace': namespace,
        'status': 'closed'
    }, select=['metadata'])
    return tasks


def get_operation_ids_from_tasks(task_df):
    operation_ids = []
    for metadata in tqdm(task_df['metadata']):
        operation_ids += metadata.get('operation_ids', [])
    return np.unique(np.array(operation_ids))


def get_operation_details(operation_ids):
    operation_details = {}
    for i in tqdm(range(0, len(operation_ids), 500)):
        end = min(len(operation_ids), i+500)

        od = cave.chunkedgraph.get_operation_details(
            operation_ids[i: end]
        )

        operation_details.update(od)
    return operation_details


def update_ext_analysis():
    global merge_num
    global total_synapse_num

    print("Getting tasks for ext namespace...")
    task_dfs = pd.concat([get_tasks_for_extension_namespace(x)
                         for x in EXTENSION_NAMESPACE])

    print("Getting operation IDs from tasks...")
    op_ids = get_operation_ids_from_tasks(task_dfs)

    print("Getting operation data...")
    operation_details = get_operation_details(op_ids)

    # splits = {k: v for k, v in operation_details.items()
    #           if v.get('removed_edges')}
    merges = {k: v for k, v in operation_details.items()
              if v.get('added_edges')}

    merge_num = len(merges)
    print(f"Number of extensions (merges) made: {merge_num}")

    #########################################
    #     Number of Synapses Modified       #
    #########################################

    starting_ids = [x['starting_seg_id'] for x in task_dfs.metadata]

    print("Getting latest roots...")
    latest_ids = Parallel(n_jobs=20)(
        delayed(cave.chunkedgraph.get_latest_roots)(x) for x in tqdm(starting_ids))
    id_map = dict(zip(starting_ids, list(map(list, latest_ids))))

    #########################################
    #     Synapse Counts for Start IDs      #
    #########################################

    counts = pd.read_csv(BOX_PATH_TASKGEN + '/v396_top_orphans.csv')

    start_counts = counts[counts['post_pt_root_id'].astype(
        str).isin(starting_ids)].copy()
    total_synapse_num = start_counts['count'].sum()
    print(f"Total synapses reassigned : {start_counts['count'].sum()}")


if __name__ == "__main__":
    update_ext_analysis()
