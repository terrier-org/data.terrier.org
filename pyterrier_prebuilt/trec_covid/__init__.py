from pyterrier.measures import *

DOC_INFO = {
    "friendlyname" : "TREC COVID",
    "desc" : "A collection of scientific articles related to COVID-19. This uses the 2020-07-16 version of the CORD-19, which is used by the TREC COVID complete benchmark."
}

INDEXER_KWARGS={'overwrite' : True, 'meta_reverse' : ['docno']}
TOPICS_QRELS=[
    {
        "name" : "TREC COVID Complete",
        "desc" : '50 topics from the TREC COVID task, with deep judgements. Using natural-language "description" queries.',
        "location" : ("irds:cord19/trec-covid", 'description', None),
        "metrics" : [nDCG@10, P@5, P(rel=2)@5, AP],
    }
]

def get_variant_description(variant : str) -> str:
    if variant == "terrier_unstemmed_text":
        return "Terrier index, no stemming, no stopword removal. Text is also saved in the MetaIndex to facilitate BERT-based reranking."
    if variant == "terrier_unstemmed":
        return "Terrier index, no stemming, no stopword removal"
    if variant == "terrier_stemmed":
        return "Terrier's default Porter stemming, and stopwords removed"
    if variant == "terrier_stemmed_text":
        return "Terrier's default Porter stemming, and stopwords removed. Text is also saved in the MetaIndex to facilitate BERT-based reranking."
    if variant == "terrier_unstemmed_positions":
        return "Terrier index, no stemming, no stopword removal. Position information is saved for proximity or phrase queries."
    if variant == "terrier_stemmed_positions":
        return "Terrier's default Porter stemming, no stopword removal. Position information is saved for proximity or phrase queries."
    return "unknown variant"

def index(dest_dir, variant='terrier_stemmed'):
    import pyterrier as pt
    def _dataset():
        encountered_dids = set()
        for doc in pt.get_dataset("irds:cord19").get_corpus_iter():
            if doc['docno'] not in encountered_dids:
                yield doc
                encountered_dids.add(doc['docno'])

    dataset = _dataset()

    init_args = INDEXER_KWARGS.copy()
    index_args = {'meta' : {'docno' : 8}, 'fields': ['title', 'abstract']}
    props = {}
    if variant.startswith('terrier_unstemmed'):
        props["termpipelines"] = ""
    if variant.endswith('text'):
        index_args['meta']={'docno' : 20, 'title': 1194, 'abstract': 122523}
    if 'positions' in variant:
        init_args['blocks'] = True
    if 'doct5query' in variant:
        from pyterrier_doc2query import Doc2Query
        doc2query = Doc2Query('./t5-base/model.ckpt')
        indexer = doc2query >> indexer
    indexer = pt.IterDictIndexer(dest_dir, **init_args)
    for k,v in props.items():
        indexer.setProperty(k, v)
    indexref = indexer.index(dataset, **index_args)

def get_retrieval_head(dataset : str, variant : str) -> str:
    return []

def get_retrieval_pipelines(dataset : str, variant : str) -> str:
    return [
        ( "bm25_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='BM25')" % ('trec-covid', variant) ),
        ( "dph_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='DPH')" % ('trec-covid', variant) ),
        ( "dph_bo1_" + variant, "dph_%s >> pt.rewrite.Bo1QueryExpansion(pt.get_dataset('%s').get_index('%s')) >> dph_%s" % (variant, 'trec-covid', variant, variant) ),
    ]
