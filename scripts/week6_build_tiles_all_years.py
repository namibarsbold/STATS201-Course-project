#!/usr/bin/env python3
# build_tiles_all_years.py
#
# Build tile-level datasets for ALL years (default 2014–2023) for Morocco/Brazil/China
# when your TIFFs are stored in subfolders like:
#
#   DATA_PATH/
#     Morocco/Morocco_2014.tif ... Morocco_2023.tif
#     Brazil/Brazil_2014.tif   ... Brazil_2023.tif
#     China/China_2014.tif     ... China_2023.tif
#
# Each GeoTIFF must have:
#   Band 1: nightlights (VIIRS radiance)
#   Band 2: population (WorldPop)
#
# Outputs (written to OUT_DIR):
#   tiles_<Country>_<Year>.csv
#   tiles_panel_all_countries_<start>-<end>.csv
#
# Continuity:
#   We choose ONE tile size per country (based on the first available year) and reuse it for all years,
#   so tiles are stable over time.
#   IMPORTANT: tile_id is STABLE across years because it is the enumerate index of the full grid.

import os, glob, re, argparse
import numpy as np
import pandas as pd
import rasterio

REGION_TYPES = ["urban_core", "dense_dim", "bright_sparse", "mixed", "empty_or_rural"]


def read_bands(fp: str):
    with rasterio.open(fp) as src:
        nl = src.read(1).astype("float32")
        pop = src.read(2).astype("float32") if src.count >= 2 else None
        nodata = src.nodata

    if nodata is not None:
        nl = np.where(nl == nodata, np.nan, nl)
        if pop is not None:
            pop = np.where(pop == nodata, np.nan, pop)

    return nl, pop


def choose_tile_size(h: int, w: int, country: str) -> int:
    # Big countries -> fewer tiles along the short edge (avoid huge runtimes)
    target_tiles_short = 60 if country.lower() in ["brazil", "china"] else 80
    short = min(h, w)
    tile = max(256, int(short / target_tiles_short))

    for nice in [256, 320, 384, 448, 512, 640, 768, 896, 1024]:
        if tile <= nice:
            return nice
    return 1024


def make_tiles(h: int, w: int, tile: int):
    tiles = []
    for r0 in range(0, h, tile):
        r1 = min(h, r0 + tile)
        for c0 in range(0, w, tile):
            c1 = min(w, c0 + tile)
            tiles.append((r0, r1, c0, c1))
    return tiles


def classify(mean_nl: float, mean_pop: float, nl_q, pop_q) -> str:
    # Quantiles computed per country-year
    if not np.isfinite(mean_pop) or mean_pop <= pop_q[0]:
        return "empty_or_rural"

    hi_pop = mean_pop >= pop_q[2]
    hi_nl = mean_nl >= nl_q[2]
    lo_nl = mean_nl <= nl_q[0]

    if hi_pop and hi_nl:
        return "urban_core"
    if hi_pop and lo_nl:
        return "dense_dim"
    if (not hi_pop) and hi_nl:
        return "bright_sparse"
    return "mixed"


def find_years(data_path: str, country: str):
    # Look inside DATA_PATH/<Country>/<Country>_YYYY.tif
    country_folder = os.path.join(data_path, country)
    pat = os.path.join(country_folder, f"{country}_*.tif")

    years = []
    for fp in glob.glob(pat):
        m = re.search(r"_(\d{4})\.tif$", os.path.basename(fp))
        if m:
            years.append(int(m.group(1)))

    return sorted(set(years))


