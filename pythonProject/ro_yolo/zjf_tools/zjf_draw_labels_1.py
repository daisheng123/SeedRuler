'''
test, not use
'''


config = {
    "font.family":'serif',
    "font.size": 24,
    "mathtext.fontset": 'stix',
#     "font.serif": ['SimSun'],

}
rcParams.update(config)
plt.rc('font',family='Times New Roman')


def plot_labels(labels, save_dir=''):
    # plot dataset labels
    c, b = labels[:, 0], labels[:, 1:].transpose()  # classes, boxes
    nc = int(c.max() + 1)  # number of classes

    # fig, ax = plt.subplots(1, 1, figsize=(8, 8), tight_layout=True)
    # ax = ax.ravel()
    # ax[0].hist(c, bins=np.linspace(0, nc, nc + 1) - 0.5, rwidth=0.8)
    # ax[0].set_xlabel('classes')
    plt.figure(figsize=(12,12))
    plt.scatter(b[0], b[1], c=hist2d(b[0], b[1], 90), cmap='jet')
    plt.xlabel('x', fontdict={'size': 28})
    plt.ylabel('y', fontdict={'size': 28})
    # plt.scatter(b[2], b[3], c=hist2d(b[2], b[3], 90), cmap='jet')
    # plt.xlabel('Width', fontdict={'family': 'Times New Roman', 'size': 28})
    # plt.ylabel('Height', fontdict={'family': 'Times New Roman', 'size': 28})
    plt.yticks( size=28)
    plt.xticks(size=28)
    # ax[0].scatter(b[0], b[1], c=hist2d(b[0], b[1], 90), cmap='jet')
    # ax[0].set_xlabel('x')
    # ax[0].set_ylabel('y')

    # ax[1].scatter(b[2], b[3], c=hist2d(b[2], b[3], 90), cmap='jet')
    # ax[1].set_xlabel('width')
    # ax[1].set_ylabel('height')
    plt.savefig(Path(save_dir) / 'labels.png', dpi=200)
    plt.close()

    # seaborn correlogram
    try:
        import seaborn as sns
        import pandas as pd
        x = pd.DataFrame(b.transpose(), columns=['x', 'y', 'width', 'height'])
        sns.pairplot(x, corner=True, diag_kind='hist', kind='scatter', markers='o',
                     plot_kws=dict(s=3, edgecolor=None, linewidth=1, alpha=0.02),
                     diag_kws=dict(bins=50))
        plt.savefig(Path(save_dir) / 'labels_correlogram.png', dpi=200)
        plt.close()
    except Exception as e:
        pass