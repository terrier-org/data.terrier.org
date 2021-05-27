

DIR="/local/terrier/Resources/msmarco/docT5query/msmarco-passages/msmarco-passage-expanded"
INDEXER_KWARGS={'overwrite' : True}
MAX_DOCNOLEN = 10

def index(dest_dir):
    import pyterrier as pt
    
    def corpus_iter():
        import json
        files = pt.io.find_files(DIR)
        for fname in files:
            if fname.startswith("docs") and fname.endswith(".json.gz"):
                with pt.io.autoopen(fname) as fh:
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
    
