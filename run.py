import argparse
from pathlib import Path

import PyPDF2
from pprint import pprint

def is_in_list(key, list_):
    return any([ t in key for t in list_ ])

def split_text(text):
    dict_ = {}
    key, val = None, None
    for unit in text.split():
        try:
            val = float(unit.replace(',',''))
        except ValueError as e:
            if key is None:
                key = unit
            else:
                key += f' {unit}'
            val = None

        if key is not None and val is not None:
            if not is_in_list(key, TRASH):
                dict_[key] = val
                if not is_in_list(key, WANTED):
                    print('Not in wanted list: ', key)
            key = None
            val = None
    # pprint(dict_)
    # import pdb;pdb.set_trace()

ap = argparse.ArgumentParser()
ap.add_argument('pdfdir')
args = ap.parse_args()

for pdfp in Path(args.pdfdir).rglob('*'):
    if pdfp.suffix in ('.pdf','.PDF') and IDENTIFIER in pdfp.stem:
        with pdfp.open('rb') as f:
            preader = PyPDF2.PdfFileReader(f)
            assert preader.numPages == 1
            page0 = preader.getPage(0)
            pdftext = page0.extractText()
            split_text(pdftext)
            # import pdb;pdb.set_trace()

