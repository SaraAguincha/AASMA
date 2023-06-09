import math
from typing import Optional, Sequence

import numpy as np
import matplotlib.pyplot as plt


def z_table(confidence):
    """Hand-coded Z-Table

    Parameters
    ----------
    confidence: float
        The confidence level for the z-value.

    Returns
    -------
        The z-value for the confidence level given.
    """
    return {
        0.99: 2.576,
        0.95: 1.96,
        0.90: 1.645
    }[confidence]


def confidence_interval(mean, n, confidence):
    """Computes the confidence interval of a sample.

    Parameters
    ----------
    mean: float
        The mean of the sample
    n: int
        The size of the sample
    confidence: float
        The confidence level for the z-value.

    Returns
    -------
        The confidence interval.
    """
    return z_table(confidence) * (mean / math.sqrt(n))


def standard_error(std_dev, n, confidence):
    """Computes the standard error of a sample.

    Parameters
    ----------
    std_dev: float
        The standard deviation of the sample
    n: int
        The size of the sample
    confidence: float
        The confidence level for the z-value.

    Returns
    -------
        The standard error.
    """
    return z_table(confidence) * (std_dev / math.sqrt(n))


def plot_confidence_bar(names, means, std_devs, N, title, x_label, y_label, confidence, show=False, filename=None, colors=None, yscale=None):
    """Creates a bar plot for comparing different agents/teams.

    Parameters
    ----------

    names: Sequence[str]
        A sequence of names (representing either the agent names or the team names)
    means: Sequence[float]
        A sequence of means (one mean for each name)
    std_devs: Sequence[float]
        A sequence of standard deviations (one for each name)
    N: Sequence[int]
        A sequence of sample sizes (one for each name)
    title: str
        The title of the plot
    x_label: str
        The label for the x-axis (e.g. "Agents" or "Teams")
    y_label: str
        The label for the y-axis
    confidence: float
        The confidence level for the confidence interval
    show: bool
        Whether to show the plot
    filename: str
        If given, saves the plot to a file
    colors: Optional[Sequence[str]]
        A sequence of colors (one for each name)
    yscale: str
        The scale for the y-axis (default: linear)
    """

    errors = [standard_error(std_devs[i], N[i], confidence) for i in range(len(means))]
    fig, ax = plt.subplots()
    x_pos = np.arange(len(names))
    ax.bar(x_pos, means, yerr=errors, align='center', alpha=0.5, color=colors if colors is not None else "gray", ecolor='black', capsize=10)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(names)
    ax.set_title(title)
    ax.yaxis.grid(True)
    if yscale is not None:
        plt.yscale(yscale)
    plt.tight_layout()
    if filename is not None:
        plt.savefig(filename)
    if show:
        plt.show()
    plt.close()


def compare_results(results, confidence=0.95, title="Agents Comparison", metric="Steps Per Episode", colors=None):

    """Displays a bar plot comparing the performance of different agents/teams.

        Parameters
        ----------

        results: dict
            A dictionary where keys are the names and the values sequences of trials
        confidence: float
            The confidence level for the confidence interval
        title: str
            The title of the plot
        metric: str
            The name of the metric for comparison
        colors: Sequence[str]
            A sequence of colors (one for each agent/team)

        """

    names = list(results.keys())
    means = [result.mean() for result in results.values()]
    stds = [result.std() for result in results.values()]
    N = [result.size for result in results.values()]

    plot_confidence_bar(
        names=names,
        means=means,
        std_devs=stds,
        N=N,
        title=title,
        x_label="", y_label=f"Avg. {metric}",
        confidence=confidence, show=True, colors=colors
    )


def plot_multiple_confidence_bars(axs, names, means, std_devs, N, title, x_label, y_label, confidence, filename=None, colors=None, yscale=None):
    """Creates multiple bar plots for comparing different agents/teams, with different metrics.

    Parameters
    ----------

    names: Sequence[str]
        A sequence of names (representing either the agent names or the team names)
    means: Sequence[float]
        A sequence of means (one mean for each name)
    std_devs: Sequence[float]
        A sequence of standard deviations (one for each name)
    N: Sequence[int]
        A sequence of sample sizes (one for each name)
    title: str
        The title of the plot
    x_label: str
        The label for the x-axis (e.g. "Agents" or "Teams")
    y_label: str
        The label for the y-axis
    confidence: float
        The confidence level for the confidence interval
    show: bool
        Whether to show the plot
    filename: str
        If given, saves the plot to a file
    colors: Optional[Sequence[str]]
        A sequence of colors (one for each name)
    yscale: str
        The scale for the y-axis (default: linear)
    """

    errors = [standard_error(std_devs[i], N[i], confidence) for i in range(len(means))]
    x_pos = np.arange(len(names))
    
    axs.bar(x_pos, means, yerr=errors, align='center', alpha=0.5, color=colors if colors is not None else "gray", ecolor='black', capsize=10)
    axs.set_ylabel(y_label)
    axs.set_xlabel(x_label)
    axs.set_xticks(x_pos)
    axs.set_xticklabels(names)
    axs.set_title(title)
    axs.yaxis.grid(True)
    

