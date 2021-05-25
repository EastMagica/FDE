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


# Plot all basis in one figure
# ----------------------------

labels = [f'x{i}' for i in range(5)]

with plt.xkcd():
    fig, axs = plt.subplots(
        5, 1,
        figsize=(9, 12),
        sharex="col",
        tight_layout=True
    )

    for n1_phi in range(5):
        x_phi = [0, 1, 2, 3, 4]
        y_phi = [0, 0, 0, 0, 0]
        
        y_phi[n1_phi] = 1
        
        ax = axs[n1_phi]
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
            xy=(x_phi[n1_phi]+0.1, 1) if n1_phi < 2 else (x_phi[n1_phi]-0.1, 1), 
            arrowprops=dict(arrowstyle='->'), 
            xytext=(x_phi[n1_phi]+0.75, 0.75) if n1_phi < 2 else (x_phi[n1_phi]-2.1, 0.75),
            color="gray"
        )

        ax.spines["right"].set_color('none')
        ax.spines["top"].set_color('none')

        ax.set_xticks(x_phi)
        ax.set_xticklabels(labels)
        ax.set_yticks([0, 1])

        ax.set_xlabel("Space", fontsize=15)
        ax.set_ylabel("Value", fontsize=15)
        
    ax.text(
        2, -0.75,
        '"The Mountain Function" from One dimensional linear element',
        ha='center',
        fontsize=18,
    )

plt.savefig(f"basis_fun_all.png")    


from scipy.interpolate import lagrange

with plt.xkcd():
    fig, ax = plt.subplots(
        figsize=(9, 6),
        sharex="col",
        tight_layout=True
    )

    x_phi = [0, 1, 2, 3, 4]
    y_phi = [0.1, 0.5, 0.8, 0.6, 0.2]
    
    f = lagrange(x_phi, y_phi)    

#     y_phi[n1_phi] = 1

#     ax.plot(
#         x_phi, y_phi
#     )
#     ax.plot(
#         [x_phi[n1_phi]]*2, [0, 1],
#         linestyle="--"
#     )
#     ax.scatter(
#         x_phi[n1_phi], 1,
#         color="black",
#         zorder=3
#     )

    ax.bar(
        x_phi, y_phi,
        width=0.98,
        linewidth=3.0,
        hatch='//',
        fill=False,
        edgecolor='gray',
        align='edge'
    )
    
    ax.scatter(
        x_phi, y_phi,
        color='tab:red',
        zorder=3
    )
    
    ax.plot(
        np.linspace(0, 5, 101),
        f(np.linspace(0, 5, 101)),
        color="black"
    )

#     ax.annotate(
#         f'THE  BASIC  FUNCTION\nPHI_{n1_phi}  DEFINED  IN  X_{n1_phi}',
#         xy=(x_phi[n1_phi]+0.1, 1) if n1_phi < 2 else (x_phi[n1_phi]-0.1, 1), 
#         arrowprops=dict(arrowstyle='->'), 
#         xytext=(x_phi[n1_phi]+0.75, 0.75) if n1_phi < 2 else (x_phi[n1_phi]-2.1, 0.75),
#         color="gray"
#     )

    ax.spines["right"].set_color('none')
    ax.spines["top"].set_color('none')

    ax.set_xticks(x_phi+[5])
    ax.set_xticklabels(labels+['x5'])
    ax.set_yticks([0, 1])

    ax.set_xlabel("Space", fontsize=15)
    ax.set_ylabel("Value", fontsize=15)

    ax.text(
        2.5, -0.25,
        'Predictor y5 by "Rectangle Rule"',
        ha='center',
        fontsize=18,
    )

plt.savefig(f"rectangle_rule.png")    
