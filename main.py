import pandas as pd
import os, sys
from dateutil.parser import parse
from dateutil.relativedelta import *


def logs_to_records(logs, struct_header):
    for l in logs:
        row = l.split(':', 1)
        struct_header[row[0]].append(row[1])

    return struct_header


def log_table_format(log_path) -> pd.DataFrame:
    struct_header = {'Log-Date': [],
                     'File-Name': [],
                     'Page-Total': [],
                     'Page-ID': [],
                     'Begin-Time': [],
                     'End-Time': [],
                     'Cut-Time': [],
                     'Objects-Total': [],
                     'Pieces-Total': [],
                     'All-Length': [],
                     'Feed-Speeed': [],
                     'SP-Length1': [],
                     'SP-Length2': [],
                     'SP-Length3': [],
                     'SP-Length4': [],
                     'SP-Length5': [],
                     'SP-Length6': [],
                     'SP-Length7': [],
                     'SP-Length8': [],
                     'SP-Length9': [],
                     'SP-Length10': [],
                     'SP-Length11': [],
                     'SP-Length12': [],
                     'SP-Length13': [],
                     'SP-Length14': [],
                     'SP-Length15': [],
                     'SP-Length16': [],
                     'SP-Length17': []}

    files = os.listdir(log_path)
    results = []

    for file in files:
        if '.log' in file:
            with open(os.path.join('resources', file), 'r') as f:
                lines = f.read().replace('\n\n', '\n')
                lines = lines.splitlines()
                df = pd.DataFrame.from_dict(logs_to_records(lines, struct_header))
                results.append(df)

    return pd.concat(results)


if __name__ == '__main__':
    df = log_table_format(os.path.join('resources'))
    sys.exit(0)
