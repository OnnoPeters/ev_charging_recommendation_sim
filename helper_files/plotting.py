import matplotlib as mpl
import matplotlib.pyplot as plt
from pylab import cm

def plot_nice_line_graph(x, y, title, labels, x_axis_label, y_axis_label,  x_lim_start = None, x_lim_end = None, y_lim_start = None, y_lim_end = None):
    """
    Standardized way to make a uniform line graph in a visually appealing fashion
    """
    plt.rcParams['font.size'] = 18
    plt.rcParams['axes.linewidth'] = 2
    colors = cm.get_cmap('tab10', len(y))

    fig, ax = plt.subplots(1, 1, figsize=(10,8))

    max_y = 0
    max_x = 0
    for i in range(len(y)):
        if labels is not None:
            ax.plot(x, y[i], linewidth=2, color=colors(i), label=labels[i])
        else:
            ax.plot(x, y[i], linewidth=2, color=colors(i))
        max_y = max(max(y[i]), max_y)
        max_x = max(max(x), max_x)

    ax.xaxis.set_tick_params(which='major', size=10, width=2, direction='in', top='on')
    ax.xaxis.set_tick_params(which='minor', size=7, width=2, direction='in', top='on')
    ax.yaxis.set_tick_params(which='major', size=10, width=2, direction='in', right='on')
    ax.yaxis.set_tick_params(which='minor', size=7, width=2, direction='in', right='on')

    if x_lim_start is not None and x_lim_end is not None and y_lim_start is not None and y_lim_end is not None:
        ax.set_xlim(x_lim_start, x_lim_end)
        ax.set_ylim(y_lim_start, y_lim_end)

    find_y_locator = False
    y_locator = 1
    while not find_y_locator:
        if max_y / (y_locator * 10) < 1:
            find_y_locator = True
        else:
            y_locator *= 10

    find_x_locator = False
    x_locator = 1
    while not find_x_locator:
        if max_x / (x_locator * 10) < 1:
            find_x_locator = True
        else:
            x_locator *= 10

    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(x_locator))
    ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(x_locator / 2))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(y_locator))
    ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(y_locator/2))

    ax.set_xlabel(x_axis_label, labelpad=10, fontsize=14)
    ax.set_ylabel(y_axis_label, labelpad=10, fontsize=14)

    if labels is not None:
        ax.legend(bbox_to_anchor=(1, 1), loc=0, frameon=False, fontsize=10)

    ax.set_title(title)

    plt.savefig('results\\{}.png'.format(title), dpi=300, transparent=False, bbox_inches='tight')

    plt.show()


def plot_nice_bar_graph(x, y1, y2, title, x_axis_label, y_axis_label, y_lim_start = None, y_lim_end = None):
    """
    Standardized way to make a uniform bar graph in a visually appealing fashion
    """
    plt.rcParams['axes.linewidth'] = 2
    plt.rcParams['font.size'] = 14
    colors = cm.get_cmap('tab10', len(y1))

    fig, ax = plt.subplots(1, 1, figsize=(10,8))

    for i in range(len(y1)):
        ax.bar(x, y1,  color='b')
        ax.bar(x, y2, bottom=y1, color='r')

    ax.set_xlabel(x_axis_label, labelpad=10, fontsize=12)
    ax.set_ylabel(y_axis_label, labelpad=10, fontsize=12)

    if y_lim_start is not None and y_lim_end is not None:
        ax.set_ylim(y_lim_start, y_lim_end)

    ax.legend(bbox_to_anchor=(1, 1), loc=0, frameon=False, fontsize=12)

    ax.set_title(title)

    plt.savefig('results\\{}.png'.format(title), dpi=300, transparent=False, bbox_inches='tight')

    plt.show()

def plot_nice_heatmap(x, title):
    """
    Standardized way to make a uniform heatmap in a visually appealing fashion
    """
    plt.rcParams['font.size'] = 18
    plt.rcParams['axes.linewidth'] = 2

    fig, ax = plt.subplots(1, 1, figsize=(10, 8))

    ax.imshow(x, cmap='hot', interpolation='nearest')
    ax.set_title(title)

    plt.savefig('results\\{}.png'.format(title), dpi=300, transparent=False, bbox_inches='tight')

    plt.show()


