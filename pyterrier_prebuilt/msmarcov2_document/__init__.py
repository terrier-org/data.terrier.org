
VBERT = "onir_pt.reranker('hgf4_joint', ranker_config={'model': 'Capreolus/bert-base-msmarco', 'norm': 'softmax-2'}"
SLIDING = "pt.text.sliding(length=128, stride=64, prepend_attr='title')"
DOC_INFO = {
    "friendlyname" : "MSMARCOv2 Document Ranking",
    "desc" : "A new version of the MSMARCO document ranking corpus, containing 11.9 million documents. Also used by the TREC 2021 Deep Learning track.",
}

TOPICS_QRELS = [
    {
        "name" : "valid1",
        "desc" : "43 topics used in the TREC 2019 Deep Learning track, with deep judgements",
        "location" : ("msmarcov2_document", "valid1"),
        "metrics" : ["ndcg_cut_10"], #TODO insert pyterrier.measures
    },
    {
        "name" : "valid2",
        "desc" : "54 topics used in the TREC 2020 Deep Learning track, with deep judgements",
        "location" : ("msmarcov2_document", "valid2"),
        "metrics" : ["ndcg_cut_10"], #TODO insert pyterrier.measures
    },
    {
        "name" : "dev1",
        "desc" : "4,552 topics with sparse judgements",
        "location" : ("msmarcov2_document", "dev1"),
        "metrics" : ["recip_rank"],
    },
]

INDEXER_KWARGS={'overwrite' : True, 'threads': 8}
MAX_DOCNOLEN = 25
MAX_TEXT = 4096

def index(dest_dir, variant='terrier_stemmed'):
    import pyterrier as pt
    dataset = pt.get_dataset('irds:msmarco-document-v2').get_corpus_iter()

    init_args = INDEXER_KWARGS.copy()
    index_args = {'fields':['url', 'title', 'headings', 'body']}
    props = {}
    init_args['meta']={'docno' : MAX_DOCNOLEN}

    if 'positions' in variant:
        init_args['blocks'] = True

    if variant.startswith('terrier_unstemmed'):
        props["termpipelines"] = ""
        
    if variant.endswith('text'):
        init_args['meta']['text'] = MAX_TEXT
        init_args['meta_tags'] = {'text' : 'ELSE'}
    
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
            ( "bm25_bert_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='BM25', metadata=['docno', 'text']) >> %s >> %s" % (dataset, variant, SLIDING, VBERT)  )
        ]
    else:
        return [
            ( "bm25_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='BM25')" % (dataset, variant) ),
            ( "dph_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='DPH')" % (dataset, variant) ),
            ( "dph_bo1_" + variant, "dph_%s >> pt.rewrite.Bo1QueryExpansion(pt.get_dataset('%s').get_index('%s')) >> dph_%s" % (variant, dataset, variant, variant) ),
        ]
