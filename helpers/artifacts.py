"""
Adaptive detection of holography edge-band artifacts.

Two-photon recordings on the holography rig show bright vertical bands at the
left/right (X) edges of the frame, produced by the photostim/SLM path. The band
is a grid/moire texture, so its per-column *mean* is elevated while its *median*
is not, and it is **transient** -- present only on the frames acquired while the
photostim is firing, not on every frame.

Historically these were trimmed by a single hardcoded, symmetric crop passed to
suite2p via ``ops['remove_artifacts'] = (x_start, x_end)`` (see ``s2p_ops.py``,
e.g. ``(75, 512-75)``). That constant under-captures the band (the real inner
edge sits a bit further in, ~x=90) and hardcodes a 512-px frame width.

:func:`detect_artifact_bounds` reads the actual recording and returns the
``(x_start, x_end)`` columns to keep. The trick is to isolate the artifact by
**difference**: average the artifact frames and subtract the average of the
clean frames, which cancels the (static) tissue and leaves the band standing
proud of a flat interior. Bands are then the bright, edge-contiguous columns of
that difference profile. If no transient artifact is present (a clean recording,
or one with no photostim), it returns ``(0, Lx)`` -- no crop.

Note on the penumbra (``min_crop``). Where the band is *visible* is not where the
contamination *ends*. On KKS082-1/260804 the bands were bright out to x~90, but
ROIs segmented as far in as x~147 still showed a step locked to the photostim
window -- 89% of cells in the outermost 64 px and 30% in the next 64 px, against
~1-3% across the interior, and flat in Y (so it is the X bands, not a general
edge effect). Uncorrected that faked a positive "network" response in cells far
from every target. Hence ``min_crop``: a floor in px/side applied on top of
detection, so the crop covers the penumbra while detection can still widen it
when the real band is bigger.
"""
import numpy as np


def _smooth(x, w):
    """Simple odd-window moving average (numpy-only, avoids a scipy dep)."""
    if w <= 1:
        return x
    w = int(w) | 1  # force odd
    pad = w // 2
    xp = np.pad(x, pad, mode="edge")
    return np.convolve(xp, np.ones(w) / w, mode="valid")


