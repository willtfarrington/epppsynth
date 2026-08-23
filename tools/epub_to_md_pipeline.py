#!/usr/bin/env python3
"""
EPUB -> per-chapter Markdown pipeline for:
  "Existential Psychotherapy" - Irvin D. Yalom (reflowable EPUB)

Implements:
  1. Read reflowable EPUB (already EPUB; no Calibre step needed)
  2. Convert XHTML -> GitHub-Flavored Markdown via pandoc, with custom pre/post processing
  3. Split per chapter; endnotes + footnotes inlined per chapter (self-contained files)
  4. Emit 00_INDEX.md (TOC routing index for agents) + manifest.json

Usage:  python3 epub_to_md_pipeline.py <extracted_epub_OEBPS_dir> <output_dir>
Requires: pandoc, beautifulsoup4, lxml
"""
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

BOOK = "Existential Psychotherapy"
AUTHOR = "Irvin D. Yalom"

# Spine docs to convert, in reading order:
# (source file, output file, type, part label, chapter number, title override)
DOCS = [
    ("introduction.xhtml", "01_ch01_introduction.md",                          "chapter", None,                        1,  "Introduction"),
    ("part001.xhtml",      "02_part-1_death.md",                               "part",    "Part I: Death",             None, "Part I. Death"),
    ("chapter001.xhtml",   "03_ch02_life-death-and-anxiety.md",                "chapter", "Part I: Death",             2,  "Life, Death, and Anxiety"),
    ("chapter002.xhtml",   "04_ch03_the-concept-of-death-in-children.md",      "chapter", "Part I: Death",             3,  "The Concept of Death in Children"),
    ("chapter003.xhtml",   "05_ch04_death-and-psychopathology.md",             "chapter", "Part I: Death",             4,  "Death and Psychopathology"),
    ("chapter004.xhtml",   "06_ch05_death-and-psychotherapy.md",               "chapter", "Part I: Death",             5,  "Death and Psychotherapy"),
    ("part002.xhtml",      "07_part-2_freedom.md",                             "part",    "Part II: Freedom",          None, "Part II. Freedom"),
    ("chapter005.xhtml",   "08_ch06_responsibility.md",                        "chapter", "Part II: Freedom",          6,  "Responsibility"),
    ("chapter006.xhtml",   "09_ch07_willing.md",                               "chapter", "Part II: Freedom",          7,  "Willing"),
    ("part003.xhtml",      "10_part-3_isolation.md",                           "part",    "Part III: Isolation",       None, "Part III. Isolation"),
    ("chapter007.xhtml",   "11_ch08_existential-isolation.md",                 "chapter", "Part III: Isolation",       8,  "Existential Isolation"),
    ("chapter008.xhtml",   "12_ch09_existential-isolation-and-psychotherapy.md","chapter","Part III: Isolation",       9,  "Existential Isolation and Psychotherapy"),
    ("part004.xhtml",      "13_part-4_meaninglessness.md",                     "part",    "Part IV: Meaninglessness",  None, "Part IV. Meaninglessness"),
    ("chapter009.xhtml",   "14_ch10_meaninglessness.md",                       "chapter", "Part IV: Meaninglessness",  10, "Meaninglessness"),
    ("chapter010.xhtml",   "15_ch11_meaninglessness-and-psychotherapy.md",     "chapter", "Part IV: Meaninglessness",  11, "Meaninglessness and Psychotherapy"),
    ("epilogue.xhtml",     "16_epilogue.md",                                   "epilogue", None,                       None, "Epilogue"),
]

GLYPH_IMG = {  # decorative inline images -> unicode
    "Art_rarrow.jpg": "→",         # right arrow (used in DRIVE -> ANXIETY schemas)
    "Art_rmacr.jpg": "r̄",         # r with macron
    "Art_dash.jpg": "@@HRULE@@",        # section-break ornament
}


def soup_of(path: Path) -> BeautifulSoup:
    return BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")


