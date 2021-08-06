
VBERT = "onir_pt.reranker('hgf4_joint', ranker_config={'model': 'Capreolus/bert-base-msmarco', 'norm': 'softmax-2'}"
DOC_INFO = {
    "friendlyname" : "MSMARCO Passage Ranking",
    "desc" : "A passage ranking task based on a corpus of 8.8 million passages released by Microsoft, which should be rank based on their relevance to questions.  Also used by the TREC Deep Learning track."
}

TOPICS_QRELS = [
    {
        "name" : "trec-2019",
        "desc" : "43 topics used in the TREC Deep Learning track Passage Ranking task, with deep judgements",
        "location" : ("msmarco_passage", "test-2019"),
        "metrics" : ["ndcg_cut_10"], #TODO insert pyterrier.measures
    },
    {
        "name" : "trec-2020",
        "desc" : "43 topics used in the TREC Deep Learning track Passage Ranking task, with deep judgements",
        "location" : ("trec-deep-learning-passages", "test-2020"),
        "metrics" : ["ndcg_cut_10"], #TODO insert pyterrier.measures
    },
    {
        "name" : "dev.small",
        "desc" : "6800 topics with sparse judgements",
        "location" : ("msmarco_passage", "dev.small"),
        "metrics" : ["recip_rank"],
    },
]

INDEXER_KWARGS={'overwrite' : True}
MAX_DOCNOLEN = 10
MAX_TEXT = 4096

def index(dest_dir, variant='terrier_stemmed'):
    import pyterrier as pt
    dataset = pt.get_dataset('irds:msmarco-passage').get_corpus_iter()

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
    if "text" in variant:
        return [
            ( "bm25_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='BM25')" % (dataset, variant) ),
            ( "bm25_bert_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='BM25', metadata=['docno', 'text']) >> %s" % (dataset, variant, VBERT)  )
        ]
    return [
        ( "bm25_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='BM25')" % (dataset, variant) ),
        ( "dph_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='DPH')" % (dataset, variant) ),
        #( "dph_bo1_" + variant, "dph_%s >> pt.rewrite.Bo1QueryExpansion(pt.get_dataset('%s').get_index('%s')) >> dph_%s" % (variant, dataset, variant, variant) ),
    ]
