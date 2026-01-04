"""
2026/01/04
cpano.sampling

- world <-> pixel conversion for north-up rasters
- nearest / bilinear sampling on rasters
- ray generation (polar sampling) and raster sampling along rays

Assumptions:
- Designed primarily for north-up rasters (transform.b == transform.d == 0).
  If you have rotated/sheared transforms, use rasterio.transform.rowcol for nearest,
  and consider warping rasters to north-up beforehand for bilinear.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional, Tuple, Union

import numpy as np
from affine import Affine

try:
    from rasterio.transform import rowcol
except ImportError as e:
    raise ImportError("rasterio is required for cpano.sampling. Please install rasterio.") from e


Method = Literal["nearest", "bilinear"]


@dataclass(frozen=True)
class RayBundle:
    """
    X, Y, Z: (M, n)
    r: (n,)
    theta: (M,)
    """
    X: np.ndarray
    Y: np.ndarray
    Z: np.ndarray
    r: np.ndarray
    theta: np.ndarray


def _is_north_up(transform: Affine) -> bool:
    return (transform.b == 0.0) and (transform.d == 0.0)


def world_to_pixel_f(transform: Affine, X: np.ndarray, Y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    World -> fractional pixel coordinates for north-up rasters.
    Returns (col_f, row_f) with same shape as X/Y.
    """
    if not _is_north_up(transform):
        raise ValueError("world_to_pixel_f assumes north-up raster (transform.b==transform.d==0).")

    a = transform.a  # pixel width
    e = transform.e  # pixel height (negative for north-up)
    c = transform.c  # x origin
    f = transform.f  # y origin

    col_f = (X - c) / a
    row_f = (Y - f) / e  # e negative -> ok
    return col_f, row_f


