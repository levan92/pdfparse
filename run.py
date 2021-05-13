import argparse
from pathlib import Path
import dateutil.parser as dparser
from collections import defaultdict

import PyPDF2
from pprint import pprint

from config import IDENTIFIER, TRASH, WANTED

WANTED2CAT = { v:k for k,l in WANTED.items() for v in l }

def is_in_list(key, list_):
    return any([ t in key for t in list_ ])

def split_text(text):
    dict_ = defaultdict(int)
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
                found_wanted = [ wanted for wanted in WANTED2CAT.keys() if wanted in key ] 
                assert len(found_wanted) == 1,f'{found_wanted},{key}'
                found_wanted = found_wanted[0] 
                dict_[WANTED2CAT[found_wanted]] += val
                
            key = None
            val = None
    res = [ dict_[k] for k in sorted(WANTED.keys()) ]
    return res

ap = argparse.ArgumentParser()
ap.add_argument('pdfdir')
args = ap.parse_args()

res_dict = {}

for pdfp in Path(args.pdfdir).rglob('*'):
    if pdfp.suffix in ('.pdf','.PDF') and IDENTIFIER in pdfp.stem:
        with pdfp.open('rb') as f:
            preader = PyPDF2.PdfFileReader(f)
            assert preader.numPages == 1
            page0 = preader.getPage(0)
            pdftext = page0.extractText()
            try:
                date = dparser.parse(pdfp.stem, fuzzy = True)
            except Exception as e:
                print('Cannot parse date from pdf name', e)
            date = date.date()
            date = date.replace(day=1)
            res = split_text(pdftext)
            res_dict[date] = res

sorted_date = sorted(res_dict.keys())
with open(f'res.csv','w') as f:
    for date in sorted_date:
        a,b,c,d = res_dict[date]
        print_str = f'{date:%d/%m/%Y},{a},{b},{c},{d}'
        print(print_str)
        f.write(print_str+'\n')
