

INDEXER_KWARGS={'overwrite' : True}
MAX_DOCNOLEN = 10
MAX_TEXT = 4096

def index(dest_dir, variant='terrier-stemmed'):
    import pyterrier as pt
    dataset = pt.get_dataset('trec-deep-learning-docs').get_corpus()

    init_args = INDEXER_KWARGS.copy()
    index_args = {}
    props = {}
    init_args['meta']={'docno' : MAX_DOCNOLEN}

    if variant.startswith('terrier-unstemmed'):
        props["termpipelines"] = ""
        
    if variant.endswith('text'):
        init_args['meta']['text'] = MAX_TEXT
        init_args['meta_tags'] = {'text' : 'ELSE'}
    
    indexer = pt.TRECCollectionIndexer(dest_dir, **init_args)
    for k,v in props.items():
        indexer.setProperty(k, v)
    indexref = indexer.index(dataset, **index_args)
    