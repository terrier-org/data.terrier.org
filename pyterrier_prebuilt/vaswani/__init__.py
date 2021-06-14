
DOC_INFO = {
    "friendlyname" : "Vaswani",
    "desc" : "The Vaswani NPL corpus is a small test collection of 11,000 abstracts has been used by the Glasgow IR group for many years (created 1990). "+
        "Due to its small size, it is used for many test cases used in both Terrier and PyTerrier.",
}

INDEXER_KWARGS={'overwrite' : True}
TOPICS_QRELS=[
    {
        "location" : ("vaswani", None),
    }
]

def get_variant_description(variant : str) -> str:
    if variant == "terrier_unstemmed_text":
        return "Terrier index, no stemming, no stopword removal. Text is also saved in the MetaIndex to facilitate BERT-based reranking.",
    if variant == "terrier_unstemmed":
        return "Terrier index, no stemming, no stopword removal"
    if variant == "terrier_stemmed":
        return "Terrier's default Porter stemming, and stopwords removed"
    if variant == "terrier_stemmed_text":
        return "Terrier's default Porter stemming, and stopwords removed. Text is also saved in the MetaIndex to facilitate BERT-based reranking."
    return "unknown variant"

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

def get_retrieval_pipelines(dataset : str, variant : str) -> str:
    return [
        ( "bm25_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='BM25')" % (dataset, variant) ),
        ( "dph_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='DPH')" % (dataset, variant) ),
        ( "dph_bo1_" + variant, "dph_%s >> pt.rewrite.Bo1QueryExpansion(pt.get_dataset('%s').get_index('%s') >> dph_%s" % (variant, dataset, variant, variant) ),
    ]
