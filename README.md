# DIST-S1-Calibration

We assume that change maps are functionally represented as a thresholded distance function between pre-event and post-event images. That is to say, we have some "metric" that we quantify disturbance in a "post-image" scene relative to a set of "pre-images":
$$
\textrm{dist}(\{\textrm{pre-images}\}, \textrm{post-image})\rightarrow \mathbb R_{\geq 0} 
$$
Using $\textrm{dist}$, we can find a suitable $T \in \mathbb R$ such that a change map is given by $\textrm{dist} > T$. Often $T$ is determined empirically at given site, but as we are determining these change maps operationally, we need to calibrate $T$ and additional metric parameters. These notebooks are determining provide some insight into this calibration activity.

# Install

Install `dist-s1` environment (see the `environment.yml` from the research repository) and install `distmetrics` (which is currently private repo). Also needed is `einops` for the transformer model (see the `distmetrics` repository and it's `environment.yml`). Make sure to install the `dist-s1` kernel too.


# Usage

`python run.py --event chile_fire_2024 --distmetric_name 'mahalanobis_2d mahalanobis_vh mahalanobis_1d_max log_ratio_vh transformer'`