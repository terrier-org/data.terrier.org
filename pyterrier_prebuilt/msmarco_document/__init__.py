
VBERT = "onir_pt.reranker('hgf4_joint', ranker_config={'model': 'Capreolus/bert-base-msmarco', 'norm': 'softmax-2'}"
SLIDING = "pt.text.sliding(length=128, stride=64, prepend_attr='title')"
DOC_INFO = {
    "friendlyname" : "MSMARCO Document Ranking",
    "desc" : "A document ranking corpus containing 3.2 million documents. Also used by the TREC Deep Learning track.",
}

INDEXER_KWARGS={'overwrite' : True}
MAX_DOCNOLEN = 10
MAX_TEXT = 4096

def index(dest_dir, variant='terrier_stemmed'):
    import pyterrier as pt
    dataset = pt.get_dataset('trec-deep-learning-docs').get_corpus()

    init_args = INDEXER_KWARGS.copy()
    index_args = {}
    props = {}
    init_args['meta']={'docno' : MAX_DOCNOLEN}

    if variant.startswith('terrier_unstemmed'):
        props["termpipelines"] = ""
        
    if variant.endswith('text'):
        init_args['meta']['text'] = MAX_TEXT
        init_args['meta_tags'] = {'text' : 'ELSE'}
    
    indexer = pt.TRECCollectionIndexer(dest_dir, **init_args)
    for k,v in props.items():
        indexer.setProperty(k, v)
    indexref = indexer.index(dataset, **index_args)

def get_variant_description(variant : str) -> str:
    import pyterrier_prebuilt as pb
    return pb.get_default_variant_description(variant)

def get_retrieval_head(dataset : str, variant : str) -> str:
    if "text" in variant:
        return [
            'import onir_pt',
            '# Lets use a Vanilla BERT ranker from OpenNIR. We\'ll use the Capreolus model available from Huggingface',
            'vanilla_bert = %s' % VBERT
        ]

def get_retrieval_pipelines(dataset : str, variant : str) -> str:
    if "text" in variant:
        return [
            ( "bm25_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='BM25')" % (dataset, variant) ),
            ( "bm25_bert_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='BM25', metadata=['docno', 'text']) >> %s >> %s" % (dataset, variant, SLIDING, 'vanilla_bert')  )
        ]
    else:
        return [
            ( "bm25_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='BM25')" % (dataset, variant) ),
            ( "dph_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='DPH')" % (dataset, variant) ),
            ( "dph_bo1_" + variant, "dph_%s >> pt.rewrite.Bo1QueryExpansion(pt.get_dataset('%s').get_index('%s')) >> dph_%s" % (variant, dataset, variant, variant) ),
        ]
