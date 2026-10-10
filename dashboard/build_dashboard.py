"""Build the public dashboard, docs/index.html, from the analysis results.

Run from the project root after rerunning notebooks/02_analysis.ipynb:

    .venv/bin/python dashboard/build_dashboard.py

The notebook saves small aggregated results to reports/dashboard_data.json. This script
writes the headline numbers and one-sentence findings into dashboard/template.html, so
they read correctly even without JavaScript, and embeds the same JSON so the page can
draw its charts and tables in the browser. The full dataset never goes into the page.
"""
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "reports" / "dashboard_data.json"
TEMPLATE_PATH = ROOT / "dashboard" / "template.html"
OUTPUT_DIR = ROOT / "docs"
REPO_URL = "https://github.com/NotKornFlakes/hhs-breach-analysis"

# How each breach type and location reads inside a sentence
PHRASES = {
    ("Type", "Hacking/IT incident"): "hacking",
    ("Type", "Theft"): "theft",
    ("Type", "Loss"): "loss",
    ("Type", "Unauthorized access/disclosure"): "unauthorized access",
    ("Type", "Improper disposal"): "improper disposal",
    ("Type", "Other"): "other breach types",
    ("Type", "Unknown"): "unknown breach types",
    ("Location", "Network server"): "network servers",
    ("Location", "Email"): "email",
    ("Location", "Paper/films"): "paper records",
    ("Location", "Laptop"): "laptops",
    ("Location", "Electronic medical record"): "electronic medical records",
    ("Location", "Other"): "other locations",
    ("Location", "Desktop computer"): "desktop computers",
    ("Location", "Other portable device"): "portable devices",
}


def ordinal(n):
    return f"{n}{'th' if 11 <= n % 100 <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def change(old, new, show):
    """'rose from 23% to 35%' or 'fell from 38% to 33%'."""
    if show(old) == show(new):
        return f"stayed at {show(new)}"
    return f"{'rose' if new > old else 'fell'} from {show(old)} to {show(new)}"


def long_date(iso):
    day = date.fromisoformat(iso)
    return f"{day:%B} {day.day}, {day.year}"


