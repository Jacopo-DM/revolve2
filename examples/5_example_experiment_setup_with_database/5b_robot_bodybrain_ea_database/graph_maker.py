import pickle

import matplotlib.pyplot as plt
import numpy as np

"""Plot the number of modules per robot over time

Plot the number of hinges per robot over time

Plot the ratio of hinges to bricks over time

Plot the symmetry over time

Later on, you could plot all morph descriptors of Karine for all algos in search of one where they differ.

"""

# load  dictionary.pkl

path = "./exp/100/"

with open(f"{path}/dictionary.pkl", "rb") as file:
    _dict = pickle.load(file)


def general_plot(path, nmod_arr, name):
    nmod_max = np.max(nmod_arr, axis=0)
    nmod_min = np.min(nmod_arr, axis=0)
    nmod_mean = np.mean(nmod_arr, axis=0)
    nmod_std = np.std(nmod_arr, axis=0)

    plt.figure()
    plt.scatter(
        range(len(nmod_mean)),
        nmod_mean,
        label="Mean",
        color="blue",
        alpha=0.25,
    )
    plt.fill_between(
        range(len(nmod_mean)),
        nmod_mean - nmod_std,
        nmod_mean + nmod_std,
        alpha=0.2,
        label="Std",
    )
    plt.scatter(
        range(len(nmod_max)),
        nmod_max,
        label="Max",
        color="green",
        marker="o",
        alpha=0.1,
    )
    plt.scatter(
        range(len(nmod_min)),
        nmod_min,
        label="Min",
        color="red",
        marker="o",
        alpha=0.1,
    )
    plt.plot(nmod_mean, label="Mean")

    # Add smoothing line
    smoothed_nmod_mean = np.convolve(nmod_mean, np.ones(10) / 10, mode="same")
    plt.plot(smoothed_nmod_mean, color="orange", alpha=0.5)

    plt.xlabel("Generation")
    # plt.ylabel("Number of Modules")
    # plt.title("Number of Modules per Robot")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{path}/{name}.png", dpi=300)


# # Plot the symmetry over time
# for i in range(100):
#     plt.figure()
#     plt.plot(_dict[i]["xy_symmetry"], label="XY Symmetry")
#     plt.plot(_dict[i]["xz_symmetry"], label="XZ Symmetry")
#     plt.plot(_dict[i]["yz_symmetry"], label="YZ Symmetry")
#     plt.xlabel("Generation")
#     plt.ylabel("Symmetry")
#     plt.title(f"Experiment {i + 1}: Symmetry over Time")
#     plt.legend()
#     plt.savefig(f"{path}/experiment_{i + 1}_symmetry.png")

#     # Add random points
#     for _ in range(10):
#         random_points_xy = np.random.normal(
#             _dict[i]["xy_symmetry"], np.std(_dict[i]["xy_symmetry"])
#         )
#         random_points_xz = np.random.normal(
#             _dict[i]["xz_symmetry"], np.std(_dict[i]["xz_symmetry"])
#         )
#         random_points_yz = np.random.normal(
#             _dict[i]["yz_symmetry"], np.std(_dict[i]["yz_symmetry"])
#         )
#         plt.scatter(
#             range(len(_dict[i]["xy_symmetry"])),
#             random_points_xy,
#             color="blue",
#             alpha=0.25,
#         )
#         plt.scatter(
#             range(len(_dict[i]["xz_symmetry"])),
#             random_points_xz,
#             color="green",
#             alpha=0.25,
#         )
#         plt.scatter(
#             range(len(_dict[i]["yz_symmetry"])),
#             random_points_yz,
#             color="red",
#             alpha=0.25,
#         )

#     # save the plots
#     plt.savefig(f"{path}/experiment_{i + 1}_symmetry.png")


def symm_plotter(path, xy_sym, yz_sym, xz_sym, name):
    xy_sym_max = np.max(xy_sym, axis=0)
    xy_sym_min = np.min(xy_sym, axis=0)
    xy_sym_mean = np.mean(xy_sym, axis=0)

    xy_sym_std = np.std(xy_sym, axis=0)

    yz_sym_max = np.max(yz_sym, axis=0)
    yz_sym_min = np.min(yz_sym, axis=0)
    yz_sym_mean = np.mean(yz_sym, axis=0)

    yz_sym_std = np.std(yz_sym, axis=0)

    xz_sym_max = np.max(xz_sym, axis=0)
    xz_sym_min = np.min(xz_sym, axis=0)
    xz_sym_mean = np.mean(xz_sym, axis=0)

    xz_sym_std = np.std(xz_sym, axis=0)

    plt.figure()
    plt.scatter(
        range(len(xy_sym_mean)),
        xy_sym_mean,
        label="XY Symmetry",
        color="blue",
        alpha=0.25,
    )
    plt.scatter(
        range(len(xy_sym_max)),
        xy_sym_max,
        label="Max",
        color="blue",
        marker="o",
        alpha=0.1,
    )
    plt.scatter(
        range(len(xy_sym_min)),
        xy_sym_min,
        label="Min",
        color="blue",
        marker="o",
        alpha=0.1,
    )
    plt.plot(xy_sym_mean, label="Mean", color="blue")

    plt.scatter(
        range(len(yz_sym_mean)),
        yz_sym_mean,
        label="YZ Symmetry",
        color="red",
        alpha=0.25,
    )
    plt.scatter(
        range(len(yz_sym_max)),
        yz_sym_max,
        label="Max",
        color="red",
        marker="o",
        alpha=0.1,
    )
    plt.scatter(
        range(len(yz_sym_min)),
        yz_sym_min,
        label="Min",
        color="red",
        marker="o",
        alpha=0.1,
    )
    plt.plot(yz_sym_mean, label="Mean", color="red")

    plt.scatter(
        range(len(xz_sym_mean)),
        xz_sym_mean,
        label="XZ Symmetry",
        color="green",
        alpha=0.25,
    )
    plt.scatter(
        range(len(xz_sym_max)),
        xz_sym_max,
        label="Max",
        color="green",
        marker="o",
        alpha=0.1,
    )
    plt.scatter(
        range(len(xz_sym_min)),
        xz_sym_min,
        label="Min",
        color="green",
        marker="o",
        alpha=0.1,
    )
    plt.plot(xz_sym_mean, label="Mean", color="green")

    plt.xlabel("Generation")
    plt.legend(loc="upper left", fancybox=True, framealpha=0.8, shadow=True)
    plt.tight_layout()
    plt.savefig(f"{path}/{name}.png", dpi=300)


nmod_arr = np.array([_dict[i]["nmod"] for i in _dict])
general_plot(path, nmod_arr, "nmod")

nhin_arr = np.array([_dict[i]["nhin"] for i in _dict])
general_plot(path, nhin_arr, "nhin")

ratio_arr = np.array([_dict[i]["ratio"] for i in _dict])
general_plot(path, ratio_arr, "ratio")

xy_sym = np.array([_dict[i]["xy_symmetry"] for i in _dict])
yz_sym = np.array([_dict[i]["yz_symmetry"] for i in _dict])
xz_sym = np.array([_dict[i]["xz_symmetry"] for i in _dict])
symm_plotter(path, xy_sym, yz_sym, xz_sym, "symmetry")
