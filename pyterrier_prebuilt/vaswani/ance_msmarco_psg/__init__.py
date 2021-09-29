
INDEXER_KWARGS={'overwrite' : True}
from typing import List
def index(dest_dir, variant=None):
    import pyterrier as pt
    import os
    import json
    dataset = pt.get_dataset("vaswani").get_corpus_iter()

    from pyterrier_ance import ANCEIndexer
    checkpoint="https://webdatamltrainingdiag842.blob.core.windows.net/semistructstore/OpenSource/Passage_ANCE_FirstP_Checkpoint.zip"
    
    indexer = ANCEIndexer(checkpoint, dest_dir, verbose=False)
    indexer.index(dataset)
    with open(os.path.join(dest_dir, '_ANCERetrievalconstruct.args.json'), 'wt') as argsfile:
        kwargs = {
            'checkpoint_path' : checkpoint,
        }
        argsfile.write(json.dumps(kwargs))

def get_variant_description(variant : str) -> str:
    return "ANCE dense retrieval index using model trained by original ANCE authors. Uses the pyterrier_ance plugin."

def get_retrieval_head(dataset : str, variant : str) -> str:
    return [
        '#!pip install --upgrade git+https://github.com/terrierteam/pyterrier_ance.git',
        'from pyterrier_ance import ANCERetrieval']

def get_retrieval_pipelines(dataset : str, variant : str) -> List[str]:
    return [
        ( "ance", "ANCERetrieval.from_dataset('%s', '%s')" % (dataset, variant) )
    ]
