"""
pyart.util.circular_stats
=========================

Functions for computing statistics on circular (directional) distributions.

.. autosummary::
    :toctree: generated/

    angular_mean
    angular_std
    angular_mean_deg
    angular_std_deg
    interval_mean
    interval_std

"""

import numpy as np


# For details on these computation see:
# https://en.wikipedia.org/wiki/Directional_statistics
# https://en.wikipedia.org/wiki/Mean_of_circular_quantities


def angular_mean(angles):
    """
    Compute the mean of a distribution of angles in radians.

    Parameters
    ----------
    angles : array like
        Distribution of angles in radians.

    Returns
    -------
    mean : float
        The mean angle of the distribution in radians.

    """
    angles = np.asanyarray(angles)
    x = np.cos(angles)
    y = np.sin(angles)
    return np.arctan2(y.mean(), x.mean())


def angular_std(angles):
    """
    Compute the standard deviation of a distribution of angles in radians.

    Parameters
    ----------
    angles : array like
        Distribution of angles in radians.

    Returns
    -------
    std : float
        Standard deviation of the distribution.

    """
    angles = np.asanyarray(angles)
    x = np.cos(angles)
    y = np.sin(angles)
    norm = np.sqrt(x.mean()**2 + y.mean()**2)
    return np.sqrt(-2 * np.log(norm))


def angular_mean_deg(angles):
    """
    Compute the mean of a distribution of angles in degrees.

    Parameters
    ----------
    angles : array like
        Distribution of angles in degrees.

    Returns
    -------
    mean : float
        The mean angle of the distribution in degrees.

    """
    return np.rad2deg(angular_mean(np.deg2rad(angles)))


def angular_std_deg(angles):
    """
    Compute the standard deviation of a distribution of angles in degrees.

    Parameters
    ----------
    angles : array like
        Distribution of angles in degrees.

    Returns
    -------
    std : float
        Standard deviation of the distribution.

    """
    return np.rad2deg(angular_std(np.deg2rad(angles)))


def interval_mean(dist, interval_min, interval_max):
    """
    Compute the mean of a distribution within an interval.

    Return the average of the array elements which are interpreted as being
    taken from a circular interval with endpoints given by interval_min and
    interval_max.

    Parameters
    ----------
    dist : array like
        Distribution of values within an interval.
    interval_min, interval_max : float
        The endpoints of the interval.

    Returns
    -------
    mean : float
        The mean value of the distribution

    """
    # transform distribution from original interval to [-pi, pi]
    half_width = (interval_max - interval_min) / 2.
    center = interval_min + half_width
    a = (np.asarray(dist) - center) / (half_width) * np.pi

    # compute the angular mean and convert back to original interval
    a_mean = angular_mean(a)
    return (a_mean * (half_width) / np.pi) + center


def interval_std(dist, interval_min, interval_max):
    """
    Compute the standard deviation of a distribution within an interval.

    Return the standard deviation of the array elements which are interpreted
    as being taken from a circular interval with endpoints given by
    interval_min and interval_max.

    Parameters
    ----------
    dist : array_like
        Distribution of values within an interval.
    interval_min, interval_max : float
        The endpoints of the interval.

    Returns
    -------
    std : float
        The standard deviation of the distribution.

    """
    # transform distribution from original interval to [-pi, pi]
    half_width = (interval_max - interval_min) / 2.
    center = interval_min + half_width
    a = (np.asarray(dist) - center) / (half_width) * np.pi

    # compute the angular standard dev. and convert back to original interval
    a_std = angular_std(a)
    return (a_std * (half_width) / np.pi)
