
VBERT = "onir_pt.reranker('hgf4_joint', ranker_config={'model': 'Capreolus/bert-base-msmarco', 'norm': 'softmax-2'}"
DOC_INFO = {
    "friendlyname" : "MSMARCO v2 Passage Ranking",
    "desc" : "A passage ranking task based on a revised corpus of 138M passages released by Microsoft in July 2021, which should be rank based on their relevance to questions.  Also used by the TREC 2021 Deep Learning track."
}

TOPICS_QRELS = []
INDEXER_KWARGS={'overwrite' : True, 'threads': 8}
MAX_DOCNOLEN = 28

def index(dest_dir, variant='terrier_stemmed'):
    import pyterrier as pt
    dataset = pt.get_dataset('irds:msmarco-passage-v2').get_corpus_iter()

    init_args = INDEXER_KWARGS.copy()
    index_args = {}
    props = {}
    index_args['meta']={'docno' : MAX_DOCNOLEN}

    if variant.startswith('terrier_unstemmed'):
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

def get_retrieval_pipelines(dataset : str, variant : str) -> str:
    return [
        ( "bm25_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='BM25')" % (dataset, variant) ),
        ( "bm25_bert_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s') >> pt.text.get_text(%s) >> %s" % (dataset, variant, 'irds:msmarco-passage-v2', VBERT)  )
        ( "dph_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='DPH')" % (dataset, variant) ),
        ( "dph_bert_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s',  wmodel='DPH') >> pt.text.get_text(%s) >> %s" % (dataset, variant, 'irds:msmarco-passage-v2', VBERT)  )

    ]
