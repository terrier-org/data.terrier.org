

INDEXER_KWARGS={'overwrite' : True}
MAX_DOCNOLEN = 10
MAX_TEXT = 4096

def index(dest_dir, variant='terrier-stemmed'):
    import pyterrier as pt
    dataset = pt.get_dataset("trec-deep-learning-passages").get_corpus_iter()

    init_args = INDEXER_KWARGS.copy()
    index_args = {}
    props = {}
    index_args['meta']={'docno' : MAX_DOCNOLEN}

    if variant.startswith('terrier-unstemmed'):
        props["termpipelines"] = ""
        
    if variant.endswith('text'):
        index_args['meta']['text'] = MAX_TEXT
    
    indexer = pt.IterDictIndexer(dest_dir, **init_args)
    for k,v in props.items():
        indexer.setProperty(k, v)
    indexref = indexer.index(dataset, **index_args)
    