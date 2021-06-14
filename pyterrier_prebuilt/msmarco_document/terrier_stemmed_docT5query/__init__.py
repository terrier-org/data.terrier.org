

DIR="/local/terrier/Resources/msmarco/docT5query/msmarco-docs/output"
FILE="docs.json.gz" #may not be compressed
INDEXER_KWARGS={'overwrite' : True}
MAX_DOCNOLEN = 10

def index(dest_dir, **kwargs):
    import pyterrier as pt
    import json
    import os

    def read_gen():
        with pt.io.autoopen(os.path.join(DIR, FILE), 'rt') as f:
            for i, x in enumerate(pt.tqdm(f, unit='d', total=3_200_000)):
                y = json.loads(x)
                y['docno'] = y['id']
                y['text'] = y['contents']
                yield y
              
    init_args = INDEXER_KWARGS.copy()
    index_args = {}
    props = {}
    index_args['meta']={'docno' : MAX_DOCNOLEN}

    indexer = pt.IterDictIndexer(dest_dir, **init_args)
    for k,v in props.items():
        indexer.setProperty(k, v)
    indexref = indexer.index(read_gen(), **index_args)
    
def get_variant_description(variant : str) -> str:
    return "Terrier index using docT5query. Porter stemming and stopword removal applied"

def get_retrieval_pipelines(dataset : str, variant : str) -> str:
    return [
        ( "bm25_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='BM25')" % (dataset, variant) ),
    ]