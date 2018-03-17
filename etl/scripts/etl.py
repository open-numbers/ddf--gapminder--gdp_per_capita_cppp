# coding: utf-8

import os.path as osp
import pandas as pd

source_file = '../source/gdppc_cppp/gdppc_cppp-by-gapminder.xlsx'
out_path = '../../'


def main():
    code = 'gdp_per_capita_cppp'

    # laod the about tab and extract the metadata
    about = pd.read_excel(source_file, header=None)
    # columns are 0: name, 1: description, 2: code
    about = about.dropna(subset=[2], how='all')
    about = about.set_index(2)

    # info about the indicator
    measure = about[[1]].T
    measure['code'] = code

    measure = measure.set_index('code')

    measure.index.name = 'concept'
    measure.columns.name = None

    measure['concept_type'] = 'measure'

    # creata concepts DataFrame
    concepts = about[[0]].copy()
    concepts.columns = ['description']
    concepts.index.name = 'concept'

    concepts['description'] = concepts['description'].map(lambda x: x.replace(':', ''))
    concepts['concept_type'] = 'string'

    # set geo concepts manually.
    domain = [ {'concept': 'geo', 'name': 'Geo', 'domain': None, 'concept_type': 'entity_domain'},
               {'concept': 'country', 'name': 'Country', 'domain': 'geo', 'concept_type': 'entity_set'},
               {'concept': 'world_4region', 'name': 'four regions', 'domain': 'geo', 'concept_type': 'entity_set'},
               {'concept': 'global', 'name': 'global', 'domain': 'geo', 'concept_type': 'entity_set'},
               {'concept': 'domain', 'name': 'Domain', 'concept_type': 'string'} ]

    domain = pd.DataFrame.from_records(domain)

    domain = domain.set_index('concept')

    time = pd.DataFrame.from_records([
        {'concept': 'year', 'concept_type': 'time', 'name': 'Year'}]).set_index('concept')

    cdf = pd.concat([measure, concepts, domain, time])
    cdf = cdf.reset_index()

    cdf['name'] = cdf['name'].fillna(cdf['concept'].map(lambda x: x.replace('_', ' ').title()))

    cdf.to_csv(osp.join(out_path, 'ddf--concepts.csv'), index=False)

    # country data. extract country entity and datapoints
    country_data = pd.read_excel(source_file,
                                 sheet_name='countries_and_territories')
    countries = country_data[['geo', 'geo.name']].copy()

    countries.columns = ['country', 'name']
    countries.to_csv(osp.join(out_path, 'ddf--entities--geo--country.csv'), index=False)

    country_df = country_data.set_index('geo').drop(['geo.name', 'indicator', 'indicator.name'], axis=1)
    country_df = country_df.stack().reset_index()
    country_df.columns = ['country', 'year', code]

    country_df.dropna(how='any').to_csv(
        osp.join(out_path,
                 'ddf--datapoints--{}--by--country--year.csv'.format(code)), index=False)

    # region data
    region_data = pd.read_excel(source_file,
                                sheet_name='four_regions')

    region = region_data[['geo', 'geo.name']]
    region.columns = ['world_4region', 'name']

    region.to_csv(osp.join(out_path, 'ddf--entities--geo--world_4region.csv'),
                  index=False)

    region_df = region_data.set_index('geo').drop(['geo.name', 'indicator', 'indicator.name'], axis=1)
    region_df = region_df.stack().reset_index()
    region_df.columns = ['world_4region', 'year', code]

    region_df.dropna(how='any').to_csv(
        osp.join(
            out_path,
            'ddf--datapoints--{}--by--world_4region--year.csv').format(code), index=False)

    # world data
    world_data = pd.read_excel(source_file,
                               sheet_name='world_total')

    world = world_data[['geo', 'geo.name']]
    world.columns = ['global', 'name']

    world.to_csv(osp.join(out_path, 'ddf--entities--geo--global.csv'), index=False)

    world_df = world_data.set_index('geo').drop(['geo.name', 'indicator', 'indicator.name'], axis=1)
    world_df = world_df.stack().reset_index()
    world_df.columns = ['global', 'year', code]

    world_df.dropna(how='any').to_csv(
        osp.join(out_path,
                 'ddf--datapoints--{}--by--global--year.csv').format(code), index=False)


if __name__ == '__main__':
    main()
    print('Done.')
