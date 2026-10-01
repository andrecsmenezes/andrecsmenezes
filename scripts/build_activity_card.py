#!/usr/bin/env python3
from __future__ import annotations

import html as html_lib
import re
import urllib.request
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

USERNAME = "andrecsmenezes"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated"
URL = f"https://github.com/users/{USERNAME}/contributions"

CELL_RE = re.compile(r"<td[^>]*class=\"[^\"]*ContributionCalendar-day[^\"]*\"[^>]*>", re.I)
ATTR_RE = re.compile(r'(?:^|\\s)([\\w:-]+)=\"([^\"]*)\"')
TOOLTIP_RE = re.compile(
    r'<tool-tip[^>]*for=\"([^\"]+)\"[^>]*>\\s*([\\d,]+)\\s+contribution',
    re.I,
)

def fetch() -> str:
    req = urllib.request.Request(
        URL,
        headers={
            "User-Agent": "andrecsmenezes-profile/1.0",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")

def parse(source: str):
    tooltips = {
        element_id: int(count.replace(",", ""))
        for element_id, count in TOOLTIP_RE.findall(source)
    }

    days = []
    unresolved_active = []
    for tag in CELL_RE.findall(source):
        attrs = dict(ATTR_RE.findall(tag))
        day = attrs.get("data-date")
        level = int(attrs.get("data-level", "0"))
        element_id = attrs.get("id")
        if not day:
            continue

        count = tooltips.get(element_id, 0)
        if level > 0 and element_id not in tooltips:
            unresolved_active.append(day)
        days.append((datetime.strptime(day, "%Y-%m-%d").date(), count))

    if len(days) < 300:
        print("DEBUG source head:", source[:4000])
        raise RuntimeError(f"Contribution parser returned only {len(days)} days")
    if unresolved_active:
        raise RuntimeError(
            "Could not resolve exact counts for active days: "
            + ", ".join(unresolved_active[:5])
        )

    days.sort(key=lambda item: item[0])
    return days

def longest_streak(days):
    longest = 0
    current = 0
    previous = None
    for day, count in days:
        if count > 0 and (previous is None or (day - previous).days == 1):
            current += 1
        elif count > 0:
            current = 1
        else:
            current = 0
        longest = max(longest, current)
        previous = day
    return longest

def weekly_totals(days):
    totals = defaultdict(int)
    for day, count in days:
        year, week, _ = day.isocalendar()
        totals[(year, week)] += count
    keys = sorted(totals)[-52:]
    return [totals[key] for key in keys]

def fmt_int(value: int) -> str:
    return f"{value:,}"

def esc(value: str) -> str:
    return html_lib.escape(value, quote=True)

def render(mode: str, days) -> str:
    dark = mode == "dark"
    bg = "#171418" if dark else "#fdf9ee"
    panel = "#211b20" if dark else "#fffdf8"
    ink = "#fffdf8" if dark else "#171418"
    muted = "#c9bec1" if dark else "#625b5b"
    line = "#ffffff" if dark else "#171418"

    total = sum(count for _, count in days)
    active = sum(1 for _, count in days if count > 0)
    streak = longest_streak(days)
    best_day_count = max((count for _, count in days), default=0)
    weeks = weekly_totals(days)
    peak = max(weeks) if weeks else 1

    metrics = [
        ("CONTRIBUTIONS", fmt_int(total)),
        ("ACTIVE DAYS", fmt_int(active)),
        ("LONGEST STREAK", f"{streak} days"),
        ("BUSIEST DAY", fmt_int(best_day_count)),
    ]

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300" role="img" aria-label="GitHub contribution metrics">',
        '<defs>',
        '  <linearGradient id="brand" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#f68543"/><stop offset=".42" stop-color="#f6535f"/><stop offset=".72" stop-color="#ef1f63"/><stop offset="1" stop-color="#9d1348"/></linearGradient>',
        '</defs>',
        f'<rect width="1200" height="300" rx="30" fill="{bg}"/>',
        f'<rect x="1" y="1" width="1198" height="298" rx="29" fill="none" stroke="{line}" stroke-opacity=".09"/>',
        f'<text x="48" y="52" fill="{muted}" font-family="Inter,system-ui,-apple-system,Segoe UI,sans-serif" font-size="15" font-weight="650" letter-spacing="1.6">LAST 12 MONTHS ON GITHUB</text>',
        f'<text x="48" y="86" fill="{ink}" font-family="Inter,system-ui,-apple-system,Segoe UI,sans-serif" font-size="24" font-weight="720">Work you can see. Private repository names stay private.</text>',
    ]

    x_positions = [48, 330, 612, 894]
    for (label, value), x in zip(metrics, x_positions):
        parts.append(f'<rect x="{x}" y="112" width="250" height="88" rx="20" fill="{panel}" stroke="{line}" stroke-opacity=".08"/>')
        parts.append(f'<text x="{x+20}" y="143" fill="{muted}" font-family="Inter,system-ui,-apple-system,Segoe UI,sans-serif" font-size="12" font-weight="650" letter-spacing="1.25">{esc(label)}</text>')
        parts.append(f'<text x="{x+20}" y="181" fill="{ink}" font-family="Inter,system-ui,-apple-system,Segoe UI,sans-serif" font-size="29" font-weight="760">{esc(value)}</text>')

    base_y = 264
    start_x = 48
    gap = 4
    bar_w = 17
    for i, value in enumerate(weeks):
        max_h = 42
        height = 3 if peak == 0 else max(3, round(max_h * value / peak))
        x = start_x + i * (bar_w + gap)
        y = base_y - height
        opacity = 0.22 + (0.78 * value / peak if peak else 0)
        parts.append(
            f'<rect x="{x}" y="{base_y}" width="{bar_w}" height="0" rx="4" fill="url(#brand)" opacity="{opacity:.2f}">'
            f'<animate attributeName="y" from="{base_y}" to="{y}" dur=".7s" begin="{i*0.012:.3f}s" fill="freeze"/>'
            f'<animate attributeName="height" from="0" to="{height}" dur=".7s" begin="{i*0.012:.3f}s" fill="freeze"/>'
            '</rect>'
        )

    parts.append(f'<text x="1148" y="281" text-anchor="end" fill="{muted}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">updated automatically</text>')
    parts.append('</svg>')
    return "\n".join(parts) + "\n"

def main():
    source = fetch()
    days = parse(source)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "activity-light.svg").write_text(render("light", days), encoding="utf-8")
    (OUT / "activity-dark.svg").write_text(render("dark", days), encoding="utf-8")
    print(
        "activity-card:",
        f"days={len(days)}",
        f"total={sum(c for _, c in days)}",
        f"active={sum(1 for _, c in days if c > 0)}",
    )

if __name__ == "__main__":
    main()
