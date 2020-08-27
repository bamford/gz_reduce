from gz_reduce import *
from astropy.table import Table, join, vstack
from glob import glob
import os
import numpy as np

date='2017-12-10'
tree='sloan'
subjectset='sloan'
survey_id_field='sdss_id'

# For some reason the usual method crashes due to the large file size
# We therefore first split the file first
os.system('mkdir sloan_tmp && cd sloan_tmp && split -l1000000 -a1 ../2017-12-10_galaxy_zoo_sloan_classifications.csv gz_sloan_')

subjectcat='galaxy_zoo_subjects_lee.csv.gz'

questions, answers = parse_tree(tree)
template = 'sloan_tmp/gz_sloan_*'
files = glob(template)
f = files.pop(0)
print(f)
indata = Table.read(f, format='csv', fast_reader=False)
outdata = collate_classifications(indata, tree, questions, answers)
for f in files:
    print(f)
    indata = Table.read(f, format='ascii', delimiter=',', names=indata.colnames, fast_reader=False)
    nextoutdata = collate_classifications(indata, tree, questions, answers)
    outdata = vstack((outdata, nextoutdata))
outdata = outdata.group_by('subject_id')
outdata = outdata.groups.aggregate(np.sum)
outdata = recalculate_odd_total(outdata)
outdata = calculate_fractions(outdata, questions, answers)
subjects = read_subjects(subjectcat, subjectset, survey_id_field)
outdata = join(outdata, subjects, 'subject_id')

outdata.write('galaxy_zoo_{}_{}.fits'.format(subjectset, date), overwrite=True)

os.system('rm -rf sloan_tmp')
