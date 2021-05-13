import argparse
from pathlib import Path

from pikepdf import Pdf

from config import IDENTIFIER

ap = argparse.ArgumentParser()
ap.add_argument('pdfdir')
ap.add_argument('pw')
args = ap.parse_args()

pdf_dir = Path(args.pdfdir)

out_pdf_dir = pdf_dir.parent / f'{pdf_dir.stem}_nopw'

for pdfp in pdf_dir.rglob('*'):
    if pdfp.suffix in ('.pdf','.PDF') and IDENTIFIER in pdfp.stem:
        subpath = pdfp.relative_to(pdf_dir).parent
        outdir = out_pdf_dir / subpath
        outdir.mkdir(parents=True, exist_ok=True)
        outpath = outdir / pdfp.name

        with Pdf.open(pdfp, password=args.pw) as pdf:
            pdf.save(outpath)
    