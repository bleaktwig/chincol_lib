# No preamble _on purpose_. This should be ran with the python version in your
#     virtual environment!

import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import chincol_palette as chp

F2_PALETTE = chp.f2_palette()
DEF_NBINS: int = 10
DEF_LABEL: str = "Remember to label your data..."
FIGSX: int = 8
FIGSY: int = 6

def setup(
    xmin: float, xmax: float, nbins: int = DEF_NBINS,
    ymin: float = None, ymax: float = None, ratio: bool = False
) -> tuple[list[float], list[plt.Axes]]:
    """
    Setups binning and matplotlib, returning the setup bins and the list of ax
    objects.

    Args:
        xmin (xmax) : Minimum (maximum) value for the binned variable.
        nbins       : Number of bins for the binned variable.
        ymin (ymax) : Minimum (maximum) value for the counts.
        ratio       : True if we are to setup a ratio plot, False otherwise.

    Returns:
        Tuple with setup bins and the list of matplotlib ax objects.
    """
    # Prepare bins.
    step = (xmax - xmin) / nbins
    bins = np.arange(xmin, xmax + step/2, step)

    # Prepare figure.
    fig, axs = [None, None]
    if ratio:
        fig, axs = plt.subplots(
            nrows=2, ncols=1, figsize=(FIGSX, FIGSY), sharex=True,
            height_ratios=(3,1)
        )
    else:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(FIGSX,FIGSY))
        axs = [ax]

    # Prepare figure.
    if xmin is not None and xmax is not None: axs[-1].set_xlim(xmin, xmax)
    if ymin is not None and ymax is not None: axs[0] .set_ylim(ymin, ymax)
    axs[0].set_yscale("log")
    axs[0].set_ylabel("Count")

    if ratio:
        axs[1].set_ylabel("Ratio")
        fig.subplots_adjust(wspace=.0, hspace=.05)

    return bins, axs

def hist(
    ax: plt.Axes, bins: list[float], x: list[float],
    w: list[float] = None, c: str | int = None, l: str = DEF_LABEL
) -> list[float]:
    """
    Draws a histogram on an ax object.

    Args:
        ax   : plt.Axes object where we're drawing the histogram.
        bins : List of bins, as setup by chincol_hist.setup().
        x    : List of counts for the binned variable.
        w    : List of weights for the binned variable.
        c    : Color of the histogram in the F2 palette.
        l    : Label of the histogram.

    Returns:
        Generated histogram.
    """
    # Assert that w is the same size as x.
    if len(x) != len(w):
        raise ValueError("x and w arrays are of different lengths.")

    # Set color.
    if c == None: c = random.choice(F2_PALETTE.values())
    else:         c = F2_PALETTE[c]

    # Setup histogram.
    hist, _ = np.histogram(
        x, bins = bins,
        weights = w if w is not None else np.ones_like(x)
    )
    hist = np.concatenate((hist, [hist[-1]]))
    ax.step(
        bins, hist, where="post", linestyle='-', lw=1.5, color=c[0], label=l
    )

    # If weights were given, setup MC errors.
    if w is not None:
        errs, _ = np.histogram(x, bins=bins, weights=pow(w, 2))
        errs = np.sqrt(errs)
        errs = np.concatenate((errs, [errs[-1]]))
        ax.fill_between(
            bins, hist-errs, hist+errs, step="post", color=c[1], alpha=.5
        )

    return hist[:-1]

def hist_ratio(
    axs: list[plt.Axes], bins: list[float], x: list[float], w: list[float],
    wref: list[float], cl: tuple[str] = None,
    ll: tuple[str] = (DEF_LABEL, DEF_LABEL)
):
    """
    Draws a ratio histogram on a pair of ax objects.

    Args:
        axs  : list[plt.Axes] object where we're drawing the histogram.
        bins : List of bins, as setup by chincol_hist.setup().
        x    : List of counts for the binned variable.
        w    : List of weights for the binned variable.
        wref : List of reference weights against which we'll compute the ratio.
        cl   : 2 colors for the histogram in the F2 palette.
        ll   : 2 labels for the histogram.

    Returns:
        Generated histogram.
    """
    # Assert input.
    if len({len(l) for l in [x, w, wref]}) != 1:
        raise ValueError("Input lists (x, w, wref) are of different lengths.")

    # Plot x.
    hist_x = hist(axs[0], bins, x, w, cl[0], ll[0])

    # Set colors.
    if cl == None: cl = random.choices(F2_PALETTE.values(), k=2)
    else:          cl = [F2_PALETTE[c] for c in cl]

    # Get reference and ratio histograms.
    hist_ref, _ = np.histogram(x, bins=bins, weights=wref)
    hist_rat = hist_x / hist_ref
    hist_ref = np.concatenate((hist_ref, [hist_ref[-1]]))
    hist_rat = np.concatenate((hist_rat, [hist_rat[-1]]))

    # Plot histograms.
    axs[0].step(
        bins, hist_ref, where="post", linestyle='-', lw=1.5, color=cl[1][0],
        label=ll[1]
    )
    axs[1].step(
        bins, hist_rat, where="post", linestyle='-', lw=1.5, color=cl[1][0]
    )
    axs[1].axhline(y=1, color=cl[1][1], lw=1.5, linestyle=":")

    # Add legend.
    axs[0].legend()

    return
