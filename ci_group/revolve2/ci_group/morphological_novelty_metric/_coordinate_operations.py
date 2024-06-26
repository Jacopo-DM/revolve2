from itertools import product
from typing import TYPE_CHECKING, Any

import numpy as np
from numpy.typing import NDArray
from revolve2.modular_robot.body import Module
from revolve2.modular_robot.body.base import Body

if TYPE_CHECKING:
    from pyrr import Vector3


def coords_from_bodies(
    bodies: list[Body], *, cob_heuristics: bool
) -> list[NDArray[np.float64]]:
    """Extract coordinates of modules from a body.

    :param bodies: The bodies.
    :type bodies: list[Body]
    :param *:
    :param cob_heuristics: If change of basis heuristic approximation is
        used.
    :type cob_heuristics: bool
    :returns: The array of coordinates.
    :rtype: list[NDArray[np.float64]]

    """
    crds = _body_to_adjusted_coordinates(bodies)
    if cob_heuristics:
        _coordinates_pca_heuristic(crds)
    else:
        _coordinates_pca_change_basis(crds)
    return crds


def _body_to_adjusted_coordinates(
    bodies: list[Body],
) -> list[NDArray[np.float64]]:
    """Extract coordinates of modules in a body and adjusts them with the core
    position.

    :param bodies: The body.
    :type bodies: list[Body]
    :returns: The coordinates for each body.
    :rtype: list[NDArray[np.float64]]

    """
    crds = [np.empty(shape=0, dtype=np.float64)] * len(bodies)
    for i, body in enumerate(bodies):
        tpl: tuple[NDArray[Any], Vector3] = body.to_grid()
        body_array, core_position = tpl
        x, y, z = body_array.shape

        elements = []
        for xe, ye, ze in product(range(x), range(y), range(z)):
            target = body_array[xe, ye, ze]
            if isinstance(target, Module):
                elements.append(np.subtract((xe, ye, ze), core_position))
        crds[i] = np.asarray(elements)
    return crds


def _coordinates_pca_change_basis(
    coordinates: list[NDArray[np.float64]],
) -> None:
    """Transform the coordinate distribution by the magnitude of variance of
    the respective basis.

    The detailed steps of the transformation are discussed in the paper.

    :param coordinates: The coordinates.
    :rtype: None
    :type coordinates: list[NDArray[np.float64]]
    :rtype: None

    """
    for i, target_coordinates in enumerate(coordinates):
        if len(target_coordinates) > 1:
            covariance_matrix = np.cov(target_coordinates.T)
            eigen_values, eigen_vectors = np.linalg.eig(covariance_matrix)

            # sorting axis by amplitude of variance
            srt = np.argsort(eigen_values)[::-1]
            temp_coordinates = target_coordinates.copy()
            for j in range(len(srt)):
                if srt[j] == j:
                    continue
                candidate = srt[j]

                # here we start rotating using Rodrigues` rotation formula.
                rx, ry, rz = eigen_vectors[candidate] / np.linalg.norm(
                    eigen_vectors[candidate]
                )
                k = np.array([[0, -rz, ry], [rz, 0, -rx], [-ry, rx, 0]])
                rotation_matrix = np.identity(3) + 2 * np.dot(k, k)

                temp_coordinates = np.dot(target_coordinates, rotation_matrix.T)

                eigen_vectors[[j, candidate]] = eigen_vectors[[candidate, j]]
                srt[[j, candidate]] = srt[[candidate, j]]

            final_coordinates = np.linalg.inv(eigen_vectors).dot(
                temp_coordinates.T
            )
            coordinates[i] = final_coordinates.T


def _coordinates_pca_heuristic(crds: list[NDArray[np.float64]]) -> None:
    """Transform the coordinate distribution by the magnitude of variance of
    the respective basis.

    The heuristic approximation of the transformation by simply
    switching axes.

    :param crds: The coordinates.
    :rtype: None
    :type crds: list[NDArray[np.float64]]
    :rtype: None

    """
    for i, target_coords in enumerate(crds):
        if len(target_coords) > 1:
            covariance_matrix = np.cov(target_coords.T)
            eigen_values, _ = np.linalg.eig(covariance_matrix)
            srt = np.argsort(eigen_values)[::-1]
            for j in range(len(srt)):
                if srt[j] == j:
                    continue
                candidate = srt[j]
                target_coords[:, [j, candidate]] = target_coords[
                    :, [candidate, j]
                ]
                srt[[j, candidate]] = srt[[candidate, j]]
            crds[i] = target_coords
