import os
import sys, getopt
import logging
import pandas as pd
from dateutil.parser import parse
from dateutil.relativedelta import *


def main(argv):
    inputdir = ''
    outputdir = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["idir=", "odir="])
    except getopt.GetoptError:
        print('test.py -i <inputdir> -o <outputdir>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputdir> -o <outputdir>')
            sys.exit()
        elif opt in ("-i", "--idir"):
            inputdir = arg
        elif opt in ("-o", "--odir"):
            outputdir = arg
    print('Input dir is "', inputdir)
    print('Output dir is "', outputdir)

    df = log_table_format(inputdir)
    df = prepare_features(df)
    header = False

    if not os.path.isdir(outputdir):
        os.mkdir(outputdir)
        header = True
    df.to_csv(os.path.join(outputdir, "output.csv"), sep=';', index=False, encoding='UTF-8', mode='a', header=header)

    sys.exit(0)


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
            with open(os.path.join(log_path, file), 'r') as f:
                lines = f.read().replace('\n\n', '\n')
                lines = lines.splitlines()
                df = pd.DataFrame.from_dict(logs_to_records(lines, struct_header))
                results.append(df)

    return pd.concat(results)


def worktime(end, begin):
    p = relativedelta(parse(end), parse(begin))
    return f'0{p.hours}:0{p.minutes}:{p.seconds}'


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    df['DataLog'] = df.apply(lambda x: parse(x['Log-Date']).strftime('%Y-%m-%d'), axis=1)
    df['MeseLog'] = df.apply(lambda x: parse(x['Log-Date']).strftime('%m'), axis=1)
    df['AnnoLog'] = df.apply(lambda x: parse(x['Log-Date']).strftime('%Y'), axis=1)
    df['OraLog'] = df.apply(lambda x: parse(x['Log-Date']).strftime('%H'), axis=1)
    df['GiorniLavoro'] = df.apply(lambda x: relativedelta(parse(x['End-Time']), parse(x['Begin-Time'])).days, axis=1)
    df['OreLavoro'] = df.apply(lambda x: relativedelta(parse(x['End-Time']), parse(x['Begin-Time'])).hours, axis=1)
    df['MinutiLavoro'] = df.apply(lambda x: relativedelta(parse(x['End-Time']), parse(x['Begin-Time'])).minutes, axis=1)
    df['SecondiLavoro'] = df.apply(lambda x: relativedelta(parse(x['End-Time']), parse(x['Begin-Time'])).seconds,
                                   axis=1)
    df['DurataFoglio'] = df.apply(lambda x: worktime(x['End-Time'], x['Begin-Time']), axis=1)

    return df


if __name__ == '__main__':
    main(sys.argv[1:])