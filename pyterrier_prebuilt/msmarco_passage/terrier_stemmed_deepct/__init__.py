

DIR="/local/terrier/Resources/msmarco/deepct/"
INDEXER_KWARGS={'overwrite' : True}
MAX_DOCNOLEN = 10

def index(dest_dir):
    import pyterrier as pt
    
    def corpus_iter():
        import json
        files = [ DIR + "collection_pred_%d/deepctcollection.gz" % d for d in [1,2] ]
        for fname in files:
                with pt.io.autoopen(fname, 'rt') as fh:
                    for l in fh:
                        docno, text = l.split("\t")
                        yield {"docno" : docno, "text" : text}
                    
    init_args = INDEXER_KWARGS.copy()
    index_args = {}
    props = {}
    index_args['meta']={'docno' : MAX_DOCNOLEN}

    indexer = pt.IterDictIndexer(dest_dir, **init_args)
    for k,v in props.items():
        indexer.setProperty(k, v)
    indexref = indexer.index(corpus_iter(), **index_args)
    