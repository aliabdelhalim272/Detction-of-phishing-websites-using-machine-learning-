"""Check output completeness and render contact sheets for visual inspection."""
from pathlib import Path
import hashlib
import json
import sys
import zipfile
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT.parent/'.delivery-tools'))
import pymupdf
from PIL import Image,ImageOps,ImageDraw
import nbformat

DELIVERY=ROOT/'submission/GroupXX_PhishingDetection'
PREVIEW=ROOT/'reports/submission_validation'
PREVIEW.mkdir(parents=True,exist_ok=True)

def inspect_pdf(path):
    doc=pymupdf.open(path)
    thumbs=[];words_count=[]
    for number,page in enumerate(doc):
        words=page.get_text('words');words_count.append(len(words))
        assert len(words)>15,(path,number)
        for x0,y0,x1,y1,*_ in words:
            assert x0>=-1 and y0>=-1 and x1<=page.rect.width+1 and y1<=page.rect.height+1,(path,number,(x0,y0,x1,y1),page.rect)
        pix=page.get_pixmap(matrix=pymupdf.Matrix(1.1,1.1))
        im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
        if number in [0,len(doc)//2,len(doc)-1]:im.save(PREVIEW/f'{path.stem}_page_{number+1}.png')
        thumb=ImageOps.contain(im,(390,510))
        tile=Image.new('RGB',(410,545),'#E8EEF3');tile.paste(thumb,((410-thumb.width)//2,12))
        ImageDraw.Draw(tile).text((12,525),f'{path.stem} | {number+1}',fill='#142B45')
        thumbs.append(tile)
    for first in range(0,len(thumbs),8):
        group=thumbs[first:first+8];sheet=Image.new('RGB',(410*4,545*((len(group)+3)//4)),'white')
        for i,tile in enumerate(group):sheet.paste(tile,((i%4)*410,(i//4)*545))
        sheet.save(PREVIEW/f'{path.stem}_contact_{first//8+1}.png')
    return {'pages':len(doc),'words_per_page':words_count}

if __name__=='__main__':
    notebook=nbformat.read(DELIVERY/'GroupXX_Project.ipynb',4)
    code=[c for c in notebook.cells if c.cell_type=='code']
    assert len(code)==48 and all(c.execution_count is not None for c in code)
    assert not any(o.output_type=='error' for c in code for o in c.outputs)
    image_count=sum('image/png' in o.get('data',{}) for c in code for o in c.outputs)
    assert image_count>=5
    assert hashlib.sha256((DELIVERY/'dataset.csv').read_bytes()).hexdigest()=='a236549cd369cd80bd478ff8e1779cbf44c58d5c3f79f7a51a1adbed7d06d1c6'
    result={'execution':'PASS','executed_code_cells':len(code),'embedded_figures':image_count,'pdf_checks':{}}
    for path in [DELIVERY/'GroupXX_Report.pdf',*sorted((ROOT/'presentation').glob('*.pdf'))]:
        result['pdf_checks'][path.name]=inspect_pdf(path)
    with zipfile.ZipFile(ROOT/'presentation/GroupXX_Presentation.pptx') as archive:
        slides=[p for p in archive.namelist() if __import__('re').fullmatch(r'ppt/slides/slide\d+\.xml',p)]
        notes=[p for p in archive.namelist() if __import__('re').fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',p)]
        assert len(slides)==len(notes)==12
        for name in slides+notes:ET.fromstring(archive.read(name))
        result['presentation']={'slides':len(slides),'notes':len(notes),'target_seconds':650,'members_speaking':3}
    (PREVIEW/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
