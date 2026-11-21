"""run_selftest.py: proves each qa/scripts/*.py catches a planted defect and raises nothing on a sound input.

Usage (from the project root):
    python qa/tests/run_selftest.py [--scratch <dir for the throw-away git repo>] [--skip-build]

Everything it writes goes to qa/tmp/planted/ (scratch, never committed) and to --scratch (a throw-away git repo
for the id_scan history test; it is NOT the project repository). It builds small LuaLaTeX documents with the
project fonts, runs every script on a sound and on a planted input, and prints a result table.
Exit code 0 = every expectation held.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap

ROOT = os.getcwd()
SCRIPTS = os.path.join("qa", "scripts")
FAKE9 = "".join(["000", "000", "000"])  # fake ID pattern built at run time: no nine-digit literal in the repository
FAKEG = "-".join(["000"] * 3)
PL = os.path.join("qa", "tmp", "planted")

PRE = r"""\documentclass[a4paper,11pt]{article}
\usepackage[english,bidi=basic]{babel}
\babelprovide[import,main]{english}
\babelprovide[import,onchar=ids fonts]{hebrew}
\usepackage{fontspec}
\defaultfontfeatures{Path=../../../fonts/,Extension=.ttf}
\setmainfont{Rubik-Regular}[BoldFont=Rubik-Bold,ItalicFont=Rubik-Italic,BoldItalicFont=Rubik-BoldItalic]
\babelfont{rm}{Rubik-Regular}[BoldFont=Rubik-Bold,ItalicFont=Rubik-Italic,BoldItalicFont=Rubik-BoldItalic]
\newfontfamily\headfont{PlayfairDisplay-Regular}[BoldFont=PlayfairDisplay-Bold]
\newfontfamily\codefont{JetBrainsMono-Regular}
\usepackage[a4paper,top=3.6cm,bottom=3cm,left=3cm,right=3cm]{geometry}
\pagestyle{empty}
\begin{document}
"""
FILL = ("Fashion e-commerce loses margin on returns because shoppers cannot judge fit before they buy. "
        "A reliable size recommendation lowers fit-related returns and raises customer satisfaction. ") * 5
HEB_GOOD = (r"חברת ClosetTwin מציעה פתרון AI לחנויות B2B באינטרנט. גודל השוק: TAM בסך \$8.5B, SAM בסך \$330M "
            r"ו-SOM בסך \$20M (הנחה) עד שנת 2026. שיעור ההחזרות הוא 24.5\% ואנו מצפים להפחתה של 15\% בתוך 3 years. "
            r"הפתרון שלנו נקרא ClosetTwin.")
HEB_BAD = (r"חברת niwTtesolC מציעה פתרון לחנויות באינטרנט. שיעור ההחזרות %30 עד שנת 6202. "
           r"עוד מלל בעברית כדי להגיע לכמות אותיות מספקת בעמוד הזה.")

results = []


def sh(args, cwd=None, timeout=300):
    p = subprocess.run(args, cwd=cwd, capture_output=True, timeout=timeout)
    return p.returncode, p.stdout.decode("utf-8", errors="replace") + p.stderr.decode("utf-8", errors="replace")


def build(name, body, passes=1):
    path = os.path.join(PL, name + ".tex")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(PRE + body + "\n\\end{document}\n")
    for _ in range(passes):
        sh(["lualatex", "--disable-installer", "-interaction=nonstopmode", name + ".tex"], cwd=PL)
    return os.path.join(PL, name)


def script(name, *args):
    return sh([sys.executable, os.path.join(SCRIPTS, name), *args])


def expect(label, out_rc, must=(), must_not=(), rc=None):
    out, code = out_rc[1], out_rc[0]
    ok = True
    why = []
    for m in must:
        if not re.search(m, out):
            ok = False
            why.append("missing: " + m)
    for m in must_not:
        if re.search(m, out):
            ok = False
            why.append("unexpected: " + m)
    if rc is not None and code != rc:
        ok = False
        why.append("exit %d, wanted %d" % (code, rc))
    results.append((label, ok, "; ".join(why)))
    print("%-4s %s %s" % ("PASS" if ok else "FAIL", label, ("(" + "; ".join(why) + ")") if why else ""))
    if not ok:
        print(textwrap.indent(out[-1500:], "     | "))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", default=tempfile.gettempdir())
    ap.add_argument("--skip-build", action="store_true")
    a = ap.parse_args()
    os.makedirs(PL, exist_ok=True)

    # ---------------------------------------------------------------- documents
    if not a.skip_build:
        build("good_heb", FILL + "\n\\newpage\n\\begin{otherlanguage}{hebrew}\n{\\bfseries\\Large תקציר מנהלים}\\par\n" + HEB_GOOD + "\n\\end{otherlanguage}\n")
        build("bad_heb", FILL + "\n\\newpage\n\\begin{otherlanguage}{hebrew}\n{\\headfont\\bfseries\\Large תקציר מנהלים}\\par\n" + HEB_BAD
              + "\n\\end{otherlanguage}\n\\newpage\n\\begin{otherlanguage}{hebrew}\n" + HEB_BAD + "\n\\end{otherlanguage}\n")
        build("good_layout", "\n".join("{\\headfont\\bfseries\\Large Section %d}\\par\\medskip\n%s\n%s\\newpage" % (i, FILL, FILL) for i in range(1, 4)))
        build("bad_layout",
              FILL + "\\par\\texttt{monospace text in Latin Modern Mono}\\newpage\n"
              + FILL + "\\par\\vspace*{\\fill}{\\headfont\\Huge Orphan Heading}\\par\\newpage\n"
              + "Almost nothing.\\newpage\n"
              + "\\noindent\\mbox{" + "W" * 70 + "}\\par\\noindent\\hbox to 10cm{a b}\\par\n\\newpage\n"
              + "{\\codefont print('hello')}\\par " + FILL)
        build("idpdf", FILL + "\\par Reference number " + FAKE9 + " appears here.")
        build("chap30", "\n".join("{\\headfont\\bfseries\\Large Chapter page %d}\\par\\medskip\n%s\n%s\n%s\\newpage" % (i, FILL, FILL, FILL) for i in range(1, 31)))

    # ---------------------------------------------------------------- hebrew_pages / bidi_bbox_check
    g, b = os.path.join(PL, "good_heb"), os.path.join(PL, "bad_heb")
    expect("hebrew_pages: sound page -> no finding", script("hebrew_pages.py", g + ".pdf", "--log", g + ".log", "--front", "2"),
           must=[r"findings=0"], must_not=[r"### F-"], rc=0)
    expect("hebrew_pages: planted 2nd Hebrew page + Playfair heading -> B1, B6, B9", script("hebrew_pages.py", b + ".pdf", "--log", b + ".log", "--front", "2"),
           must=[r"B1\b", r"B9\b", r"B8\b|expected exactly 1"], rc=1)
    expect("bidi_bbox_check: sound corpus -> no finding", script("bidi_bbox_check.py", g + ".pdf", "--page", "2"),
           must=[r"findings=0"], must_not=[r"### F-"], rc=0)
    expect("bidi_bbox_check: planted reversed 'niwTtesolC', '6202', '%30' -> B3", script("bidi_bbox_check.py", b + ".pdf", "--page", "2"),
           must=[r"reversed run 'niwTtesolC'", r"reversed run '6202'", r"number/unit order error"], rc=1)

    # ---------------------------------------------------------------- fonts_by_page
    gl, bl = os.path.join(PL, "good_layout"), os.path.join(PL, "bad_layout")
    expect("fonts_by_page: sound document (Playfair+Rubik) -> no finding", script("fonts_by_page.py", gl + ".pdf", "--formula-pages", "99", "--code-pages", "99"),
           must=[r"findings=0"], rc=0)
    expect("fonts_by_page: planted mono font + JetBrains off the code page -> K3", script("fonts_by_page.py", bl + ".pdf", "--formula-pages", "99", "--code-pages", "99"),
           must=[r"K3\b", r"LMMono|Mono"], rc=1)
    t5 = os.path.join("fix", "tests", "t5.pdf")
    if os.path.exists(t5):
        expect("fonts_by_page: planted LM Math on a non-formula page (t5, formula only on p.1) -> D11",
               script("fonts_by_page.py", t5, "--formula-pages", "1", "--code-pages", "3"), must=[r"D11\b"], rc=1)
    # figure PDFs: matplotlib default (Type 3 + DejaVu) vs fonttype 42 + Rubik
    sh([sys.executable, "-c", textwrap.dedent("""
        import matplotlib; matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib import font_manager as fm
        plt.plot([1,2,3]); plt.title('Bad figure'); plt.savefig(r'%s/fig_bad.pdf'); plt.close()
        fm.fontManager.addfont(r'fonts/Rubik-Regular.ttf')
        plt.rcParams.update({'pdf.fonttype': 42, 'font.family': 'Rubik'})
        plt.plot([1,2,3]); plt.title('Good figure'); plt.savefig(r'%s/fig_good.pdf'); plt.close()
    """ % (PL.replace("\\", "/"), PL.replace("\\", "/")))])
    expect("fonts_by_page: sound figure (Rubik, fonttype 42) -> no finding", script("fonts_by_page.py", gl + ".pdf", "--figures", os.path.join(PL, "fig_good.pdf")),
           must=[r"findings=0"], rc=0)
    expect("fonts_by_page: planted figure (DejaVu, Type 3) -> I8", script("fonts_by_page.py", gl + ".pdf", "--figures", os.path.join(PL, "fig_bad.pdf")),
           must=[r"I8\b"], rc=1)

    # ---------------------------------------------------------------- overfull / page_stats / bbox_margin
    expect("overfull: sound log -> no finding", script("overfull.py", gl + ".log"), must=[r"findings=0"], rc=0)
    expect("overfull: planted 70-letter word + underfull box -> BU5, BU6", script("overfull.py", bl + ".log"), must=[r"BU5\b", r"BU6\b"], rc=1)
    expect("page_stats: sound document -> no L2/L4", script("page_stats.py", gl + ".pdf", "--min-total", "2"),
           must_not=[r"L2\b", r"L4\b"], rc=0)
    expect("page_stats: planted orphan heading (p.2) and near-empty page (p.3) -> L2, L4", script("page_stats.py", bl + ".pdf", "--min-total", "2"),
           must=[r"L2\b", r"PDF page 2", r"L4\b", r"PDF page 3"], rc=1)
    toc = os.path.join(PL, "chap30.toc")
    firsts = [1, 4, 8, 11, 17, 20, 22, 24, 27, 29]   # ch4 gets 6 pages (budget 4), ch10 gets 2 (exactly 1 wanted)
    with open(toc, "w", encoding="utf-8") as fh:
        for i, p in enumerate(firsts, 1):
            fh.write("\\contentsline {chapter}{\\numberline {%d}Chapter %d}{%d}{chapter.%d}%%\n" % (i, i, p, i))
    expect("page_stats: planted budget breach (ch.4 = 6 pages, ch.10 = 2) -> D17 x2, D1 passes at 30", script("page_stats.py", os.path.join(PL, "chap30.pdf"), "--toc", toc),
           must=[r"chapter 4 has 6 page", r"chapter 10 has 2 page"], must_not=[r"### F-typeset-\d+  \[blocker\]  D1"], rc=1)
    expect("page_stats: planted content total below 25 (--min-total 31) -> D1", script("page_stats.py", os.path.join(PL, "chap30.pdf"), "--toc", toc, "--min-total", "31"),
           must=[r"D1\b"], rc=1)
    expect("bbox_margin: sound document -> no finding", script("bbox_margin.py", gl + ".pdf"), must=[r"findings=0"], rc=0)
    expect("bbox_margin: planted text running into the margin (p.4) -> L9", script("bbox_margin.py", bl + ".pdf"), must=[r"L9\b", r"PDF page 4"], rc=1)

    # ---------------------------------------------------------------- label_refs / table_sums
    src = os.path.join(PL, "labels.tex")
    with open(src, "w", encoding="utf-8") as fh:
        fh.write(textwrap.dedent(r"""
            See Table~\ref{tab:good} and Figure~\ref{fig:missing}.
            \begin{table}\caption{Good}\label{tab:good}\begin{tabular}{lr}a&1\\\end{tabular}\end{table}
            \begin{table}\begin{tabular}{lr}b&2\\\end{tabular}\caption{Caption below}\label{tab:below}\end{table}
            \begin{figure}\includegraphics{x}\end{figure}
            \begin{equation}\label{eq:one}a=b\end{equation}
        """))
    expect("label_refs tab: planted caption below + unreferenced label -> TB2", script("label_refs.py", "tab", "--src", src),
           must=[r"caption is below", r"never referenced"], rc=1)
    expect("label_refs fig: planted figure without caption/label + undefined ref -> I3", script("label_refs.py", "fig", "--src", src),
           must=[r"without", r"does not exist"], rc=1)
    good_src = os.path.join(PL, "labels_ok.tex")
    with open(good_src, "w", encoding="utf-8") as fh:
        fh.write(r"Table~\ref{tab:a}. \begin{table}\caption{A}\label{tab:a}\begin{tabular}{lr}x&1\\\end{tabular}\end{table}")
    expect("label_refs tab: sound source -> no finding", script("label_refs.py", "tab", "--src", good_src), must=[r"findings=0"], rc=0)
    tt = os.path.join(PL, "totals.tex")
    with open(tt, "w", encoding="utf-8") as fh:
        fh.write(textwrap.dedent(r"""
            \begin{tabular}{lrr}\toprule Item & A & B\\\midrule
            x & 10 & \usd{1,200}\\ y & 20.5 & 800\\ \midrule Total & 30.5 & \usd{2,100}\\\bottomrule\end{tabular}
        """))
    expect("table_sums: planted wrong total (col B should be 2,000) -> TB5", script("table_sums.py", tt), must=[r"TB5\b", r"column 3"], must_not=[r"column 2"], rc=1)
    tt_ok = os.path.join(PL, "totals_ok.tex")
    with open(tt_ok, "w", encoding="utf-8") as fh:
        fh.write(open(tt, encoding="utf-8").read().replace("2,100", "2,000"))
    expect("table_sums: sound totals -> no finding", script("table_sums.py", tt_ok), must=[r"findings=0"], rc=0)

    # ---------------------------------------------------------------- contrast_colors (PIL-made pages)
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype("fonts/Rubik-Regular.ttf", 15)
    big = ImageFont.truetype("fonts/Rubik-Regular.ttf", 70)

    def page(name, bg, items):
        im = Image.new("RGB", (827, 1169), bg)
        d = ImageDraw.Draw(im)
        for xy, txt, col, f in items:
            d.text(xy, txt, fill=col, font=f)
        p = os.path.join(PL, name + ".png")
        im.save(p)
        return p
    ink, white, ivory = "#111111", "#FFFFFF", "#F7F3EE"
    good_png = page("c_good", white, [((80, 100), "Body text in ink on a white page, 11 pt.", ink, font),
                                      ((80, 200), "Caption label in mocha-deep", "#6B4B3D", font),
                                      ((80, 300), "3", "#A47864", big)])
    bad_png = page("c_bad", ivory, [((80, 100), "Link-blue text like the hyperref default", "#0000EE", font),
                                    ((80, 200), "Small caption label in mocha is 3.85 to 1", "#A47864", font),
                                    ((80, 260), "Small pink text is 1.4 to 1", "#E8C6C0", font)])
    expect("contrast_colors: sound white page (ink, mocha-deep, large mocha) -> no finding", script("contrast_colors.py", good_png), must=[r"findings=0"], rc=0)
    expect("contrast_colors: planted ivory page, blue text, small mocha/pink text -> D19, D6, D18", script("contrast_colors.py", bad_png),
           must=[r"D19\b", r"D6\b", r"D18\b"], rc=1)
    expect("contrast_colors: --pairs mocha-deep on white passes, mocha on white fails", script("contrast_colors.py", good_png, "--pairs", "6B4B3D/FFFFFF=4.5,A47864/FFFFFF=4.5"),
           must=[r"A47864 on FFFFFF is 3\.\d\d:1"], must_not=[r"6B4B3D on FFFFFF is"], rc=1)
    expect("contrast_colors: --figure series ink vs mocha-deep (gap < 20%) -> I12", script("contrast_colors.py", good_png, "--figure", "--series", "111111,6B4B3D,A47864"),
           must=[r"I12\b"], rc=1)

    # ---------------------------------------------------------------- code_diff
    src_py = os.path.join("python", "fig_f6_retailer_economics.py")
    if os.path.exists(src_py):
        lines = [l for l in open(src_py, encoding="utf-8").read().splitlines() if l.strip()][:14]
        good_txt = os.path.join(PL, "code_good.txt")
        bad_txt = os.path.join(PL, "code_bad.txt")
        with open(good_txt, "w", encoding="utf-8") as fh:
            fh.write("Appendix A. How our charts are made\n\n" + "\n".join("%3d  %s" % (i, l) for i, l in enumerate(lines, 1)) + "\n\nThe script is read from its file.\n")
        changed = list(lines)
        changed[6] = changed[6] + "  # EDITED BY HAND"
        changed[9] = "x_hand_pasted = 1"
        with open(bad_txt, "w", encoding="utf-8") as fh:
            fh.write("Appendix A. How our charts are made\n\n" + "\n".join("%3d  %s" % (i, l) for i, l in enumerate(changed, 1)) + "\n")
        expect("code_diff: sound box (verbatim lines) -> no finding", script("code_diff.py", good_txt, src_py), must=[r"findings=0"], rc=0)
        expect("code_diff: planted edited and pasted lines -> K4", script("code_diff.py", bad_txt, src_py), must=[r"K4\b", r"differ from"], rc=1)
        unrelated = os.path.join(PL, "code_other.txt")
        with open(unrelated, "w", encoding="utf-8") as fh:
            fh.write("for i in range(3):\n    print('not the real script')\n")
        expect("code_diff: planted box that shows another script -> K4", script("code_diff.py", unrelated, src_py), must=[r"does not show"], rc=1)
    else:
        results.append(("code_diff", False, "python/fig_f6_retailer_economics.py not found"))

    # ---------------------------------------------------------------- bib_vs_cited
    keys = ["k%02d" % i for i in range(1, 13)]
    bib_ok = os.path.join(PL, "ok.bib")
    bcf_ok = os.path.join(PL, "ok.bcf")
    with open(bib_ok, "w", encoding="utf-8") as fh:
        for k in keys:
            fh.write("@article{%s, author={A, B}, title={T %s}, journal={J}, year={2024}, pages={1--9}, doi={10.1000/%s}}\n" % (k, k, k))
    with open(bcf_ok, "w", encoding="utf-8") as fh:
        fh.write("".join("<bcf:citekey order=\"%d\">%s</bcf:citekey>\n" % (i, k) for i, k in enumerate(keys, 1)))
    expect("bib_vs_cited: sound bib (12 complete, all cited) -> no finding", script("bib_vs_cited.py", bcf_ok, bib_ok), must=[r"findings=0"], rc=0)
    bib_bad = os.path.join(PL, "bad.bib")
    bcf_bad = os.path.join(PL, "bad.bcf")
    with open(bib_bad, "w", encoding="utf-8") as fh:
        fh.write(open(bib_ok, encoding="utf-8").read())
        fh.write("@online{unused2020, author={X, Y}, title={Never cited}, url={https://example.org/x}}\n")
        fh.write("@article{noyear, author={A, B}, title={No year or venue}, doi={10.1/x}}\n")
    with open(bcf_bad, "w", encoding="utf-8") as fh:
        fh.write(open(bcf_ok, encoding="utf-8").read() + "<bcf:citekey order=\"13\">ghost2099</bcf:citekey>\n<bcf:citekey order=\"14\">noyear</bcf:citekey>\n")
    expect("bib_vs_cited: planted missing key, unused entry, no urldate, incomplete entry -> R1, R11, R6",
           script("bib_vs_cited.py", bcf_bad, bib_bad), must=[r"R1\b", r"ghost2099", r"R11\b", r"unused2020", r"no urldate", r"R6\b", r"noyear"], rc=1)

    # ---------------------------------------------------------------- id_scan
    tree = os.path.join(PL, "idtree")
    shutil.rmtree(tree, ignore_errors=True)
    os.makedirs(tree)
    with open(os.path.join(tree, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("Course: Generative AI for Management (875523402)\nlecturer: Dr. Yoram Segal\nsha256 123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0\nprice USD 320000000\n")
    expect("id_scan: sound tree (course code, hash, money) -> no finding", script("id_scan.py", "--root", tree), must=[r"findings=0"], rc=0)
    with open(os.path.join(tree, "team.md"), "w", encoding="utf-8") as fh:
        fh.write("Hila ID: " + FAKE9 + "\nbackup " + FAKEG + "\n")
    expect("id_scan: planted 9-digit and grouped ID in a file -> C6, digits masked", script("id_scan.py", "--root", tree),
           must=[r"C6\b", r"team\.md:1\s+00\*{7}", r"team\.md:2\s+00\*{7}"], must_not=[FAKE9], rc=1)
    os.makedirs(tree + "_none", exist_ok=True)
    expect("id_scan: planted 9-digit number in the PDF text -> C6", script("id_scan.py", "--root", tree + "_none", "--pdf", os.path.join(PL, "idpdf.pdf")),
           must=[r"PDF page 1", r"00\*{7}"], must_not=[FAKE9], rc=1)
    repo = os.path.join(a.scratch, "qa_idscan_history_repo")
    shutil.rmtree(repo, ignore_errors=True)
    os.makedirs(repo)
    g = lambda *args: sh(["git", "-C", repo, "-c", "user.name=qa-selftest", "-c", "user.email=qa@example.invalid", *args])
    g("init", "-q")
    with open(os.path.join(repo, "notes.md"), "w", encoding="utf-8") as fh:
        fh.write("student " + FAKE9 + "\n")
    g("add", "notes.md")
    g("commit", "-q", "-m", "add")
    with open(os.path.join(repo, "notes.md"), "w", encoding="utf-8") as fh:
        fh.write("cleaned\n")
    g("commit", "-q", "-am", "remove")
    expect("id_scan: ID deleted from the tree but still in git history -> clean tree, C6 from --history",
           script("id_scan.py", "--root", repo, "--history"), must=[r"git HISTORY", r"commit [0-9a-f]+ notes\.md\s+00\*{7}"], must_not=[r"repository files", FAKE9], rc=1)
    shutil.rmtree(repo, ignore_errors=True)

    # ---------------------------------------------------------------- summary
    bad = [r for r in results if not r[1]]
    print("\n%d expectation(s), %d passed, %d failed" % (len(results), len(results) - len(bad), len(bad)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
