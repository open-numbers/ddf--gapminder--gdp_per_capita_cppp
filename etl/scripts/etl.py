# coding: utf-8

import os

import pandas as pd

from ddf_utils.model.package import Datapackage

source = '../source/gdp_per_capita_cppp--by--geo--year--pivoted_datapoints.csv'
try:
    datasets_dir = os.environ['DATASETS_DIR']
except KeyError:
    datasets_dir = '../../../'
out_dir = '../../'

data = pd.read_csv(source, encoding='latin1')


geo_domain = Datapackage(os.path.join(datasets_dir, 'open-numbers/ddf--gapminder--geo_entity_domain'))
country = geo_domain.load().get_entity('country')

data = data.set_index('geo')
data = data.stack().reset_index()

cname = 'GDP per capita, constant PPP'
cid = 'gdp_per_capita_cppp'

data.columns = ['geo', 'time', cid]

geo_upper = data.geo.unique()

mapping = {}

for g in geo_upper:
    m0 = country['name'] == g
    m1 = country['gapminder_list'] == g

    m = m0 | m1
    filtered = country[m]
    if len(filtered) > 0:
        mapping[g] = filtered['country'].values[0]
    else:
        print('not found: ', g)


data.geo = data.geo.map(lambda x: mapping[x])


data.to_csv(os.path.join(out_dir,
                         'ddf--datapoints--{}--by--geo--time.csv'.format(cid)),
            index=False, float_format='%.15g')


concepts = ['Name', 'Time', cname, 'Domain', 'Country', 'Indicator URL']
ids = ['name', 'time', cid, 'domain', 'geo', 'indicator_url']

cdf = pd.DataFrame({'concept': ids, 'name': concepts})

cdf['concept_type'] = 'string'


cdf.loc[1, 'concept_type'] = 'time'
cdf.loc[2, 'concept_type'] = 'measure'
cdf.loc[4, 'concept_type'] = 'entity_domain'
cdf.loc[2, 'indicator_url'] = 'https://github.com/open-numbers/ddf--gapminder--gdp_per_capita_cppp'

cdf.to_csv(os.path.join(out_dir, 'ddf--concepts.csv'), index=False)

geo_df = pd.DataFrame.from_records(mapping, index=[0])

geo_df = geo_df.T

geo_df = geo_df.reset_index()

geo_df.columns = ['name', 'geo']

geo_df.to_csv(os.path.join(out_dir, 'ddf--entities--geo.csv'), index=False)
