

DIR="/local/terrier/Resources/msmarco/docT5query/msmarco-passages/msmarco-passage-expanded"
INDEXER_KWARGS={'overwrite' : True}
MAX_DOCNOLEN = 10

def index(dest_dir, **kwargs):
    import pyterrier as pt
    
    def corpus_iter():
        import json
        files = pt.io.find_files(DIR)
        for fname in files:
            if "/docs" in fname and fname.endswith(".json.gz"):
                with pt.io.autoopen(fname, 'rt') as fh:
                    for l in fh:
                        obj = json.loads(l)
                        obj['docno'] = obj.pop('id')
                        obj['text'] = obj.pop('contents')
                        yield obj                    
                    
    init_args = INDEXER_KWARGS.copy()
    index_args = {}
    props = {}
    index_args['meta']={'docno' : MAX_DOCNOLEN}

    indexer = pt.IterDictIndexer(dest_dir, **init_args)
    for k,v in props.items():
        indexer.setProperty(k, v)
    indexref = indexer.index(corpus_iter(), **index_args)

def get_variant_description(variant : str) -> str:
    return """Terrier index using docT5query. Porter stemming and stopword removal applied. This index was made using the MSMARCO files
provided linked from the [authors' original repository](https://github.com/castorini/docTTTTTquery).
To create indices for other corpora, use the [pyterrier_doc2query plugin](https://github.com/terrierteam/pyterrier_doc2query)."""

def get_retrieval_head(dataset : str, variant : str) -> str:
    return None

def get_retrieval_pipelines(dataset : str, variant : str) -> str:
    return [
        ( "bm25_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='BM25')" % (dataset, variant) ),
    ]