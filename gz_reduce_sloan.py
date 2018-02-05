from gz_reduce import reduce_data, parse_tree
from astropy.table import Table, join, vstack
from glob import glob

date='2017-12-10'
tree='sloan'
subjectset='sloan'
survey_id_field='sdss_id'

# For some reason the usual method crashes due to the large file size
# We therefore first split the file first
os.system('mkdir sloan_tmp && cd sloan_tmp && split -l1000000 -a1 ../2017-12-10_galaxy_zoo_sloan_classifications.csv gz_sloan_')

questions, answers = parse_tree(tree)
template = 'sloan_tmp/gz_sloan_*'
files = glob(template)
f = files.pop(0)
indata = Table.read(f, format='csv', fast_reader=False)
for f in files:
    nextdata = Table.read(f, format='ascii', delimiter=',', names=indata.colnames, fast_reader=False)
    indata = vstack((indata, nextdata))
os.system('rm -rf sloan_tmp')
outdata = collate_classifications(indata, tree, questions, answers)
outdata = recalculate_odd_total(outdata)
outdata = calculate_fractions(outdata, questions, answers)
subjects = read_subjects(subjectcat, subjectstub, survey_id_field)
outdata = join(outdata, subjects, 'subject_id')

outdata.write('galaxy_zoo_{}_{}.fits'.format(subjectset, date), overwrite=True)
