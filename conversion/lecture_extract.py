#!/usr/bin/env python3
"""
Extract a Fa26 lecture deck into text an agent can read.

    python conversion/lecture_extract.py --out <dir>        # reads lectures/*.pptx

Writes <dir>/L0N/slides.md (per-slide text plus the media each slide shows), notes.md (speaker
notes), and media/ (images). python-pptx is not in the d100 env, so this reads the OOXML directly.
An image present in every deck is template chrome (Slido icons, the theme logo) and is dropped by
content hash, so nothing downstream has to recognise it.
"""
import zipfile, re, hashlib, os, sys, glob, collections
from xml.etree import ElementTree as ET
import argparse
ap = argparse.ArgumentParser(description="Extract slide text, speaker notes and media from the Fa26 decks in lectures/.")
ap.add_argument("--out", required=True, help="directory to write L0N/{slides.md,notes.md,media/} into")
ap.add_argument("--decks", default="lectures", help="directory holding the .pptx files")
args = ap.parse_args()
OUT = args.out
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
decks = sorted(glob.glob(os.path.join(args.decks, "*.pptx")))
# hash count across decks -> template chrome = appears in all 5 decks
hashes = collections.Counter()
per = {}
for d in decks:
    z = zipfile.ZipFile(d); hs = set()
    for n in z.namelist():
        if n.startswith("ppt/media/"):
            hs.add(hashlib.md5(z.read(n)).hexdigest())
    per[d] = hs; hashes.update(hs)
chrome = {h for h, c in hashes.items() if c == len(decks)}
def slide_text(xml):
    root = ET.fromstring(xml); paras = []
    for p in root.iter(A + "p"):
        t = "".join(x.text or "" for x in p.iter(A + "t"))
        if t.strip(): paras.append(t)
    return paras
for d in decks:
    m = re.search(r"Lec (\d+)", d); L = f"L{m.group(1)}"
    od = os.path.join(OUT, L); md = os.path.join(od, "media"); os.makedirs(md, exist_ok=True)
    z = zipfile.ZipFile(d)
    slides = sorted([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)],
                    key=lambda s: int(re.search(r"(\d+)", s.split("/")[-1]).group(1)))
    lines = [f"# {os.path.basename(d)}\n"]; notes = []
    for s in slides:
        k = int(re.search(r"slide(\d+)", s).group(1))
        rels = f"ppt/slides/_rels/slide{k}.xml.rels"; media = []
        if rels in z.namelist():
            for rel in ET.fromstring(z.read(rels)):
                t = rel.get("Target", "")
                if "media/" in t:
                    name = t.split("/")[-1]; data = z.read("ppt/media/" + name)
                    if hashlib.md5(data).hexdigest() in chrome: continue
                    media.append(name)
                    p = os.path.join(md, name)
                    if not os.path.exists(p): open(p, "wb").write(data)
                if "notesSlide" in t:
                    nx = "ppt/notesSlides/" + t.split("/")[-1]
                    if nx in z.namelist():
                        nt = [x for x in slide_text(z.read(nx)) if not x.strip().isdigit()]
                        if nt: notes.append(f"## Slide {k}\n" + "\n".join(nt) + "\n")
        lines.append(f"## Slide {k}\n" + "\n".join(slide_text(z.read(s))))
        if media: lines.append("media: " + ", ".join(sorted(set(media))))
        lines.append("")
    open(os.path.join(od, "slides.md"), "w").write("\n".join(lines))
    open(os.path.join(od, "notes.md"), "w").write("\n".join(notes))
    print(L, len(slides), "slides,", len(os.listdir(md)), "media")
