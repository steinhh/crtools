#!/usr/bin/env python3
"""
Example: sigma-based outlier detection using `fsigma_ext`.

This script demonstrates how to compute a local standard deviation (sigma) with
`fsigma_ext.fsigma`, compute a local neighbor mean in Python (excluding the center
pixel), form a z-score for each pixel, and threshold to detect outliers.

Usage: run from repository root after building the extensions:

    python3 fsigma/example_sigma_threshold.py

"""
import numpy as np
from fsigma import fsigma_ext

# Optional plotting (matplotlib). We save the figure to a file so the example
# works in both interactive and headless environments.
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    _HAS_MPL = True
except Exception:
    _HAS_MPL = False


def neighbor_mean_exclude_center(arr, xsize, ysize):
    """Compute per-pixel mean of the neighborhood excluding the center pixel.

    This is a simple, clear implementation (not optimized) intended for examples.
    It handles image boundaries by taking the intersection of the window with the
    image.
    """
    H, W = arr.shape
    out = np.zeros_like(arr, dtype=np.float64)
    for y in range(H):
        for x in range(W):
            y0 = max(0, y - ysize)
            y1 = min(H, y + ysize + 1)
            x0 = max(0, x - xsize)
            x1 = min(W, x + xsize + 1)
            window = arr[y0:y1, x0:x1]
            # Exclude center element if present
            if window.size == 1:
                out[y, x] = 0.0
            else:
                # Flatten and exclude the center element at relative position
                ry = y - y0
                rx = x - x0
                flat = window.flatten()
                center_idx = ry * (x1 - x0) + rx
                # Use np.mean on masked array to keep code simple
                out[y, x] = (flat.sum() - flat[center_idx]) / (flat.size - 1)
    return out


def main():
    # Build a sample image with a few outliers
    im = np.array(
        [
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            [10, 20, 20, 20, 20, 20, 20, 20, 20, 10],
            [10, 20, 30, 30, 30, 30, 30, 30, 20, 10],
            [10, 20, 30, 40, 40, 40, 40, 30, 20, 10],
            [10, 20, 30, 40, 100, 40, 40, 30, 20, 10],  # outlier at (4,4)
            [10, 20, 30, 40, 40, 40, 40, 30, 20, 10],
            [10, 20, 30, 30, 30, 30, 30, 30, 20, 10],
            [10, 20, 20, 20, 20, 20, 20, 20, 20, 10],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            [5, 10, 10, 10, 10, 10, 10, 10, 10, 5],
        ],
        dtype=np.float64,
    )

    H, W = im.shape
    xsize = 1
    ysize = 1

    print("Computing local sigma (exclude center from neighborhood)...")
    sigma = np.zeros_like(im, dtype=np.float64)
    fsigma_ext.fsigma(im, sigma, xsize, ysize, 1)

    print("Computing neighbor mean (exclude center)...")
    nmean = neighbor_mean_exclude_center(im, xsize, ysize)

    eps = 1e-8
    z = (im - nmean) / (sigma + eps)

    # Detect outliers at > 5 sigma
    thresh = 5.0
    mask = np.abs(z) > thresh

    print("Input image:")
    print(im)
    print("\nLocal sigma:")
    print(np.round(sigma, 3))
    print("\nLocal neighbor mean (exclude center):")
    print(np.round(nmean, 3))
    print("\nZ-score map (rounded):")
    print(np.round(z, 3))
    print(f"\nOutlier mask (|z| > {thresh}):")
    print(mask.astype(int))

    # Replace detected outliers with the local neighbor mean as a simple repair
    repaired = im.copy()
    repaired[mask] = nmean[mask]

    print("\nRepaired image (outliers replaced by local mean):")
    print(np.round(repaired, 3))

    # Summary
    num_outliers = np.count_nonzero(mask)
    print(f"\nDetected {num_outliers} outlier(s) using threshold {thresh} sigma")

    # Visualization: input, sigma, neighbor mean, z-score, mask, repaired
    if _HAS_MPL:
        fig, axes = plt.subplots(2, 3, figsize=(12, 8))
        ax = axes.ravel()
        im0 = ax[0].imshow(im, cmap='viridis')
        ax[0].set_title('Input')
        fig.colorbar(im0, ax=ax[0])

        im1 = ax[1].imshow(sigma, cmap='magma')
        ax[1].set_title('Local sigma')
        fig.colorbar(im1, ax=ax[1])

        im2 = ax[2].imshow(nmean, cmap='viridis')
        ax[2].set_title('Neighbor mean (excl center)')
        fig.colorbar(im2, ax=ax[2])

        im3 = ax[3].imshow(z, cmap='RdBu', vmin=-np.nanmax(np.abs(z)), vmax=np.nanmax(np.abs(z)))
        ax[3].set_title('Z-score')
        fig.colorbar(im3, ax=ax[3])

        im4 = ax[4].imshow(mask, cmap='gray')
        ax[4].set_title('Outlier mask')
        fig.colorbar(im4, ax=ax[4])

        im5 = ax[5].imshow(repaired, cmap='viridis')
        ax[5].set_title('Repaired')
        fig.colorbar(im5, ax=ax[5])

        plt.suptitle('fsigma: Sigma-based outlier detection')
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        out_path = 'fsigma/sigma_threshold.png'
        plt.savefig(out_path, dpi=150)
        print(f"\nSaved visualization to: {out_path}")
    else:
        print("matplotlib not available; skipping visualization.")


if __name__ == '__main__':
    main()
