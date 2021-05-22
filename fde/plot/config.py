#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : east
# @time    : 2021/5/22 19:12
# @file    : config.py
# @project : FDE

import matplotlib
import matplotlib.pyplot as plt


# Constant
# --------

plt.rcParams.update({
    "text.usetex": True,
    # "font.family": "sans-serif",
    "font.family": "Times New Roman",
})

line_styles = [
    'solid', 
    (0, (18, 15)), 
    'dashed', 
    (0, (18, 10, 1, 10)), 
    (0, (18, 8, 1, 5, 1, 8)),
    "-.",
    (0, (1, 10))
]

title_style = {
    "fontfamily": "Times New Roman",
    "fontsize": 20,
    "y": 1.05,
}

label_style = {
    "fontfamily": "Times New Roman",
    "fontsize": 18
}

legend_style = {
    "shadow": True,
    "loc": 'best',
    "labelspacing": 0.2,
    "columnspacing": 0.8,
    "handletextpad": 0.5,
    "prop": {
        "size": 14,
        "family": "Arial"
    }
}

tick_style = {
    "labelsize": 14
}

line_style = {
    "alpha": 1.,
    "linewidth": 1.2,
}


# Functions
# ---------

def get_ax(title="", xlabel=r"\textbf{x}", ylabel=r"\textbf{y}"):
    fig_0, ax_0 = plt.subplots(
        figsize=(8, 6),
        tight_layout=True
    )

    ax_0.tick_params(
        **tick_style
    )
    ax_0.set_xlabel(
        xlabel,
        **label_style
    )
    ax_0.set_ylabel(
        ylabel,
        **label_style
    )
    ax_0.set_title(
        title,
        **title_style
    )
    
    return fig_0, ax_0


def set_ax(ax_0, legend=True):
    if legend:
        ax_0.legend(
            **legend_style
        )

    ax_0.ticklabel_format(
        axis='y',
        style='scientific',
        useMathText=True,
        scilimits=(-3, 4)
    )
    tx = ax_0.yaxis.get_offset_text()
    tx.set_fontname('Times New Roman')
    tx.set_fontsize(16)
