"""Shared SVG write + optional PNG export for architecture diagram generators."""
from __future__ import annotations

from pathlib import Path

_CAIROSVG = None
_CAIROSVG_ERROR: str | None = None


def _load_cairosvg():
    global _CAIROSVG, _CAIROSVG_ERROR
    if _CAIROSVG is not None or _CAIROSVG_ERROR is not None:
        return _CAIROSVG
    try:
        import cairosvg

        _CAIROSVG = cairosvg
    except OSError as exc:
        _CAIROSVG_ERROR = str(exc)
        _CAIROSVG = None
    return _CAIROSVG


def write_svg_and_png(out_dir: Path, name: str, svg: str, *, png_width: int = 2400) -> None:
    """Write SVG (always) and PNG when libcairo is available."""
    out_dir.mkdir(parents=True, exist_ok=True)
    svg_path = out_dir / f"{name}.svg"
    png_path = out_dir / f"{name}.png"
    svg_path.write_text(svg, encoding="utf-8")
    print(f"Wrote {svg_path}")

    cairosvg = _load_cairosvg()
    if cairosvg is None:
        print(
            f"SKIP PNG {png_path.name}: libcairo unavailable "
            f"(macOS: brew install cairo · CI: apt install libcairo2)"
        )
        if _CAIROSVG_ERROR:
            print(f"  detail: {_CAIROSVG_ERROR[:120]}...")
        return

    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(png_path), output_width=png_width)
    print(f"Wrote {png_path} ({png_path.stat().st_size} bytes)")
