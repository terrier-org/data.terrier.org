
INDEXER_KWARGS={'overwrite' : True}
from typing import List
def index(dest_dir, variant=None):
    import pyterrier as pt
    import os
    import json
    dataset = pt.get_dataset("vaswani").get_corpus_iter()

    from pyterrier_colbert.indexing import ColBERTIndexer
    checkpoint="http://www.dcs.gla.ac.uk/~craigm/colbert.dnn.zip"

    indexer = ColBERTIndexer(checkpoint, os.path.dirname(dest_dir),os.path.basename(dest_dir), chunksize=3, gpu=False)
    indexer.index(dataset)
    with open(os.path.join(dest_dir, 'ColBERTFactory.args.json'), 'wt') as argsfile:
        kwargs = {
            'colbert_model' : checkpoint,
        }
        argsfile.write(json.dumps(kwargs))

def get_variant_description(variant : str) -> str:
    return "ColBERT dense retrieval index using model trained by UoG for TREC 2020 DL track"

def get_retrieval_head(dataset : str, variant : str) -> str:
    return ['from pyterrier_colbert.ranking import ColBERTFactory']

def get_retrieval_pipelines(dataset : str, variant : str) -> List[str]:
    return [
        ( "colbert_e2e", "ColBERTFactory.from_dataset('%s', '%s').end_to_end()" % (dataset, variant) ),
        ( "colbert_prf_rank", "ColBERTFactory.from_dataset('%s', '%s').colbert_prf(rerank=False)" % (dataset, variant) ),
        ( "colbert_prf_rerank", "ColBERTFactory.from_dataset('%s', '%s').colbert_prf(rerank=True)" % (dataset, variant) ),
    ]