# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter, ScalarFormatter


def clip(value_before_switch, value_after_switch, t_switch, t):
    """
    logical function of time. Changes value at threshold time t_switch.

    """
    if t <= t_switch:
        return value_before_switch
    else:
        return value_after_switch


class Clipper:
    """
    Class helper. Rather than using clip(var, var1, t_switch, t), defines
    var as a function of the time: var(t).

    """

    def __init__(self, value_before_switch, value_after_switch,
                 trigger_value):
        self.value_before_switch = value_before_switch
        self.value_after_switch = value_after_switch
        self.trigger_value = trigger_value

    def __call__(self, t):
        return clip(self.value_before_switch, self.value_after_switch,
                    self.trigger_value, t)


def make_patch_spines_invisible(ax):
    """
    Helper from matplotlib gallery (Multiple Yaxis With Spines)

    """
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


def plot_world_variables(time, var_data, var_names, var_lims,
                         title=None,
                         figsize=None,
                         dist_spines=0.09,
                         grid=False):
    """
    Plots world state from an instance of World2.

    """
    var_number = len(var_data)

    fig, host = plt.subplots(figsize=figsize)
    axs = [host, ]
    for i in range(var_number-1):
        axs.append(host.twinx())

    fig.subplots_adjust(left=dist_spines*2)
    for i, ax in enumerate(axs[1:]):
        ax.spines["left"].set_position(("axes", -(i + 1)*dist_spines))
        ax.spines["left"].set_visible(True)
        ax.yaxis.set_label_position('left')
        ax.yaxis.set_ticks_position('left')

    ps = []
    for ax, label, ydata, color in zip(axs, var_names, var_data,
                                       ["black", "#e7298a", "#d95f02",
                                        "#7570b3", "#1b9e77"]):
        ps.append(ax.plot(time, ydata, label=label, color=color, linewidth=3,
                          alpha=0.7)[0])
    axs[0].grid(grid)
    axs[0].set_xlim(time[0], time[-1])

    for ax, lim in zip(axs, var_lims):
        ax.set_ylim(lim[0], lim[1])

    for ax_ in axs:
        formatter_ = EngFormatter(places=0, sep="\N{THIN SPACE}")
        ax_.tick_params(axis='y', rotation=90)
        ax_.yaxis.set_major_locator(plt.MaxNLocator(5))
        ax_.yaxis.set_major_formatter(formatter_)

    tkw = dict(size=4, width=1.5)
    axs[0].set_xlabel("time [years]")
    axs[0].tick_params(axis='x', **tkw)
    for i, (ax, p) in enumerate(zip(axs, ps)):
        ax.set_ylabel(p.get_label(), rotation="horizontal")
        ax.yaxis.label.set_color(p.get_color())
        ax.tick_params(axis='y', colors=p.get_color(), **tkw)
        ax.yaxis.set_label_coords(-i*dist_spines, 1.01)

    if title is not None:
        fig.suptitle(title, x=0.95, ha="right", fontsize=10)

    plt.tight_layout()
    return axs