def inline_md(tag) -> str:
    """Minimal HTML->markdown for note bodies (em/i/strong/b/sup/sub/a/span)."""
    out = []
    for node in tag.children:
        if isinstance(node, NavigableString):
            out.append(str(node))
        elif node.name in ("em", "i"):
            inner = inline_md(node).strip()
            out.append(f"*{inner}*" if inner else "")
        elif node.name in ("strong", "b"):
            inner = inline_md(node).strip()
            out.append(f"**{inner}**" if inner else "")
        elif node.name in ("a", "span", "sup", "sub", "small"):
            out.append(inline_md(node))
        elif node.name == "br":
            out.append(" ")
        else:  # unexpected tag: keep text, note it
            print(f"    [note-conv] flattened <{node.name}> in note", file=sys.stderr)
            out.append(inline_md(node))
    return re.sub(r"\s+", " ", "".join(out))


def load_notes(oebps: Path):
    """Parse notes files.

    Returns:
      endnotes:  {id: (label, md_text)}
      en_chapter: {id: book_chapter_number}   (from "Chapter N" h2 groups)
      en_order:  [ids in document order]
      footnotes: {id: (label, md_text)}  -- multi-paragraph notes joined with
                 indented continuation lines (p.footnote-i / -ii / etc.)
    """
    footnotes = {}
    s = soup_of(oebps / "footnotes.xhtml")
    cur_id = None
    for p in s.find_all("p", class_=re.compile(r"^footnote")):
        pid = p.get("id")
        if pid and pid.endswith("fn"):  # a new note starts here
            back = p.find("a")
            if back:
                back.extract()
            cur_id = pid
            footnotes[cur_id] = [inline_md(p).strip()]
        elif cur_id:  # continuation paragraph of the current note
            footnotes[cur_id].append(inline_md(p).strip())
    footnotes = {k: ("*", "\n    ".join(v)) for k, v in footnotes.items()}

    endnotes, en_chapter, en_order = {}, {}, []
    s = soup_of(oebps / "endnotes.xhtml")
    cur_ch = None
    for el in s.find_all(["h2", "p"]):
        if el.name == "h2":
            m = re.search(r"Chapter\s+(\d+)", el.get_text())
            if m:
                cur_ch = int(m.group(1))
            continue
        if "endnote" not in (el.get("class") or []):
            continue
        pid = el.get("id")  # e.g. en001en
        back = el.find("a")  # backref anchor holds the note number
        label = back.get_text(strip=True) if back else "?"
        if back:
            back.extract()
        # a footnote referenced from inside a citation (e.g. fn049: "Hereafter
        # referred to as Standard Edition") -- resolve it inline
        tails = []
        for a in el.find_all("a", href=re.compile(r"footnotes\.xhtml#(fn\d+fn)")):
            fid = re.search(r"#(fn\d+fn)", a["href"]).group(1)
            if fid in footnotes:
                tails.append(f"\\[\\* {footnotes[fid][1]}\\]")
            a.replace_with("\\*")
        text = inline_md(el).strip()
        if tails:
            text += " " + " ".join(tails)
        endnotes[pid] = (label, text)
        en_chapter[pid] = cur_ch
        en_order.append(pid)
    return endnotes, en_chapter, en_order, footnotes


