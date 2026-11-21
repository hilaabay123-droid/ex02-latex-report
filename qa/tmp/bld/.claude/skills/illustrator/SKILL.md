---
name: illustrator
description: Production skill for figures: Python graphs and TikZ diagrams in the project palette, text at least 8 pt, data from the model, captioned, labelled and referenced. Use when creating or changing anything in figures/ or python/.
version: 1.0
---

# illustrator

Rules for art-se when making graphs and diagrams.

## When to use
Creating or changing a Python chart, a TikZ diagram, or the code appendix script.

## Inputs
`python/ct_style.py` (palette, fonts, canvas), `python/model.py` and `python/data/*.csv`, `art/chart-style-guide.md`, PRD 5.3-5.4 (F1-F7), `docs/cls-commands.md` (TikZ keys).

## Procedure
1. One idea per figure; one y-axis; at most 4 series; a title that states the finding.
2. **Python graphs**: import everything visual from `python/ct_style.py`; only the eight palette colours (#111111, #F7F3EE, #A47864, #E8C6C0, #6B4B3D, #D3BBAE, #E3DCD4, #6F6862); Rubik/Playfair text at least 8 pt at print size; fixed canvas equal to the text width (15.0 cm) so it prints 1:1; vector PDF with embedded fonts, no Type 3. Script writes to `figures/`, uses relative paths only, runs with `python python/<name>.py` with no warning on stderr.
3. **Data honesty**: plot only model or sourced values; financial charts say "Assumption"; F5 shows nothing past year 5 and marks the first profitable year and the peak deficit; F6 marks the retailer break-even; F2 axes are two columns of the vendor table; F1 is "not to scale".
4. **TikZ diagrams**: use the `ct ...` keys only, no raw colours, 8 pt text, nodes not overlapping.
5. Series must differ by more than colour: at least 20% luminance gap in grayscale or a direct label; text contrast at least 4.5:1 (3:1 for large text).
6. Each figure: `\caption` below, `\label{fig:...}`, referenced in the text. Do not edit chapters; send writer-se the label and a one-line description.
7. The code appendix script is an ASCII, runnable, line-length-80 file; shown with `\pythonbox{python/<file>.py}`.
8. Render the page at 150 dpi and look before reporting done.

## Outputs
`figures/*.pdf` or `figures/*.tex`, `python/*.py`; reply `DONE` listing file, label and caption text.

## Success check
`qa-img` and `qa-code` would pass: palette, fonts, contrast, 1:1, labels, no stderr, values equal the model.
