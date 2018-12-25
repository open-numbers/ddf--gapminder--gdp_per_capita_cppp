# coding: utf-8

import os.path as osp
import pandas as pd

from ddf_utils.io import open_google_spreadsheet, serve_datapoint
from ddf_utils.str import to_concept_id

DOCID = '1n9ql6TebePZEDtxVd3JwBgFwqsz5JV4RzcR9GoKz0kg'
SHEET = 'data-for-countries-etc-by-year'

DIMENSIONS = ['geo', 'year']
OUT_DIR = '../../'


def gen_datapoints(df_: pd.DataFrame):
    df = df_.copy()
    df = df.set_index(DIMENSIONS).drop('name', axis=1)  # set index and drop column 'name'
    for c in df:
        yield (c, df[[c]])


def create_geo_domain(df: pd.DataFrame) -> pd.DataFrame:
    return df[['geo', 'name']].drop_duplicates()


def main():
    print('running etl...')
    data = pd.read_excel(open_google_spreadsheet(DOCID), sheet_name=SHEET)

    measures = list()

    for c, df in gen_datapoints(data):
        c_id = to_concept_id(c)
        df.columns = [c_id]
        serve_datapoint(df, OUT_DIR, c_id)

        measures.append((c_id, c))

    measures_df = pd.DataFrame(measures, columns=['concept', 'name'])
    measures_df['concept_type'] = 'measure'

    discrete_df = pd.DataFrame.from_dict(
        dict(concept=['geo', 'name', 'year'],
             name=['Geo', 'Name', 'Time'],
             concept_type=['entity_domain', 'string', 'time'])
    )
    pd.concat([measures_df, discrete_df], ignore_index=True).to_csv(osp.join(OUT_DIR, 'ddf--concepts.csv'), index=False)

    geo_df = create_geo_domain(data)
    geo_df.to_csv(osp.join(OUT_DIR, 'ddf--entities--geo.csv'), index=False)


if __name__ == '__main__':
    main()
    print('Done.')
