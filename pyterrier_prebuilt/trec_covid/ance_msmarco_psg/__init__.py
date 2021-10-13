INDEXER_KWARGS={'overwrite' : True}
from typing import List

def index(dest_dir, variant=None):
    import pyterrier as pt
    import os
    import json
    dataset = pt.get_dataset('irds:cord19').get_corpus_iter()

    from pyterrier_ance import ANCEIndexer
    checkpoint = "https://webdatamltrainingdiag842.blob.core.windows.net/semistructstore/OpenSource/Passage_ANCE_FirstP_Checkpoint.zip"
    
    indexer = ANCEIndexer(checkpoint, dest_dir, verbose=False, text_attr='abstract')
    indexer = pt.text.sliding(text_attr='abstract', prepend_attr='title') >> indexer
    indexer.index(dataset)
    with open(os.path.join(dest_dir, '_ANCERetrievalconstruct.args.json'), 'wt') as argsfile:
        kwargs = {
            'checkpoint_path' : checkpoint,
        }
        argsfile.write(json.dumps(kwargs))

def get_variant_description(variant : str) -> str:
    return "ANCE dense retrieval index using model trained by original ANCE authors. Uses the [pyterrier_ance](https://github.com/terrierteam/pyterrier_ance) plugin. " \
           "Since most documents exceed the maximum length supported by ANCE, a sliding window of 150 tokens was used (stride 75, prepending title) to construct passages. As such, " \
           "passage scores need to be aggregated, e.g., using pt.text.max_passage()."

def get_retrieval_head(dataset : str, variant : str) -> str:
    return [
        '#!pip install --upgrade git+https://github.com/terrierteam/pyterrier_ance.git',
        'from pyterrier_ance import ANCERetrieval']

def get_retrieval_pipelines(dataset : str, variant : str) -> List[str]:
    return [
        ( "ance", "ANCERetrieval.from_dataset('%s', '%s') >> pt.text.max_passage()" % (dataset, variant) )
    ]
