"""
A program for solving one-dimensional integrals via Monte Carlo method.
"""

import matplotlib.pyplot as plt
import numpy as np


def f_at_x(x):
    """The function to be integrated.

    Parameters
    ---------
    x: float
        The independent variable.

    Returns
    -------
    f_x: float
        The value of the function evaluated at given point.
    """

    # Do you recognize this function?
    f_x = np.sqrt(1 - x ** 2)

    # TODO: What happens if the functions is...?
    # f_x = np.sqrt(1 - x ** 2) * x ** 2
    return f_x


def montecarlo_integral(f_at_x, limits=(0, 1), N_points=1e5, dense_output=False):
    """Integrates the fiven function within desired lower and upper limits via
    Monte Carlo integration.

    Parameters
    ----------
    f_at_x: function
        Name of the function to be integrated.
    limits: tuple
        Lower and upper limits of integration.
    N_points: int
        Number of points: the higher this number, the greater the accuracy.
    dense_output: boolean
        If `True` inside and outside points are returned.

    Returns
    -------
    I_val: float
        The value for the integral (a.k.a. area under the curve).
    """

    # Lower limit is named 'a' while upper one is 'b'
    a, b = limits

    # Provided limits must have different values and in increasing order
    try:
        assert a < b
    except AssertionError:
        raise ValueError(f"Provided {limits = } are not valid ones.")

    # Evaluate function value. Lower limit is named 'a' while upper one is 'b'.
    # You could use the 'limits' variable here instead of '(a, b)', but this
    # last way is more explicit.
    f_at_a, f_at_b = [f_at_x(x) for x in (a, b)]

    # Compute the base and height of the rectangle and collect those inside the
    # same matrix.
    rectangle_base, rectangle_height = b - a, max([f_at_a, f_at_b])
    rectangle_sides = np.array([rectangle_base, rectangle_height])

    # Evaluate the area of the rectangle
    rectangle_area = rectangle_base * rectangle_height

    # Generate a collection of random x and y values, all of them located within
    # the desired rectangle. Notice the random function generates values between
    # [0, 1] whose purpose is to be used as scaling values. In addition, the
    # value of 'a' limit needs to be added to the x-coordinates in order to
    # shitf the location of this points
    random_points = (
        np.array([a, 0]) + np.random.rand(int(N_points), 2) * rectangle_sides
    )
    rand_x, rand_f_at_x = random_points.T

    # Evaluate the function at previously randomly generated x-coordinates. The
    # x-coordinates are located in the first column of the matrix
    f_at_rand_x = f_at_x(rand_x)

    # Compare randomly generated y-coordinates with previously computed ones
    is_below_curve = rand_f_at_x < f_at_rand_x

    # Guess the area below the curve
    I_val = rectangle_area * (len(random_points[is_below_curve]) / int(N_points))

    # Returns desired amount of values
    if dense_output is False:
        return I_val
    else:
        return I_val, random_points[is_below_curve], random_points[~is_below_curve]


def plot_function(f_at_x, limits=(0, 1), N_points=100, ax=None, **kargs):
    """Plots a given function within desired limits.

    Parameters
    ----------
    f_at_x: function
        The function to be plotted.
    limits: tuple
        Lower and upper limits for the independent variable.
    ax: ~matplotlib.pyplot.Axes
        The axes for drawing the figure.
    **kargs: dict
        A dictionary holding additional customization options.
    """

    # Check if axes available
    if ax is None:
        _, ax = plt.subplots()

    # Generate a set of points for the independent variable
    a, b = limits
    x = np.linspace(a, b, N_points + 1)

    # Evaluate the function at previous points
    f_x = f_at_x(x)

    # Plot the values
    ax.plot(x, f_x, **kargs)
    return ax

def plot_points(points, ax=None, **kargs):
    """Plots desired points on given axes.

    Parameters
    ----------
    points: ~np.ndarray
        An Nx2 matrix holding the x and y coordinates of the points.
    ax: ~matplotlib.pyplot.Axes
        Axes of the figure.
    **kargs: dict
        Additional customization parameters.
    """

    if ax is None:
        _, ax = plt.subplots()

    ax.scatter(points[:,0], points[:,1], **kargs)
    return ax

def main():
    """Entry point of the script."""

    # Compute the area under the curve and collect random points
    I_val, below_points, above_points = montecarlo_integral(
            f_at_x, limits=(0, 1), N_points=1e4, dense_output=True
    )
    print(f"Area under the curve = {I_val:.5f}.")

    # Draw the function and the points to have a graphical representation
    fig, ax = plt.subplots()
    ax = plot_function(f_at_x, ax=ax, color="k")
    ax = plot_points(below_points, ax=ax, color="g", s=1.5)
    ax = plot_points(above_points, ax=ax, color="r", s=1.5)

    # Add figure title and labels
    ax.set_title(r"Integrating $f(x)$ via Monte Carlo")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$f(x)$")
    ax.set_aspect("equal")
    plt.show()


if __name__ == "__main__":
    main()
