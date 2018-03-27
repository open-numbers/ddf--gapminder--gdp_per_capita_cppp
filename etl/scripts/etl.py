# coding: utf-8

import os.path as osp
import pandas as pd


code = 'gdppc_cppp'
measure_name = 'GDP per capita, constant PPP'

out_path = '../../'

source_file = f'../source/{code}/{code}-by-gapminder.xlsx'
mappings_file = 'https://github.com/Gapminder-Indicators/concepts/blob/master/concepts-in-gapminder-indicators.xlsx?raw=true'


def main():
    print('loading mapping file...')
    mappings = pd.read_excel(mappings_file)

    print('running etl...')
    measure_id = mappings.set_index('repo_id')['concept'].loc[code]

    # set concepts manually.
    domain = [ {'concept': 'geo', 'name': 'Geo', 'domain': None, 'concept_type': 'entity_domain'},
               {'concept': 'country', 'name': 'Country', 'domain': 'geo', 'concept_type': 'entity_set'},
               {'concept': 'world_4region', 'name': 'four regions', 'domain': 'geo', 'concept_type': 'entity_set'},
               {'concept': 'global', 'name': 'global', 'domain': 'geo', 'concept_type': 'entity_set'},
               {'concept': 'domain', 'name': 'Domain', 'concept_type': 'string'} ]

    domain = pd.DataFrame.from_records(domain)

    domain = domain.set_index('concept')

    time = pd.DataFrame.from_records([
        {'concept': 'year', 'concept_type': 'time', 'name': 'Year'}]).set_index('concept')

    strings = pd.DataFrame.from_records([
        {'concept': 'name', 'concept_type': 'string', 'name': 'Name'}]).set_index('concept')

    measure = pd.DataFrame.from_records([
        {'concept': measure_id, 'concept_type': 'measure', 'name': measure_name}]).set_index('concept')

    cdf = pd.concat([measure, strings, domain, time])
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
    country_df.columns = ['country', 'year', measure_id]

    country_df.dropna(how='any').to_csv(
        osp.join(out_path,
                 'ddf--datapoints--{}--by--country--year.csv'.format(measure_id)), index=False)

    # region data
    region_data = pd.read_excel(source_file,
                                sheet_name='four_regions')

    region = region_data[['geo', 'geo.name']]
    region.columns = ['world_4region', 'name']

    region.to_csv(osp.join(out_path, 'ddf--entities--geo--world_4region.csv'),
                  index=False)

    region_df = region_data.set_index('geo').drop(['geo.name', 'indicator', 'indicator.name'], axis=1)
    region_df = region_df.stack().reset_index()
    region_df.columns = ['world_4region', 'year', measure_id]

    region_df.dropna(how='any').to_csv(
        osp.join(
            out_path,
            'ddf--datapoints--{}--by--world_4region--year.csv').format(measure_id), index=False)

    # world data
    world_data = pd.read_excel(source_file,
                               sheet_name='world_total')

    world = world_data[['geo', 'geo.name']]
    world.columns = ['global', 'name']

    world.to_csv(osp.join(out_path, 'ddf--entities--geo--global.csv'), index=False)

    world_df = world_data.set_index('geo').drop(['geo.name', 'indicator', 'indicator.name'], axis=1)
    world_df = world_df.stack().reset_index()
    world_df.columns = ['global', 'year', measure_id]

    world_df.dropna(how='any').to_csv(
        osp.join(out_path,
                 'ddf--datapoints--{}--by--global--year.csv').format(measure_id), index=False)


if __name__ == '__main__':
    main()
    print('Done.')