def build_tile_table(country: str, year: int, fp: str, tiles, min_valid: int = 500):
    nl, pop = read_bands(fp)
    if pop is None:
        raise ValueError(f"{fp} is missing population band (band 2).")

    h, w = nl.shape
    valid = np.isfinite(nl) & np.isfinite(pop) & (nl >= 0) & (pop >= 0)

    rows = []

    # IMPORTANT: stable tile_id comes from enumerate(tiles)
    for idx, (r0, r1, c0, c1) in enumerate(tiles, start=1):
        # Clip in case dimensions differ slightly year-to-year
        rr0 = min(r0, h)
        rr1 = min(r1, h)
        cc0 = min(c0, w)
        cc1 = min(c1, w)

        if rr0 >= rr1 or cc0 >= cc1:
            continue

        m = valid[rr0:rr1, cc0:cc1]
        n = int(m.sum())
        if n < min_valid:
            continue

        nl_block = nl[rr0:rr1, cc0:cc1][m]
        pop_block = pop[rr0:rr1, cc0:cc1][m]

        rows.append({
            "country": country,
            "year": year,
            "tile_id": idx,  # <-- stable across years
            "r0": rr0, "r1": rr1, "c0": cc0, "c1": cc1,
            "n_valid_pixels": n,
            "mean_light": float(np.nanmean(nl_block)),
            "mean_pop": float(np.nanmean(pop_block)),
        })

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError(
            f"No tiles produced for {country} {year}. "
            f"Try lowering --min_valid (currently {min_valid})."
        )

    # Compute quantiles on produced tiles for this country-year
    nl_q = np.nanquantile(df["mean_light"].values, [0.25, 0.5, 0.75])
    pop_q = np.nanquantile(df["mean_pop"].values, [0.25, 0.5, 0.75])

    df["region_type"] = [classify(a, b, nl_q, pop_q) for a, b in zip(df["mean_light"], df["mean_pop"])]
    df["log_light"] = np.log1p(df["mean_light"].clip(lower=0))
    df["log_pop"] = np.log1p(df["mean_pop"].clip(lower=0))
    df["region_type"] = pd.Categorical(df["region_type"], categories=REGION_TYPES, ordered=True)

    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_path", required=True, help="Root folder containing subfolders: Morocco/, Brazil/, China/")
    ap.add_argument("--out_dir", default=None, help="Output folder (default: <data_path>/outputs_tiles)")
    ap.add_argument("--countries", default="Morocco,Brazil,China", help="Comma-separated list")
    ap.add_argument("--start_year", type=int, default=2014)
    ap.add_argument("--end_year", type=int, default=2023)
    ap.add_argument("--min_valid", type=int, default=500, help="Minimum valid pixels per tile (default 500)")
    args = ap.parse_args()

    data_path = args.data_path
    out_dir = args.out_dir or os.path.join(data_path, "outputs_tiles")
    os.makedirs(out_dir, exist_ok=True)

    countries = [c.strip() for c in args.countries.split(",") if c.strip()]
    panel_parts = []

    for country in countries:
        available = find_years(data_path, country)
        use_years = [y for y in available if args.start_year <= y <= args.end_year]
        if not use_years:
            print(f"[WARN] No years found for {country} in range {args.start_year}-{args.end_year}")
            continue

        # Reference year defines the stable tile grid for this country
        ref_year = use_years[0]
        ref_fp = os.path.join(data_path, country, f"{country}_{ref_year}.tif")
        if not os.path.exists(ref_fp):
            print(f"[WARN] Missing reference file: {ref_fp}")
            continue

        nl_ref, _ = read_bands(ref_fp)
        h_ref, w_ref = nl_ref.shape
        tile_size = choose_tile_size(h_ref, w_ref, country)
        tiles = make_tiles(h_ref, w_ref, tile_size)

        print(f"{country}: ref_year={ref_year}, shape={h_ref}x{w_ref}, tile_size={tile_size}, tiles_total={len(tiles)}")

        for year in use_years:
            fp = os.path.join(data_path, country, f"{country}_{year}.tif")
            if not os.path.exists(fp):
                print(f"[WARN] missing {fp}")
                continue

            df = build_tile_table(country, year, fp, tiles, min_valid=args.min_valid)
            out_csv = os.path.join(out_dir, f"tiles_{country}_{year}.csv")
            df.to_csv(out_csv, index=False)
            panel_parts.append(df)

            print(f"  {year}: n_tiles={len(df)} -> {os.path.basename(out_csv)}")

    if panel_parts:
        panel = pd.concat(panel_parts, ignore_index=True)
        panel_path = os.path.join(out_dir, f"tiles_panel_all_countries_{args.start_year}-{args.end_year}.csv")
        panel.to_csv(panel_path, index=False)
        print("\nSaved panel:", panel_path)
    else:
        print("No tiles produced. Check that file names match <Country>_<Year>.tif inside each country folder.")


if __name__ == "__main__":
    main()