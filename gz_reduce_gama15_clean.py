from matplotlib import pyplot as plt
from gz_reduce import (reduce_data, parse_tree, collate_classifications,
                       recalculate_odd_total, calculate_fractions,
                       count_matches)
from astropy.table import Table, join
import numpy as np
from numpy import ma


def evaluate_data(indata, outdata, stub):
    data = join(indata, outdata,
                keys='subject_id', join_type='left')
    evaluation = data[['subject_id', 'user', 'weight']]
    evaluation['consistency'] = 0.0
    evaluation['agreement'] = 0.0
    nanswered = np.zeros(len(data), np.int)
    qindex = 0
    for c in indata.columns:
        if c.startswith(stub):
            q = questions[qindex]
            if ('discuss' in q) or ('odd' in q):
                qindex += 1
                continue
            consistency = np.zeros(len(data))
            crossentropy = np.zeros(len(data))
            answered = np.zeros(len(data), np.bool)
            for aindex, (a, qtype) in enumerate(answers[qindex]):
                test = '{}-{}'.format(qtype, aindex)
                match = count_matches(data[c], test,
                                      anywhere=(qtype == 'x'))
                answered |= match
                name = '{}_{}'.format(q, a)
                tname = '{}_total'.format(q)
                total = data[tname]
                fname = '{}_frac'.format(name)
                p = data[fname]
                consistencyi = np.where(match, p, 1 - p)
                total = total.clip(min=1)
                minprob = 0.1 / total
                p = p.clip(min=minprob)  # bound the minimum probability
                crossentropyi = -np.where(match, 1, 0) * np.log(p)
                consistency += consistencyi
                crossentropy += crossentropyi
            nqanswers = len(answers[qindex])
            consistency /= nqanswers
            agreement = (1 - crossentropy) / np.log(nqanswers)
            # ignore and mask questions that are not answered
            consistency[~answered] = 0
            agreement[~answered] = 0
            name = '{}_consistency'.format(q)
            evaluation[name] = consistency
            evaluation['consistency'] += evaluation[name]
            evaluation[name].mask = ~answered
            name = '{}_agreement'.format(q)
            evaluation[name] = agreement
            evaluation['agreement'] += evaluation[name]
            evaluation[name].mask = ~answered
            nanswered += np.where(answered, 1, 0)
            qindex += 1
    evaluation['nanswered'] = nanswered
    evaluation['consistency'] /= nanswered
    evaluation['agreement'] /= nanswered
    evaluation = evaluation.group_by('user')
    evaluation_user = evaluation.groups.aggregate(ma.mean)
    #evaluation['count'] = 1
    user_count = evaluation['user', 'weight'].groups.aggregate(ma.sum)
    evaluation_user['count'] = user_count['weight']
    evaluation_user.sort('consistency')
    return evaluation, evaluation_user


def stripnan(x):
    return x[~np.isnan(x)]


def evaluation_plots(eval):

    fig, axarr = plt.subplots(3, 2, figsize=(10, 12))
    axarr = axarr.flat

    ax = axarr[0]
    for q in questions:
        name = '{}_consistency'.format(q)
        if name in eval.colnames:
            ax.hist(stripnan(eval[name]), label=q, histtype='step', log=True,
                    range=(0, 1), bins=25)
    ax.hist(eval['consistency'], label='total', histtype='step',
            color='k', lw=3, log=True,
            range=(0, 1), bins=25)
    ax.set_xlabel('consistency')
    ax.vlines(0.75, 0.1, 3000, linestyles='dotted')
    ax.set_xlim(0.0, 1.0)
    ax.legend(fontsize='xx-small')

    ax = axarr[1]
    for q in questions:
        name = '{}_agreement'.format(q)
        if name in eval.colnames:
            ax.hist(stripnan(eval[name]), label=q, histtype='step', log=True,
                    range=(-6, 3), bins=25)
    ax.hist(eval['agreement'], label='total', histtype='step',
            color='k', lw=3, log=True,
            range=(-6, 3), bins=25)
    ax.set_xlabel('agreement')
    ax.vlines(0.0, 0.1, 3000, linestyles='dotted')
    ax.set_xlim(-6, 3)
    ax.legend(fontsize='xx-small')

    ax = axarr[2]
    ax.scatter(eval['consistency'], eval['agreement'], marker='.',
               alpha=0.5, edgecolor='none', c=np.log10(eval['count']),
               vmin=-1, vmax=5)
    ax.set_xlim(0.4, 0.9)
    ax.set_ylim(-1, 1)
    ax.set_xlabel('consistency')
    ax.set_ylabel('agreement')

    ax = axarr[3]
    ax.hist(np.log10(eval['count']))
    ax.set_xlim(-1, 5)
    ax.set_xlabel('$\log_{10}(count)$')

    ax = axarr[4]
    ax.scatter(np.log10(eval['count']), eval['consistency'], marker='.',
               alpha=0.5, edgecolor='none', c=np.log10(eval['count']),
               vmin=-1, vmax=5)
    ax.hlines(0.75, -0.25, 4.5)
    ax.set_xlim(-1, 5)
    ax.set_ylim(0.4, 0.9)
    ax.set_xlabel('$\log_{10}(count)$')
    ax.set_ylabel('consistency')

    ax = axarr[5]
    ax.scatter(np.log10(eval['count']), eval['agreement'], marker='.',
               alpha=0.5, edgecolor='none', c=np.log10(eval['count']),
               vmin=-1, vmax=5)
    ax.hlines(0, -0.25, 4.5)
    ax.set_xlim(-1, 5)
    ax.set_ylim(-1, 1)
    ax.set_xlabel('$\log_{10}(count)$')
    ax.set_ylabel('agreement')

    #ax.set_axis_off()
    plt.tight_layout()


