from gz_reduce import reduce_data
from astropy.table import Table, join

date='2017-11-26'
tree='decals'
subjectset='decals_dr2'
survey_id_field='nsa_id'
outdata = reduce_data(date, tree, subjectset, survey_id_field, subjectstub=tree)
outdata.write('galaxy_zoo_{}_{}.fits'.format(subjectset, date), overwrite=True)

date='2017-11-26'
tree='decals'
subjectset='decals'
survey_id_field='provided_image_id'
outdata = reduce_data(date, tree, subjectset, survey_id_field)
outdata.write('galaxy_zoo_{}_dr1_{}.fits'.format(subjectset, date), overwrite=True)

date='2017-11-26'
tree='gama'
subjectset='gama09'
survey_id_field='provided_image_id'
outdata = reduce_data(date, tree, subjectset, survey_id_field)
outdata.write('galaxy_zoo_{}_{}.fits'.format(subjectset, date), overwrite=True)

#outdata = Table.read('reduced/galaxy_zoo_gama09_2017-07-09.fits')
outdata['survey_id'] = [int(x) for x in outdata['survey_id']]
info = Table.read('gama_info.fits')
info.rename_column('CATAID', 'survey_id')
outdata = join(outdata, info, keys='survey_id')
outdata.write('galaxy_zoo_{}_{}_extra.fits'.format(subjectset, date), overwrite=True)

date='2017-11-26'
tree='gama'
subjectset='gama12'
survey_id_field='provided_image_id'
outdata = reduce_data(date, tree, subjectset, survey_id_field)
outdata.write('galaxy_zoo_{}_{}.fits'.format(subjectset, date), overwrite=True)

date='2018-02-04'
tree='gama'
subjectset='gama15'
survey_id_field='provided_image_id'
outdata = reduce_data(date, tree, subjectset, survey_id_field)
outdata.write('galaxy_zoo_{}_{}.fits'.format(subjectset, date), overwrite=True)

date='2017-11-26'
tree='sloan'
subjectset='missing_manga'
survey_id_field='dr8objid'
outdata = reduce_data(date, tree, subjectset, survey_id_field)
outdata.write('galaxy_zoo_{}_{}.fits'.format(subjectset, date), overwrite=True)

date='2017-11-26'
tree='sloan'
subjectset='sdss_lost_set'
survey_id_field='nsa_id'
outdata = reduce_data(date, tree, subjectset, survey_id_field)
outdata.write('galaxy_zoo_{}_{}.fits'.format(subjectset, date), overwrite=True)

date='2017-11-26'
tree='sloan_singleband'
subjectset='sloan_singleband'
survey_id_field='provided_image_id'
outdata = reduce_data(date, tree, subjectset, survey_id_field)
outdata['band'] = [x[1:2] for x in outdata['survey_id']]
outdata['objid'] = [x[2:] for x in outdata['survey_id']]
outdata.write('galaxy_zoo_{}_{}.fits'.format(subjectset, date), overwrite=True)

date='2017-11-26'
tree='ukidss'
subjectset='ukidss'
survey_id_field='provided_image_id'
outdata = reduce_data(date, tree, subjectset, survey_id_field)
outdata.write('galaxy_zoo_{}_{}.fits'.format(subjectset, date), overwrite=True)

date='2017-11-26'
tree='illustris'
subjectset='illustris'
survey_id_field='provided_image_id'
outdata = reduce_data(date, tree, subjectset, survey_id_field)
outdata.write('galaxy_zoo_{}_{}.fits'.format(subjectset, date), overwrite=True)
