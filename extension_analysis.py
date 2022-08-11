import pickle
import json

import pandas as pd
from joblib import Parallel, delayed
from tqdm.auto import tqdm
import numpy as np

from neuvueclient import NeuvueQueue
from caveclient import CAVEclient

from neuvue_queue_task_assignment.neuvue_constants import (
    BOX_PATH, BOX_PATH_TASKGEN, NEUVUE_QUEUE_URL, EXTENSION_NAMESPACE
)

# https://github.com/aplbrain/MICrONS_minnie65_task_assignment_scripts/blob/extension-analysis/notebooks/extension_analysis.ipynb

cave = CAVEclient("minnie65_phase3_v1")
neuvue = NeuvueQueue(NEUVUE_QUEUE_URL)

#########################################
#           Number of Edits             #
#########################################

def get_tasks_for_extension_namespace(namespace):
    tasks = neuvue.get_tasks(sieve={
    'namespace': 'reverseExtension',
    'status':'closed'
    }, select=['metadata'])
    return tasks

task_dfs = pd.concat([get_tasks_for_extension_namespace(x) for x in EXTENSION_NAMESPACE])

def get_operation_ids_from_tasks(task_df):
    operation_ids = []
    for metadata in task_df['metadata']:
        operation_ids += metadata.get('operation_ids', [])
    return np.unique(np.array(operation_ids))


op_ids = get_operation_ids_from_tasks(task_dfs)

def get_operation_details(operation_ids):
    operation_details = {}
    for i in tqdm(range(0, len(operation_ids), 500)):
        end = min(len(operation_ids), i+500)
        
        od = cave.chunkedgraph.get_operation_details(
            operation_ids[i: end]
        )
        
        operation_details.update( od)
    return operation_details

operation_details = get_operation_details(op_ids)

splits = {k:v for k,v in operation_details.items() if v.get('removed_edges')}
merges = {k:v for k,v in operation_details.items() if v.get('added_edges')}

print(f"Number of extensions (merges) made: {len(merges)}")

#########################################
#     Number of Synapses Modified       #
#########################################

starting_ids = [x['starting_seg_id'] for x in task_dfs.metadata]

len(starting_ids)

latest_ids = Parallel(n_jobs=20)(delayed(cave.chunkedgraph.get_latest_roots)(x) for x in tqdm(starting_ids))

id_map = dict(zip(starting_ids, list(map(list, latest_ids))))

#########################################
#     Synapse Counts for Start IDs      #
#########################################

counts = pd.read_csv(BOX_PATH_TASKGEN + '/v396_top_orphans.csv')

start_counts = counts[counts['post_pt_root_id'].astype(str).isin(starting_ids)].copy()

print(f"Total synapses reassigned : {start_counts['count'].sum()}")