date = '2018-02-04'
tree = 'gama'
subjectset = 'gama15'
survey_id_field = 'provided_image_id'

questions, answers = parse_tree(tree)
template = '{}_galaxy_zoo_{}_classifications.csv'
indata = Table.read(template.format(date, subjectset), fast_reader=False)

indata['weight'] = np.ones(len(indata))

outdata = collate_classifications(indata, tree, questions, answers)
outdata = recalculate_odd_total(outdata)
outdata = calculate_fractions(outdata, questions, answers)

evaluation, evaluation_user = evaluate_data(indata, outdata, tree)
evaluation_user_avg = evaluation_user.groups.aggregate(np.nanmean)

outshuffle = outdata.copy()
perm = np.random.permutation(len(outdata))
outshuffle['subject_id'] = outshuffle['subject_id'][perm]
evalshuffle, evalshuffle_user = evaluate_data(indata, outshuffle, tree)
evalshuffle_user_avg = evalshuffle_user.groups.aggregate(np.nanmean)

evaluation_plots(evaluation_user)
plt.savefig('{}_evaluation_stage1.pdf'.format(subjectset))
plt.close()

evaluation_plots(evalshuffle_user)
plt.savefig('{}_evalshuffle_stage1.pdf'.format(subjectset))
plt.close()


def iterate_weights(stage, indata, outdata, evaluation_user):
    # set weights, add to data table, iterate...
    evaluation_user['weight'] = ((evaluation_user['consistency'] /
                                  0.75)**10).clip(max=1)

    plot_consistency = np.linspace(0.0, 1.0, 1000)
    plot_weights = ((plot_consistency / 0.75)**10).clip(max=1)
    plt.plot(plot_consistency, plot_weights)

    user_weight = Table(evaluation_user['user', 'weight'], masked=False)
    indata.remove_column('weight')
    indata = join(indata, user_weight, join_type='left', keys='user')

    outdata = collate_classifications(indata, tree, questions, answers)
    outdata = recalculate_odd_total(outdata)
    outdata = calculate_fractions(outdata, questions, answers)

    evaluation, evaluation_user = evaluate_data(indata, outdata, tree)
    evaluation_user_avg = evaluation_user.groups.aggregate(np.nanmean)

    outshuffle = outdata.copy()
    perm = np.random.permutation(len(outdata))
    outshuffle['subject_id'] = outshuffle['subject_id'][perm]
    evalshuffle, evalshuffle_user = evaluate_data(indata, outshuffle, tree)
    evalshuffle_user_avg = evalshuffle_user.groups.aggregate(np.nanmean)

    evaluation_plots(evaluation_user)
    plt.savefig('{}_evaluation_stage{}.pdf'.format(subjectset, stage))
    plt.close()

    evaluation_plots(evalshuffle_user)
    plt.savefig('{}_evalshuffle_stage{}.pdf'.format(subjectset, stage))
    plt.close()
    return (indata, outdata,
            evaluation, evaluation_user, evaluation_user_avg,
            evalshuffle, evalshuffle_user, evalshuffle_user_avg)

for i in range(4):
    (indata, outdata,
     evaluation, evaluation_user, evaluation_user_avg,
     evalshuffle, evalshuffle_user, evalshuffle_user_avg) = iterate_weights(i+2, indata, outdata, evaluation_user)

outdata.write('galaxy_zoo_{}_{}_consistency_clean.fits'.format(subjectset, date), overwrite=True)