def build_text(data):
    """Headline numbers and one-sentence findings, keyed by their [[PLACEHOLDER]] in the template."""
    meta, trend, cause, vendors = data["meta"], data["trend"], data["cause"], data["vendors"]
    locations, states = data["locations"], data["states"]
    whole = lambda x: f"{x:,.0f}"
    pct = lambda x: f"{x:.0f}%"
    millions = lambda x: f"{x:.1f} million"
    period = lambda name: name.replace("-", "–")

    first_year, last_year = trend["years"][0], trend["years"][-1]
    first_day, last_day = date.fromisoformat(meta["first_date"]), date.fromisoformat(meta["last_date"])
    hacking = cause["share"]["Hacking/IT incident"]
    early, recent = list(vendors["pooled"])  # e.g. "2010-2014", "2021-2025"
    early_shares, recent_shares = vendors["pooled"][early], vendors["pooled"][recent]

    most = 0  # locations are sorted by number of breaches
    largest = max(range(len(locations["names"])), key=lambda i: locations["median_all"][i])
    if most == largest:
        location_finding = (
            f"{locations['names'][most]} breaches were both the most common "
            f"({whole(locations['breaches'][most])}, {pct(locations['share_of_breaches'][most])} of all breaches) "
            f"and the largest, with a median of {whole(locations['median_all'][most])} people affected "
            f"({whole(locations['median_excl_mega'][most])} without mega-breaches)."
        )
    else:
        location_finding = (
            f"{locations['names'][most]} breaches were the most common ({whole(locations['breaches'][most])}), "
            f"while {locations['names'][largest]} breaches were the largest, with a median of "
            f"{whole(locations['median_all'][largest])} people affected."
        )

    vendor_breaches = (early_shares["% of breaches"], recent_shares["% of breaches"])
    vendor_people = (early_shares["% of people (all breaches)"], recent_shares["% of people (all breaches)"])
    vendor_people_excl = (early_shares["% of people (excl. mega-breaches)"],
                          recent_shares["% of people (excl. mega-breaches)"])
    same_direction = (vendor_people[1] > vendor_people[0]) == (vendor_people_excl[1] > vendor_people_excl[0])
    vendor_finding = (
        f"Vendor-related breaches {'rose' if vendor_breaches[1] > vendor_breaches[0] else 'fell'} from "
        f"{pct(vendor_breaches[0])} of all breaches in {period(early)} to {pct(vendor_breaches[1])} in {period(recent)}; "
        f"their share of people affected {change(*vendor_people, pct)}, {'and' if same_direction else 'but'} "
        f"{change(*vendor_people_excl, pct)} without mega-breaches."
    )

    pattern = states["pattern"]
    gaps = [ny - us for ny, us in zip(pattern["new_york"], pattern["all_us"])]
    above, below = gaps.index(max(gaps)), gaps.index(min(gaps))
    phrase = lambda i: PHRASES.get((pattern["group"][i], pattern["labels"][i]), pattern["labels"][i].lower())
    ny = states["new_york"]

    return {
        "SUBTITLE": f"{whole(meta['total_breaches'])} HHS-reported breaches, {first_day.year}–{last_day.year}",
        "REPO_URL": REPO_URL,
        "TOTAL": whole(meta["total_breaches"]),
        "TOTAL_NOTE": f"from {first_day:%b} {first_day.year} to {last_day:%b} {last_day.year}, each affecting 500+ people",
        "MEDIAN": whole(meta["median_people"]),
        "MEAN": whole(meta["mean_people"]),
        "HACKING": pct(hacking[-1]),
        "HACKING_NOTE": (f"of breaches in {last_year} involved hacking, "
                         f"{'up' if hacking[-1] > hacking[0] else 'down'} from {pct(hacking[0])} in {first_year}"),
        "FIRST_YEAR": str(first_year),
        "LAST_YEAR": str(last_year),
        "VENDOR": pct(vendor_breaches[1]),
        "VENDOR_NOTE": (f"of breaches in {period(recent)} involved a vendor (business associate), "
                        f"{'up' if vendor_breaches[1] > vendor_breaches[0] else 'down'} from "
                        f"{pct(vendor_breaches[0])} in {period(early)}"),
        "NY_RANK": ordinal(ny["rank"]),
        "STATE_COUNT": str(len(states["codes"])),
        "NATIONAL_RATE": f"{states['national_rate']:.1f}",
        "MEGA_COUNT": whole(meta["mega_breaches"]),
        "PARTIAL_FIRST": str(first_day.year),
        "PARTIAL_LAST": str(last_day.year),
        "FIRST_DATE": long_date(meta["first_date"]),
        "LAST_DATE": long_date(meta["last_date"]),
        "FINDING_TREND": (
            f"Reported breaches {change(trend['breaches'][0], trend['breaches'][-1], whole)} between {first_year} "
            f"and {last_year}, and the people affected each year "
            f"{change(trend['people_all_m'][0], trend['people_all_m'][-1], millions)} "
            f"({millions(trend['people_excl_mega_m'][0])} to {millions(trend['people_excl_mega_m'][-1])} "
            "without mega-breaches)."
        ),
        "FINDING_CAUSE": (
            f"Hacking overtook theft and loss in {cause['overtake_year']}, and its share of breaches "
            f"{change(hacking[0], hacking[-1], pct)} between {first_year} and {last_year}."
        ),
        "FINDING_VENDORS": vendor_finding,
        "FINDING_LOCATIONS": location_finding,
        "FINDING_STATES": (
            f"New York ranks {ordinal(ny['rank'])} of {len(states['codes'])} with {ny['per_million']:.1f} breaches "
            f"per million residents (all states: {states['national_rate']:.1f}); its breaches involve {phrase(above)} "
            f"more often than the U.S. overall ({pattern['new_york'][above]:.1f}% vs {pattern['all_us'][above]:.1f}%) "
            f"and {phrase(below)} less often ({pattern['new_york'][below]:.1f}% vs {pattern['all_us'][below]:.1f}%)."
        ),
    }


def main():
    data = json.loads(DATA_PATH.read_text())
    page = TEMPLATE_PATH.read_text()
    for key, value in build_text(data).items():
        page = page.replace(f"[[{key}]]", html.escape(value))
    leftover = re.findall(r"\[\[[A-Z_]+\]\]", page)
    assert not leftover, f"Unfilled placeholders: {sorted(set(leftover))}"

    # Compact JSON, with "</" escaped so it can't close the <script> tag early
    embedded = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
    page = page.replace("__DASHBOARD_DATA__", embedded)

    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "index.html").write_text(page)
    (OUTPUT_DIR / ".nojekyll").touch()  # serve the page as-is, without a Jekyll build
    print(f"Wrote {OUTPUT_DIR / 'index.html'} ({len(page.encode()) / 1024:.1f} KB, data {len(embedded) / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