def pixel_center_world(transform: Affine, row: np.ndarray, col: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Pixel indices -> world coords of pixel centers.
    row/col can be arrays.
    """
    # center: (col+0.5, row+0.5)
    colc = col.astype(np.float32) + 0.5
    rowc = row.astype(np.float32) + 0.5
    X = transform.a * colc + transform.b * rowc + transform.c
    Y = transform.d * colc + transform.e * rowc + transform.f
    return X, Y


def sample_nearest(
    arr: np.ndarray,
    transform: Affine,
    X: np.ndarray,
    Y: np.ndarray,
    nodata: Optional[float] = None,
    fill_oob: float = np.nan,
) -> np.ndarray:
    """
    Nearest neighbor sampling using rowcol (supports general affine).
    X, Y arrays same shape. Returns float32.
    """
    Z = np.full(X.shape, fill_oob, dtype=np.float32)

    # rowcol works with scalars; vectorization via flatten
    xf = X.ravel()
    yf = Y.ravel()

    rr = np.empty_like(xf, dtype=np.int64)
    cc = np.empty_like(xf, dtype=np.int64)

    # rowcol can take arrays in recent rasterio versions; but to be safe, loop is avoided by try.
    try:
        rr, cc = rowcol(transform, xf, yf)
        rr = np.asarray(rr, dtype=np.int64)
        cc = np.asarray(cc, dtype=np.int64)
    except Exception:
        # fallback: python loop (still okay for small grids)
        for i, (x, y) in enumerate(zip(xf, yf)):
            r, c = rowcol(transform, x, y)
            rr[i] = r
            cc[i] = c

    H, W = arr.shape
    inb = (rr >= 0) & (rr < H) & (cc >= 0) & (cc < W)
    if not np.any(inb):
        return Z

    z = arr[rr[inb], cc[inb]].astype(np.float32, copy=False)

    if nodata is not None and not (isinstance(nodata, float) and np.isnan(nodata)):
        good = z != np.float32(nodata)
        tmp = np.full_like(z, fill_oob, dtype=np.float32)
        tmp[good] = z[good]
        z = tmp

    Z_flat = Z.ravel()
    Z_flat[np.where(inb)[0]] = z
    return Z


def sample_bilinear(
    arr: np.ndarray,
    transform: Affine,
    X: np.ndarray,
    Y: np.ndarray,
    nodata: Optional[float] = None,
    fill_oob: float = np.nan,
) -> np.ndarray:
    """
    Bilinear interpolation for north-up rasters.
    Returns float32 with fill_oob for out-of-bounds or nodata-neighborhood.
    """
    if not _is_north_up(transform):
        raise ValueError("sample_bilinear assumes north-up raster (transform.b==transform.d==0).")

    col_f, row_f = world_to_pixel_f(transform, X, Y)

    c0 = np.floor(col_f).astype(np.int32)
    r0 = np.floor(row_f).astype(np.int32)
    c1 = c0 + 1
    r1 = r0 + 1

    wc = (col_f - c0).astype(np.float32)
    wr = (row_f - r0).astype(np.float32)

    H, W = arr.shape
    valid = (r0 >= 0) & (r1 < H) & (c0 >= 0) & (c1 < W)

    Z = np.full(X.shape, fill_oob, dtype=np.float32)
    if not np.any(valid):
        return Z

    z00 = arr[r0[valid], c0[valid]].astype(np.float32, copy=False)
    z10 = arr[r0[valid], c1[valid]].astype(np.float32, copy=False)
    z01 = arr[r1[valid], c0[valid]].astype(np.float32, copy=False)
    z11 = arr[r1[valid], c1[valid]].astype(np.float32, copy=False)

    # nodata handling: if any neighbor is nodata => fill_oob
    if nodata is not None and not (isinstance(nodata, float) and np.isnan(nodata)):
        nd = np.float32(nodata)
        bad = (z00 == nd) | (z10 == nd) | (z01 == nd) | (z11 == nd)
        if np.any(bad):
            # keep only those not bad
            valid_idx = np.where(valid)
            valid2 = valid.copy()
            valid2[valid_idx[0][bad], valid_idx[1][bad]] = False
            valid = valid2
            if not np.any(valid):
                return Z
            z00 = arr[r0[valid], c0[valid]].astype(np.float32, copy=False)
            z10 = arr[r0[valid], c1[valid]].astype(np.float32, copy=False)
            z01 = arr[r1[valid], c0[valid]].astype(np.float32, copy=False)
            z11 = arr[r1[valid], c1[valid]].astype(np.float32, copy=False)

    wc_v = wc[valid]
    wr_v = wr[valid]

    Z[valid] = (
        (1 - wc_v) * (1 - wr_v) * z00 +
        (wc_v)     * (1 - wr_v) * z10 +
        (1 - wc_v) * (wr_v)     * z01 +
        (wc_v)     * (wr_v)     * z11
    ).astype(np.float32)

    return Z


def sample_points(
    arr: np.ndarray,
    transform: Affine,
    X: np.ndarray,
    Y: np.ndarray,
    *,
    method: Method = "bilinear",
    nodata: Optional[float] = None,
    fill_oob: float = np.nan,
) -> np.ndarray:
    """
    Unified sampler.
    """
    if method == "nearest":
        return sample_nearest(arr, transform, X, Y, nodata=nodata, fill_oob=fill_oob)
    if method == "bilinear":
        return sample_bilinear(arr, transform, X, Y, nodata=nodata, fill_oob=fill_oob)
    raise ValueError(f"Unknown method='{method}'. Use 'nearest' or 'bilinear'.")


def get_z0_nearest(arr: np.ndarray, transform: Affine, x0: float, y0: float) -> float:
    """
    Get Z at a single point using nearest neighbor.
    """
    r, c = rowcol(transform, x0, y0)
    if not (0 <= r < arr.shape[0] and 0 <= c < arr.shape[1]):
        raise ValueError("Point (x0, y0) is outside raster bounds.")
    return float(arr[r, c])


def sample_rays(
    arr: np.ndarray,
    transform: Affine,
    x0: float,
    y0: float,
    *,
    R: float = 100.0,
    M: int = 1000,
    ds: float = 0.5,
    method: Method = "bilinear",
    nodata: Optional[float] = None,
    fill_oob: float = np.nan,
    theta0: float = 0.0,
    clockwise: bool = False,
) -> RayBundle:
    """
    Generate M rays around (x0,y0) up to radius R, sample every ds meters.

    Args:
      R: max radius (meters)
      M: number of directions
      ds: step along ray (meters)
      method: 'nearest' or 'bilinear'
      theta0: starting angle (radians), default 0 (east)
      clockwise: if True, angles go clockwise

    Returns:
      RayBundle(X,Y,Z,r,theta)
    """
    if ds <= 0:
        raise ValueError("ds must be > 0")
    if M <= 0:
        raise ValueError("M must be > 0")
    if R <= 0:
        raise ValueError("R must be > 0")

    n = int(np.floor(R / ds)) + 1
    r = (np.arange(n, dtype=np.float32) * ds).astype(np.float32)

    theta = (np.arange(M, dtype=np.float32) / np.float32(M)) * (2 * np.pi)
    theta = theta + np.float32(theta0)
    if clockwise:
        theta = -theta

    cos_t = np.cos(theta)[:, None].astype(np.float32)
    sin_t = np.sin(theta)[:, None].astype(np.float32)

    X = (x0 + r[None, :] * cos_t).astype(np.float32)
    Y = (y0 + r[None, :] * sin_t).astype(np.float32)

    Z = sample_points(arr, transform, X, Y, method=method, nodata=nodata, fill_oob=fill_oob)

    return RayBundle(X=X, Y=Y, Z=Z, r=r, theta=theta)
