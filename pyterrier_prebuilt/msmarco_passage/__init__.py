

DOC_INFO = {
    "friendlyname" : "MSMARCO Passage Ranking",
    "desc" : "A passage ranking task based on a corpus of 8.8 million passages released by Microsoft, which should be rank based on their relevance to questions.  Also used by the TREC Deep Learning track."
}

TOPICS_QRELS = [
    # {
    #     "name" : "dev.small",
    #     "desc" : "6800 topics with sparse judgements",
    #     "location" : ("trec-deep-learning-passages", "dev.small"),
    #     "metrics" : ["recip_rank"],
    # },
    {
        "name" : "trec-2019",
        "desc" : "43 topics used in the TREC Deep Learning track Passage Ranking task, with deep judgements",
        "location" : ("trec-deep-learning-passages", "test-2019"),
        "metrics" : ["ndcg_cut_10"], #TODO insert pyterrier.measures
    },
    {
        "name" : "trec-2020",
        "desc" : "43 topics used in the TREC Deep Learning track Passage Ranking task, with deep judgements",
        "location" : ("trec-deep-learning-passages", "test-2019"),
        "metrics" : ["ndcg_cut_10"], #TODO insert pyterrier.measures
    }
]

INDEXER_KWARGS={'overwrite' : True}
MAX_DOCNOLEN = 10
MAX_TEXT = 4096

def index(dest_dir, variant='terrier-stemmed'):
    import pyterrier as pt
    dataset = pt.get_dataset('irds:msmarco-passage').get_corpus_iter()

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
    
def get_variant_description(variant : str) -> str:
    import pyterrier_prebuilt as pb
    return pb.get_default_variant_description(variant)