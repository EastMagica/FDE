#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : east
# @time    : 2021/5/22 19:05
# @file    : plot_basis_func.py
# @project : FDE

import matplotlib
import matplotlib.pyplot as plt


for n1_phi in [0, 2]:

    x_phi = [0, 1, 2, 3, 4]
    y_phi = [0, 0, 0, 0, 0]
    y_phi[n1_phi] = 1

    labels = [f'x{i}' for i in range(5)]

    with plt.xkcd():
        fig, ax = plt.subplots(
            figsize=(9, 3),
            tight_layout=True
        )

        ax.plot(
            x_phi, y_phi
        )
        ax.plot(
            [x_phi[n1_phi]]*2, [0, 1],
            linestyle="--"
        )
        ax.scatter(
            x_phi[n1_phi], 1,
            color="black",
            zorder=3
        )

        ax.annotate(
            f'THE  BASIC  FUNCTION\nPHI_{n1_phi}  DEFINED  IN  X_{n1_phi}',
            xy=(x_phi[n1_phi]+0.1, 1), 
            arrowprops=dict(arrowstyle='->'), 
            xytext=(x_phi[n1_phi]+0.75, 0.75)
        )

        fig.text(
            0.5, -0.1,
            '"The Mountain Function" from One dimensional linear element',
            ha='center',
            fontsize=18
        )

        ax.spines["right"].set_color('none')
        ax.spines["top"].set_color('none')

        ax.set_xticks(x_phi)
        ax.set_xticklabels(labels)
        ax.set_yticks([0, 1])

        ax.set_xlabel("Space", fontsize=15)
        ax.set_ylabel("Value", fontsize=15)

    plt.savefig(f"basis_fun_{n1_phi}.png")