def gh_slug(text: str) -> str:
    """GitHub-style heading slug."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def preprocess(soup, body, fname: str):
    """Mutate soup body: tokens for notes/pages/ornaments, heading normalization."""
    # 1) note references -> tokens
    for a in body.find_all("a", href=True):
        href = a["href"]
        m = re.match(r"endnotes\.xhtml#(en\d+en)", href)
        if m:
            a.replace_with(f"@@EN{m.group(1)}@@")
            continue
        m = re.match(r"footnotes\.xhtml#(fn\d+fn)", href)
        if m:
            a.replace_with(f"@@FN{m.group(1)}@@")
            continue
        if href.startswith("toc.xhtml"):
            a.unwrap()  # heading backlinks to TOC

    # 2) print-page anchors -> tokens
    for a in body.find_all("a", id=re.compile(r"^page-\d+$")):
        n = a["id"].split("-")[1]
        a.replace_with(f"@@PAGE{n}@@")

    # 3) decorative images -> glyphs / hrule
    for img in body.find_all("img"):
        src = (img.get("src") or "").split("/")[-1]
        if src in GLYPH_IMG:
            img.replace_with(GLYPH_IMG[src])
        else:
            print(f"    [warn] dropping unexpected image {src} in {fname}", file=sys.stderr)
            img.decompose()

    # 4) space-break paragraphs mark a scene break BEFORE the paragraph;
    #    they still contain real text -- keep it, insert a rule before it.
    for p in body.find_all("p", class_=re.compile(r"^space-break")):
        p.insert_before("@@HRULE@@")
        del p["class"]

    # 5) unwrap presentational spans
    for cls in ("dropcap", "small-caps", "bor"):
        for sp in body.find_all("span", class_=cls):
            sp.unwrap()

    # 5b) quote semantics:
    #     div.blockquote* are real quote containers -> <blockquote>
    for d in body.find_all("div", class_=re.compile(r"^blockquote")):
        d.name = "blockquote"
        d.attrs = {}
    #     standalone display blocks -- extracts (ext), verse (linegroup/line),
    #     therapy-dialogue transcripts (dia) -- wrap consecutive runs in <blockquote>
    display_pat = re.compile(r"^(ext|line|dia)")

    def is_display(el):
        if isinstance(el, NavigableString) or not getattr(el, "get", None):
            return False
        if el.name == "p" and any(display_pat.match(c) for c in (el.get("class") or [])):
            return True
        return el.name == "div" and "linegroup" in (el.get("class") or [])

    for el in [e for e in body.find_all(["p", "div"]) if is_display(e)]:
        if el.find_parent("blockquote"):
            continue
        prev = el.find_previous_sibling(lambda t: True)
        if prev is not None and prev.name == "blockquote" and prev.get("data-run"):
            prev.append(el.extract())
        else:
            bq = soup.new_tag("blockquote", **{"data-run": "1"})
            el.insert_before(bq)
            bq.append(el.extract())
    for bq in body.find_all("blockquote"):
        bq.attrs = {}

    # 6) merge "<h1 chapter-number>CHAPTER 2</h1><h1 chapter-title>Title</h1>" pairs
    def is_h1(tag, pat):
        return tag and tag.name == "h1" and any(re.match(pat, c) for c in (tag.get("class") or []))

    for num_pat, tit_pat in ((r"chapter-number", r"chapter-title"),
                             (r"part-number", r"part-title"),
                             (r"preface-number", r"preface-title")):
        for h in body.find_all("h1", class_=re.compile(num_pat)):
            nxt = h.find_next_sibling()
            num_txt = h.get_text(" ", strip=True)
            num_txt = re.sub(r"@@PAGE\d+@@", " ", num_txt)
            num_txt = re.sub(r"\s+", " ", num_txt).strip()
            if is_h1(nxt, tit_pat):
                tit_txt = nxt.get_text(" ", strip=True)
                tit_txt = re.sub(r"@@PAGE\d+@@", " ", tit_txt)
                tit_txt = re.sub(r"\s+", " ", tit_txt).strip()
                # "CHAPTER 2" -> "Chapter 2" ; "PART I" -> "Part I"
                num_txt = re.sub(r"^(CHAPTER|PART)", lambda m: m.group(1).capitalize(), num_txt)
                merged = f"{num_txt}. {tit_txt}"
                nxt.decompose()
                h.string = merged
                h.attrs = {}
            else:
                h.string = num_txt
                h.attrs = {}

    # lone chapter-title (e.g. epilogue "EPILOGUE")
    for h in body.find_all("h1", class_=re.compile(r"chapter-title")):
        t = h.get_text(" ", strip=True)
        h.string = t.title() if t.isupper() else t
        h.attrs = {}

    # 7) demote sections: sect1 h1 -> h2, sect2 h2 -> h3 (capture ids first)
    sections = []
    for h in body.find_all("h1", class_="sect1"):
        title = re.sub(r"\s*@@PAGE\d+@@\s*", " ", h.get_text(" ", strip=True))
        title = re.sub(r"\s+", " ", title).strip()
        sections.append({"id": h.get("id"), "title": title})
        h.name = "h2"
        h.attrs = {}
    for h in body.find_all("h2", class_="sect2"):
        h.name = "h3"
        h.attrs = {}
    return sections


def postprocess_md(md: str, endnotes, footnotes, unlinked, fname: str):
    """Tokens -> markdown footnote refs; append Notes section; tidy."""
    used_en, used_fn = [], []

    def en_sub(m):
        nid = m.group(1)
        if nid not in endnotes:
            print(f"    [warn] missing endnote {nid} in {fname}", file=sys.stderr)
            return ""
        used_en.append(nid)
        return f"[^{endnotes[nid][0]}]"

    def fn_sub(m):
        nid = m.group(1)
        if nid not in footnotes:
            print(f"    [warn] missing footnote {nid} in {fname}", file=sys.stderr)
            return ""
        used_fn.append(nid)
        return f"[^fn-{len(used_fn)}]"

    md = re.sub(r"@@EN(en\d+en)@@", en_sub, md)
    md = re.sub(r"@@FN(fn\d+fn)@@", fn_sub, md)

    # page tokens: drop from heading lines, else -> invisible comment
    def page_line(line):
        if line.lstrip().startswith("#"):
            return re.sub(r"\s*@@PAGE(\d+)@@\s*", " ", line).rstrip()
        return re.sub(r"@@PAGE(\d+)@@", r"<!--p.\1-->", line)

    md = "\n".join(page_line(l) for l in md.split("\n"))
    md = re.sub(r"^\s*@@HRULE@@\s*$", "---", md, flags=re.M)
    md = md.replace("@@HRULE@@", "---")
    md = md.replace("\\!", "!")  # no image syntax in this book; unescape
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"(^---\n\n)+(?=---\n)", "", md, flags=re.M)  # collapse doubled rules

    # cross-references between chapters: chapterNNN.xhtml -> our md filenames
    src2md = {d[0]: d[1] for d in DOCS}

    def xref(m):
        target, anchor = m.group(1), m.group(2) or ""
        if target in src2md:
            return f"({src2md[target]}{anchor})"
        print(f"    [warn] unmapped cross-ref {target} in {fname}", file=sys.stderr)
        return m.group(0)

    md = re.sub(r"\(([a-z]+\d*\.xhtml)(#[^)]*)?\)", xref, md)

    notes_lines = []
    if used_fn:
        notes_lines.append("### Author footnotes\n")
        for i, nid in enumerate(used_fn, 1):
            notes_lines.append(f"[^fn-{i}]: {footnotes[nid][1]}\n")
    if used_en:
        notes_lines.append("### Citations\n")
        seen = set()
        for nid in used_en:
            if nid in seen:
                continue
            seen.add(nid)
            label, text = endnotes[nid]
            notes_lines.append(f"[^{label}]: {text}\n")
    if unlinked:
        notes_lines.append("### Citations not linked in the EPUB text\n")
        notes_lines.append("*(These notes belong to this chapter in the book's back matter, "
                           "but their in-text reference markers were lost in the digital edition.)*\n")
        for nid in unlinked:
            label, text = endnotes[nid]
            notes_lines.append(f"- {label}. {text}")
        notes_lines.append("")
    if notes_lines:
        md = md.rstrip() + "\n\n---\n\n## Notes\n\n" + "\n".join(notes_lines)
    return md.rstrip() + "\n", len(used_fn), len(set(used_en)), len(unlinked)


def convert_doc(oebps: Path, src: str, endnotes, footnotes, unlinked):
    soup = soup_of(oebps / src)
    body = soup.find("body")
    sections = preprocess(soup, body, src)
    html = "".join(str(c) for c in body.children)
    md = subprocess.run(
        ["pandoc", "-f", "html", "-t", "gfm-raw_html", "--wrap=none"],
        input=html.encode("utf-8"), capture_output=True, check=True,
    ).stdout.decode("utf-8")
    md, n_fn, n_en, n_ul = postprocess_md(md, endnotes, footnotes, unlinked, src)
    return md, sections, n_fn, n_en, n_ul


def main(oebps_dir: str, out_dir: str):
    oebps, out = Path(oebps_dir), Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    endnotes, en_chapter, en_order, footnotes = load_notes(oebps)
    print(f"Loaded {len(endnotes)} endnotes, {len(footnotes)} footnotes")

    manifest = {"book": BOOK, "author": AUTHOR,
                "source_epub": "Existential Psychotherapy - Irvin D. Yalom.epub",
                "index": "00_INDEX.md", "files": []}

    for src, dest, typ, part, chnum, title in DOCS:
        # endnotes of this chapter whose in-text markers are absent from the source
        unlinked = []
        if chnum is not None:
            referenced = set(re.findall(r"endnotes\.xhtml#(en\d+en)",
                                        (oebps / src).read_text(encoding="utf-8")))
            unlinked = [i for i in en_order if en_chapter.get(i) == chnum and i not in referenced]
        md, sections, n_fn, n_en, n_ul = convert_doc(oebps, src, endnotes, footnotes, unlinked)
        fm = ["---", f'book: "{BOOK}"', f'author: "{AUTHOR}"', f"type: {typ}"]
        if part:
            fm.append(f'part: "{part}"')
        if chnum:
            fm.append(f"chapter: {chnum}")
        fm += [f'title: "{title}"', "---", "", ""]
        body_md = "\n".join(fm) + md
        (out / dest).write_text(body_md, encoding="utf-8")
        words = len(re.findall(r"\S+", md))
        manifest["files"].append({
            "file": dest, "source": src, "type": typ, "part": part,
            "chapter": chnum, "title": title,
            "sections": [{"title": s["title"], "anchor": gh_slug(s["title"])} for s in sections],
            "words": words, "author_footnotes": n_fn, "citations": n_en, "unlinked_citations": n_ul,
        })
        print(f"  {dest:55} {words:>7} words, {n_fn} fn, {n_en} cit (+{n_ul} unlinked), {len(sections)} sections")

    # ---------- 00_INDEX.md ----------
    L = []
    L.append(f"# {BOOK} — {AUTHOR}\n")
    L.append("Markdown edition split per chapter, converted from the reflowable EPUB "
             "(Basic Books). This file is the **routing index**: use the table and TOC below "
             "to decide which chapter file to open for a given topic.\n")
    L.append("## Conventions\n")
    L.append("- One file per chapter/part intro/epilogue, in reading order (`NN_` prefix = spine order; `chNN` = the book's chapter number).")
    L.append("- Each file is **self-contained**: the chapter's citations (endnotes) and the author's footnotes are inlined at the bottom under `## Notes`, referenced in-text as `[^12]` (citations) and `[^fn-1]` (author footnotes).")
    L.append("- `<!--p.N-->` comments mark print-edition page starts (invisible when rendered; grep-able for page-accurate citation).")
    L.append("- Headings: `#` chapter, `##` major section (listed below), `###` subsection. `---` = ornamental section break in the print text.")
    L.append("- `manifest.json` carries the same map in machine-readable form (files, sections, anchors, word counts).")
    L.append("- Front matter (cover, copyright, dedication, acknowledgments) and publisher pages were omitted.\n")
    L.append("## File map\n")
    L.append("| File | Chapter | Title | Words |")
    L.append("|---|---|---|---|")
    for f in manifest["files"]:
        ch = f"Ch. {f['chapter']}" if f["chapter"] else ("—" if f["type"] != "part" else "Part")
        L.append(f"| `{f['file']}` | {ch} | {f['title']} | {f['words']:,} |")
    L.append("\n## Table of contents (routing)\n")
    cur_part = "~"
    for f in manifest["files"]:
        if f["type"] == "part":
            L.append(f"\n### [{f['title']}]({f['file']})\n")
            cur_part = f["part"]
            continue
        if f["type"] == "chapter" and f["part"] is None and cur_part != None:
            pass
        label = f"Chapter {f['chapter']}. {f['title']}" if f["chapter"] else f["title"]
        L.append(f"- **[{label}]({f['file']})**")
        for s in f["sections"]:
            L.append(f"  - [{s['title']}]({f['file']}#{s['anchor']})")
    L.append("")
    (out / "00_INDEX.md").write_text("\n".join(L), encoding="utf-8")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    total = sum(f["words"] for f in manifest["files"])
    print(f"\nWrote {len(manifest['files'])} content files + 00_INDEX.md + manifest.json ({total:,} words total)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
