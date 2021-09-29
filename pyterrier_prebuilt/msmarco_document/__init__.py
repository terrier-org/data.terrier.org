from typing import List
import itertools
from pyterrier.measures import *
VBERT = "onir_pt.reranker('hgf4_joint',  text_field='body', ranker_config={'model': 'Capreolus/bert-base-msmarco', 'norm': 'softmax-2'})"
SLIDING = "pt.text.sliding(length=128, stride=64, prepend_attr='title')"
MAXP = "pt.text.max_passage()"
DOC_INFO = {
    "friendlyname" : "MSMARCO Document Ranking",
    "desc" : "A document ranking corpus containing 3.2 million documents. Also used by the TREC Deep Learning track.",
}

INDEXER_KWARGS={'overwrite' : True}
MAX_DOCNOLEN = 10
MAX_TEXT = 4096
MAX_TITLE = 256

TOPICS_QRELS = [
    {
        "name" : "trec-2019",
        "desc" : "43 topics used in the TREC 2019 Deep Learning track Document Ranking task, with deep judgements",
        "location" : ("msmarco_document", "test"),
        "metrics" : [RR, nDCG@10, nDCG@100, AP],
    },
    {
        "name" : "trec-2020",
        "desc" : "45 topics used in the TREC 2020 Deep Learning track Document Ranking task, with deep judgements",
        "location" : ("msmarco_document", "test-2020"),
        "metrics" : [RR, nDCG@10, nDCG@100, AP],
    },
    {
        "name" : "dev",
        "desc" : "5193 topics with sparse judgements",
        "location" : ("msmarco_document", "dev"),
        "metrics" : [RR],
    },
]

def index(dest_dir, variant='terrier_stemmed'):
    import pyterrier as pt
    dataset = pt.get_dataset('irds:msmarco-document').get_corpus_iter()

    init_args = INDEXER_KWARGS.copy()
    index_args = {}
    props = {}
    index_args['meta']={'docno' : MAX_DOCNOLEN}
    index_args['fields']=['title', 'body']

    if variant.startswith('terrier_unstemmed'):
        props["termpipelines"] = ""
        
    if variant.endswith('text'):
        index_args['meta']['body'] = MAX_TEXT
        index_args['meta']['title'] = MAX_TITLE
    
    indexer = pt.IterDictIndexer(dest_dir, **init_args)
    for k,v in props.items():
        indexer.setProperty(k, v)
    indexref = indexer.index(dataset, **index_args)

def get_variant_description(variant : str) -> str:
    import pyterrier_prebuilt as pb
    return pb.get_default_variant_description(variant)

def get_retrieval_head(dataset : str, variant : str) -> List[str]:
    if "text" in variant:
        return [
            '#!pip install git+https://github.com/Georgetown-IR-Lab/OpenNIR.git',
            'import onir_pt',
            '# Lets use a Vanilla BERT ranker from OpenNIR. We\'ll use the Capreolus model available from Huggingface',
            'vanilla_bert = %s' % VBERT
        ]

def get_retrieval_pipelines(dataset : str, variant : str) -> List[str]:
    if "text" in variant:
        return [
            #( "bm25_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='BM25', num_results=100)" % (dataset, variant) ),
            ( "bm25_bert_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='BM25', metadata=['docno', 'title', 'body'], num_results=100) >> %s >> %s >> %s" % 
                (dataset, variant, SLIDING, 'vanilla_bert', MAXP)  )
        ]
    else:
        return [
            ( "bm25_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='BM25', num_results=100)" % (dataset, variant) ),
            ( "dph_" + variant, "pt.BatchRetrieve.from_dataset('%s', '%s', wmodel='DPH', num_results=100)" % (dataset, variant) ),
            ( "dph_bo1_" + variant, "dph_%s >> pt.rewrite.Bo1QueryExpansion(pt.get_dataset('%s').get_index('%s')) >> dph_%s" % (variant, dataset, variant, variant) ),
        ]
