
INDEXER_KWARGS={'overwrite' : True}

def index(dest_dir, variant='terrier-stemmed'):
    import pyterrier as pt
    dataset = pt.get_dataset("vaswani").get_corpus_iter()

    init_args = INDEXER_KWARGS.copy()
    index_args = {}
    props = {}
    if variant.startswith('terrier-unstemmed'):
        props["termpipelines"] = ""
    if variant.endswith('text'):
        index_args['meta']={'docno' : 20, 'text': 4096}
    
    indexer = pt.IterDictIndexer(dest_dir, **init_args)
    for k,v in props.items():
        indexer.setProperty(k, v)
    indexref = indexer.index(dataset, **index_args)
    