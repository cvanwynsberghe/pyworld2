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


def plot_world_state(world2, title=None, dist_spines=0.09):
    """
    Plots world state from a World2 instance.

    """
    fig, host = plt.subplots(figsize=(7, 4))
    axs = [host, ]
    for i in range(4):
        axs.append(host.twinx())

    fig.subplots_adjust(left=dist_spines*2)
    for i, ax in enumerate(axs[1:]):
        ax.spines["left"].set_position(("axes", -(i + 1)*dist_spines))
        ax.spines["left"].set_visible(True)
        ax.yaxis.set_label_position('left')
        ax.yaxis.set_ticks_position('left')

    ps = []
    for ax, color, label, ydata in zip(axs,
                                       ["black", "#e7298a", "#d95f02",
                                        "#7570b3", "#1b9e77"],
                                       ["P", "POLR  ", "CI ", "QL ", "NR "],
                                       [world2.p, world2.polr, world2.ci,
                                        world2.ql, world2.nr]):

        ps.append(ax.plot(world2.time, ydata, color=color, label=label)[0])
    axs[0].grid(1)

    axs[0].set_xlim(world2.time[0], world2.time[-1])
    axs[0].set_ylim(0, 8e9)
    axs[1].set_ylim(0, 40)
    axs[2].set_ylim(0, 20e9)
    axs[3].set_ylim(0, 2)
    axs[4].set_ylim(0, 1000e9)
    for ax_, formatter_ in zip(axs,
                               [EngFormatter(places=0, sep="\N{THIN SPACE}"),
                                EngFormatter(places=0, sep="\N{THIN SPACE}"),
                                EngFormatter(places=0, sep="\N{THIN SPACE}"),
                                ScalarFormatter(),
                                EngFormatter(places=0, sep="\N{THIN SPACE}")]):
        ax_.tick_params(axis='y', rotation=90)
        ax_.yaxis.set_major_locator(plt.MaxNLocator(4))
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