def compare_all_results(results, collisions, waitingTime, confidence=0.95, title="Agents Comparison", metric="Steps Per Episode", colors=None):

    """Displays a bar plot comparing the performance of different agents/teams.

        Parameters
        ----------

        results: dict
            A dictionary where keys are the names and the values sequences of trials
        confidence: float
            The confidence level for the confidence interval
        title: str
            The title of the plot
        metric: str
            The name of the metric for comparison
        colors: Sequence[str]
            A sequence of colors (one for each agent/team)

        """

    # same for every plot
    names = list(results.keys())
    
    results_means = [result.mean() for result in results.values()]   
    results_stds = [result.std() for result in results.values()]
    results_N = [result.size for result in results.values()]
    
    collisions_means = [collision.mean() for collision in collisions.values()]
    collisions_stds = [collision.std() for collision in collisions.values()]
    collisions_N = [collision.size for collision in collisions.values()]
    
    waitingTime_means = [wait.mean() for wait in waitingTime.values()]
    waitingTime_stds = [wait.std() for wait in waitingTime.values()]
    waitingTime_N = [wait.size for wait in waitingTime.values()]
    
    fig, axs = plt.subplots(3,1)

    plot_multiple_confidence_bars(
        axs[0],
        names=names,
        means=results_means,
        std_devs=results_stds,
        N=results_N,
        title=title,
        x_label="", y_label=f"Avg. {metric}",
        confidence=confidence, colors=colors
    )
    
    plot_multiple_confidence_bars(
        axs[1],
        names=names,
        means=collisions_means,
        std_devs=collisions_stds,
        N=collisions_N,
        title="",
        x_label="", y_label=f"Avg. collisions Per Episode",
        confidence=confidence, colors=colors
    )
    
    plot_multiple_confidence_bars(
        axs[2],
        names=names,
        means=waitingTime_means,
        std_devs=waitingTime_stds,
        N=waitingTime_N,
        title="",
        x_label="", y_label=f"Avg. Waiting time Per Episode",
        confidence=confidence, colors=colors
    )
    
    plt.show()
    plt.close()
    
    
    
def compare_results_and_collisions(results, collisions, confidence=0.95, title="Agents Comparison", metric="Steps Per Episode", colors=None):

    """Displays a bar plot comparing the performance of different agents/teams.

        Parameters
        ----------

        results: dict
            A dictionary where keys are the names and the values sequences of trials
        confidence: float
            The confidence level for the confidence interval
        title: str
            The title of the plot
        metric: str
            The name of the metric for comparison
        colors: Sequence[str]
            A sequence of colors (one for each agent/team)

        """

    # same for every plot
    names = list(results.keys())
    
    results_means = [result.mean() for result in results.values()]   
    results_stds = [result.std() for result in results.values()]
    results_N = [result.size for result in results.values()]
    
    collisions_means = [collision.mean() for collision in collisions.values()]
    collisions_stds = [collision.std() for collision in collisions.values()]
    collisions_N = [collision.size for collision in collisions.values()]
    
    fig, axs = plt.subplots(2,1)

    plot_multiple_confidence_bars(
        axs[0],
        names=names,
        means=results_means,
        std_devs=results_stds,
        N=results_N,
        title=title,
        x_label="", y_label=f"Avg. {metric}",
        confidence=confidence, colors=colors
    )
    
    plot_multiple_confidence_bars(
        axs[1],
        names=names,
        means=collisions_means,
        std_devs=collisions_stds,
        N=collisions_N,
        title="",
        x_label="", y_label=f"Avg. collisions Per Episode",
        confidence=confidence, colors=colors
    )
    
    plt.show()
    plt.close()
