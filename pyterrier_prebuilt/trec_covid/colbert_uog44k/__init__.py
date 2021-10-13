INDEXER_KWARGS={'overwrite' : True}
from typing import List
def index(dest_dir, variant=None):
    import pyterrier as pt
    import os
    import json
    dataset = pt.get_dataset("irds:cord19").get_corpus_iter()

    from pyterrier_colbert.indexing import ColBERTIndexer
    checkpoint="http://www.dcs.gla.ac.uk/~craigm/colbert.dnn.zip"

    indexer = ColBERTIndexer(checkpoint, os.path.dirname(dest_dir),os.path.basename(dest_dir), chunksize=3, gpu=False)
    indexer = pt.text.sliding(text_attr='abstract', prepend_attr='title') >> pt.apply.text(lambda r: r['abstract']) >> indexer
    indexer.index(dataset)
    with open(os.path.join(dest_dir, '_ColBERTFactoryconstruct.args.json'), 'wt') as argsfile:
        kwargs = {
            'colbert_model' : checkpoint,
            'faiss_partitions': 100
        }
        argsfile.write(json.dumps(kwargs))

def get_variant_description(variant : str) -> str:
    return "ColBERT dense retrieval index using model trained by UoG for TREC 2020 DL track. Uses the [pyterrier_colbert](https://github.com/terrierteam/pyterrier_colbert) plugin. " \
           "Since most documents exceed the maximum length supported by ColBERT, a sliding window of 150 tokens was used (stride 75, prepending title) to construct passages. As such, " \
           "passage scores need to be aggregated, e.g., using pt.text.max_passage()."

def get_retrieval_head(dataset : str, variant : str) -> str:
    return ['#!pip install --upgrade git+https://github.com/terrierteam/pyterrier_colbert.git', 'from pyterrier_colbert.ranking import ColBERTFactory']

def get_retrieval_pipelines(dataset : str, variant : str) -> List[str]:
    return [
        ( "colbert_e2e", "ColBERTFactory.from_dataset('%s', '%s').end_to_end() >> pt.text.max_passage()" % (dataset, variant) ),
        ( "colbert_prf_rank", "ColBERTFactory.from_dataset('%s', '%s').colbert_prf(rerank=False) >> pt.text.max_passage()" % (dataset, variant) ),
        ( "colbert_prf_rerank", "ColBERTFactory.from_dataset('%s', '%s').colbert_prf(rerank=True) >> pt.text.max_passage()" % (dataset, variant) ),
    ]