def _resolve_fallback(fallback, Lx):
    """
    Turn a ``fallback`` spec into concrete ``(x_start, x_end)`` bounds.

    Accepts ``None`` (-> no crop, ``(0, Lx)``), an int (symmetric crop of that
    many px per side), or an explicit ``(x_start, x_end)`` tuple.
    """
    if fallback is None:
        return (0, Lx)
    if isinstance(fallback, (int, np.integer)):
        f = int(fallback)
        return (min(f, Lx // 2), max(Lx - f, Lx // 2))
    if isinstance(fallback, (tuple, list)) and len(fallback) == 2:
        xs, xe = int(fallback[0]), int(fallback[1])
        return (max(0, xs), min(Lx, xe))
    raise ValueError(f"bad fallback {fallback!r}: expected None, int, or (xs, xe)")


def _iter_planes(data, nplanes, nchannels, ch):
    """Yield (plane_index, (nframes, Y, X)) for one channel of interleaved data."""
    for z in range(nplanes):
        sl = slice((z * nchannels) + ch, None, nplanes * nchannels)
        yield z, data[sl]


def _band_profile(plane_stack, edge_px=60, art_z=4.0, clean_z=1.0):
    """
    Isolate the artifact band on one plane by differencing artifact vs clean
    frames (cancels static tissue).

    Returns (profile, n_artifact) where ``profile`` is the length-X mean-over-rows
    difference (artifact_mean - clean_mean), or ``None`` if the plane has no clear
    transient (too few artifact or clean frames to difference).
    """
    stack = np.asarray(plane_stack, dtype=np.float64)
    if stack.ndim != 3 or stack.shape[0] < 4:
        return None, 0
    N, Y, X = stack.shape

    # per-frame edge-vs-interior brightness (mean over rows); the band lifts the
    # edge strips relative to the interior only on photostim frames
    colmean = stack.mean(1)                       # (N, X)
    edge = np.c_[colmean[:, :edge_px], colmean[:, -edge_px:]].mean(1)
    interior = colmean[:, int(0.3 * X):int(0.7 * X)].mean(1)
    score = edge - interior

    m = np.median(score)
    s = 1.4826 * np.median(np.abs(score - m)) + 1e-6
    zf = (score - m) / s
    art = np.where(zf > art_z)[0]
    clean = np.where(zf < clean_z)[0]
    if len(art) < 1 or len(clean) < 2:
        return None, len(art)

    diff = stack[art].mean(0) - stack[clean].mean(0)   # tissue cancels
    return diff.mean(0), len(art)


def detect_artifact_bounds(data, nplanes=1, nchannels=1, func_ch=0,
                           k=6.0, smooth=7, margin=3, max_frac=0.30,
                           edge_px=60, fallback=None, min_crop=None,
                           return_info=False):
    """
    Detect the transient holography edge bands and return columns to keep.

    Args:
        data (np.ndarray): the recording. Either a single plane's ``(nframes, Y,
            X)`` stack (use ``nplanes=1, nchannels=1``), or the raw interleaved
            suite2p array with ``nplanes``/``nchannels`` set so the functional
            channel's planes can be de-interleaved.
        nplanes, nchannels (int): acquisition layout for de-interleaving.
        func_ch (int): 0-based functional channel to analyse.
        k (float): band threshold in robust-std units above the (flat) interior
            of the difference profile. Lower = more aggressive trimming.
        smooth (int): moving-average window applied to the profile.
        margin (int): extra pixels trimmed inward past the detected band edge.
        max_frac (float): hard cap on the fraction of width trimmed per side.
        edge_px (int): width of the edge strips used to score artifact frames.
        fallback: bounds to use when nothing is detected (e.g. the sample tiff
            has no photostim frames, so the band can't be seen here even though
            other tiffs in the epoch have it). ``None`` -> no crop; an int ->
            symmetric px-per-side crop; a ``(xs, xe)`` tuple -> those bounds.
        min_crop (int | None): floor on the crop, in px per side, applied to the
            detected bounds *and* to the fallback. The band's visible edge
            under-states how far the contamination reaches: on KKS082-1/260804
            the detected inner edge sat at x~90 while ROIs out to x~147 still
            carried a photostim-locked step (see the note at module level). A
            floor widens the crop to cover that penumbra without giving up
            data-driven detection when the real band is wider still. ``None``
            keeps the detected/fallback bounds as-is.
        return_info (bool): also return a dict of intermediates (for plotting).

    Returns:
        (x_start, x_end): integer columns to keep -- suite2p uses
        ``frame[:, x_start:x_end]``. When no transient band is found on any plane
        the resolved ``fallback`` is returned (``(0, Lx)`` / no crop by default).
        Either way ``min_crop`` is then enforced. With ``return_info`` returns
        ``((x_start, x_end), info)``.
    """
    data = np.asarray(data)
    if data.ndim != 3:
        raise ValueError(f"expected 3-D (frames, Y, X) data, got {data.shape}")
    Lx = data.shape[2]

    # per-plane difference profiles; average the planes that show a transient
    # (the SLM band is the same across depths, tissue differs -> average diffs)
    profiles, n_art = [], 0
    for _z, pstack in _iter_planes(data, nplanes, nchannels, func_ch):
        prof, na = _band_profile(pstack, edge_px=edge_px)
        if prof is not None:
            profiles.append(prof)
            n_art += na

    prof = base = thr = None
    if profiles:
        prof = _smooth(np.mean(profiles, axis=0), smooth)
        # difference interior is flat ~0 (tissue cancelled); band = edge-contiguous
        # columns standing above interior noise
        interior = prof[int(0.3 * Lx):int(0.7 * Lx)]
        base = np.median(interior)
        rstd = 1.4826 * np.median(np.abs(interior - base)) + 1e-6
        thr = base + k * rstd
        hot = prof > thr
        cap = int(max_frac * Lx)

        x_start = int(np.argmin(hot)) if hot[0] else 0          # end of left band
        x_end = Lx - int(np.argmin(hot[::-1])) if hot[-1] else Lx  # start of right band
        if x_start > 0:
            x_start = min(x_start + margin, cap)
        if x_end < Lx:
            x_end = max(x_end - margin, Lx - cap)
        x_start = int(np.clip(x_start, 0, Lx))
        x_end = int(np.clip(x_end, 0, Lx))
        if x_end <= x_start:                # degenerate -> treat as not detected
            x_start, x_end = 0, Lx
        bounds = (x_start, x_end)
    else:
        bounds = (0, Lx)                    # no transient anywhere

    # nothing detected -> apply the fallback crop (e.g. this tiff had no
    # photostim, but other tiffs in the epoch do)
    detected = bounds != (0, Lx)
    if not detected:
        bounds = _resolve_fallback(fallback, Lx)

    # enforce the minimum crop last, so it floors both paths. Detection sees only
    # where the band is *visible*; contaminated ROIs extend past that.
    widened = False
    if min_crop:
        # cap the floor the same way max_frac caps detection, so a mis-set
        # min_crop can never empty the frame (0.4 keeps >=20% of the width)
        f = min(int(min_crop), int(0.4 * Lx))
        xs, xe = max(bounds[0], f), min(bounds[1], Lx - f)
        widened = (xs, xe) != tuple(bounds)
        bounds = (xs, xe)

    if return_info:
        info = dict(profile=prof, threshold=thr, baseline=base,
                    n_artifact=n_art, n_planes=len(profiles), Lx=Lx,
                    detected=detected, widened_to_min_crop=widened,
                    fallback_used=(not detected and fallback is not None))
        return bounds, info
    return bounds


def debug_plot(data, nplanes=1, nchannels=1, func_ch=0, save_path=None, **kwargs):
    """
    Visualize detection: the difference band-profile with threshold and detected
    bounds. Returns the matplotlib Figure (and prints where it saved).
    """
    import matplotlib
    if save_path is not None:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    bounds, info = detect_artifact_bounds(
        data, nplanes=nplanes, nchannels=nchannels, func_ch=func_ch,
        return_info=True, **kwargs)
    x_start, x_end = bounds

    fig, ax = plt.subplots(figsize=(10, 4))
    if not info["detected"]:
        how = "fallback" if info["fallback_used"] else "no crop"
        ax.set_title(f"no transient artifact detected -> {how} "
                     f"keep x[{x_start}:{x_end}]")
    else:
        ax.plot(info["profile"], label="band profile (artifact - clean, mean/row)")
        ax.axhline(info["threshold"], color="orange", ls="--", label="threshold")
        ax.axhline(info["baseline"], color="gray", ls=":", label="interior baseline")
        for x in (x_start, x_end):
            ax.axvline(x, color="r", lw=2)
        ax.set_title(f"keep x[{x_start}:{x_end}]  "
                     f"(trim L={x_start}, R={info['Lx'] - x_end}; "
                     f"{info['n_artifact']} artifact frames, {info['n_planes']} planes)")
        ax.legend(loc="upper center", fontsize=8)
    ax.set_xlabel("x pixel")
    fig.tight_layout()
    if save_path is not None:
        fig.savefig(save_path, dpi=100)
        print(f"saved {save_path}")
    return fig
