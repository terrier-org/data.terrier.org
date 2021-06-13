

DIR="/local/terrier/Resources/msmarco/docT5query/msmarco-passages/msmarco-passage-expanded"
INDEXER_KWARGS={'overwrite' : True}
MAX_DOCNOLEN = 10

def index(dest_dir):
    import pyterrier as pt
    import json

    def read_gen():
        with open('/local/terrier/Resources/msmarco/docT5query/msmarco-docs/output/docs.json') as f:
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
    
