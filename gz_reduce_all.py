from gz_reduce import reduce_data

date='2017-06-18'
tree='decals'
subjectset='decals_dr2'
survey_id_field='nsa_id'
outdata = reduce_data(date, tree, subjectset, survey_id_field, subjectstub=tree)
outdata.write('galaxy_zoo_{}_{}.fits'.format(subjectset, date), overwrite=True)

date='2017-03-19'
tree='decals'
subjectset='decals'
survey_id_field='provided_image_id'
outdata = reduce_data(date, tree, subjectset, survey_id_field)
outdata.write('galaxy_zoo_{}_dr1_{}.fits'.format(subjectset, date), overwrite=True)

date='2017-07-09'
tree='gama'
subjectset='gama09'
survey_id_field='provided_image_id'
outdata = reduce_data(date, tree, subjectset, survey_id_field)
outdata.write('galaxy_zoo_{}_{}.fits'.format(subjectset, date), overwrite=True)

date='2017-07-09'
tree='sloan'
subjectset='missing_manga'
survey_id_field='dr8objid'
outdata = reduce_data(date, tree, subjectset, survey_id_field)
outdata.write('galaxy_zoo_{}_{}.fits'.format(subjectset, date), overwrite=True)

date='2017-06-18'
tree='sloan'
subjectset='sdss_lost_set'
survey_id_field='nsa_id'
outdata = reduce_data(date, tree, subjectset, survey_id_field)
outdata.write('galaxy_zoo_{}_{}.fits'.format(subjectset, date), overwrite=True)

date='2017-07-09'
tree='sloan_singleband'
subjectset='sloan_singleband'
survey_id_field='provided_image_id'
outdata = reduce_data(date, tree, subjectset, survey_id_field)
outdata['band'] = [x[1:2] for x in outdata['survey_id']]
outdata['objid'] = [x[2:] for x in outdata['survey_id']]
outdata.write('galaxy_zoo_{}_{}.fits'.format(subjectset, date), overwrite=True)

date='2017-07-09'
tree='ukidss'
subjectset='ukidss'
survey_id_field='provided_image_id'
outdata = reduce_data(date, tree, subjectset, survey_id_field)
outdata.write('galaxy_zoo_{}_{}.fits'.format(subjectset, date), overwrite=True)
