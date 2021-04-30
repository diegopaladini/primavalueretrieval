import os
import sys, getopt
import logging, traceback
from datetime import date
import pandas as pd
from dateutil.parser import parse
from dateutil.relativedelta import *

logging.basicConfig(filename=os.path.join(os.path.dirname(__file__),'parsing.log'), filemode='a',
                    format='%(name)s - %(levelname)s - %(message)s')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)


def main(argv):
    inputdir = ''
    outputdir = ''
    df = pd.DataFrame()

    try:
        opts, args = getopt.getopt(argv, "hi:o:m:", ["idir=", "odir=", "mode="])
    except getopt.GetoptError:
        print('primavalueretrieval.py -i <inputdir> -o <outputdir> -m daily|all')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('primavalueretrieval.py -i <inputdir> -o <outputdir>')
            sys.exit()
        elif opt in ("-i", "--idir"):
            inputdir = arg
        elif opt in ("-o", "--odir"):
            outputdir = arg
        elif opt in ("-m", "--mode") and arg in ("d", "daily"):
            df = parse_single_log(inputdir)
        elif opt in ("-m", "--mode") and arg in ("a", "all"):
            df = parse_multiple_logs(inputdir)

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


def parse_log(base_path, inputfile) -> pd.DataFrame:

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

    with open(os.path.join(base_path, inputfile), 'r') as f:
        lines = f.read().replace('\n\n', '\n')
        lines = lines.splitlines()
        df = pd.DataFrame.from_dict(logs_to_records(lines, struct_header))

    return df


def parse_single_log(log_path) -> pd.DataFrame:

    results = []

    today = date.today()
    d = today.strftime("%Y-%m-%d")
    logger.info(f'parsing file {d}_log.log ...')

    try:
        results.append(parse_log(log_path, d + "_log.log"))
    except Exception as e:
        logger.error(f"Unable to parse parsing file {d}_log.log", e)

    return pd.concat(results)


def parse_multiple_logs(log_path) -> pd.DataFrame:
    files = os.listdir(log_path)

    results = []
    try:
        for file in files:
            if '.log' in file:
                logger.info(f'parsing file {file} ...')
                results.append(parse_log(log_path, file))
    except Exception as e:
        logger.error(f"Unable to parse parsing file {file}", e)

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
