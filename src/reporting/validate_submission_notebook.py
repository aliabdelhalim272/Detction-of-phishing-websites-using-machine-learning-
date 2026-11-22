"""Execute the notebook from its standalone folder and preserve visible outputs."""
from pathlib import Path
import json
import time
import nbformat
from nbclient import NotebookClient

ROOT=Path(__file__).resolve().parents[2]
DELIVERY=ROOT/'submission/GroupXX_PhishingDetection'
PATH=DELIVERY/'GroupXX_Project.ipynb'

if __name__=='__main__':
    nb=nbformat.read(PATH,as_version=4)
    started=time.perf_counter()
    def on_cell_executed(cell,cell_index,**kwargs):
        print(f'Completed cell {cell_index+1}/{len(nb.cells)}',flush=True)
    client=NotebookClient(nb,timeout=1800,kernel_name='python3',
        resources={'metadata':{'path':str(DELIVERY)}},on_cell_executed=on_cell_executed)
    try:
        client.execute()
    finally:
        nbformat.write(nb,PATH)
    assert not any(o.output_type=='error' for c in nb.cells if c.cell_type=='code' for o in c.outputs)
    assert all(c.execution_count is not None for c in nb.cells if c.cell_type=='code')
    expected=json.loads((ROOT/'reports/final_evaluation/status.json').read_text())
    actual=json.loads((DELIVERY/'reports/final_evaluation/status.json').read_text())
    assert actual==expected,(actual,expected)
    print(f'Standalone execution passed in {time.perf_counter()-started:.1f}s; frozen evaluation reproduced.',flush=True)
