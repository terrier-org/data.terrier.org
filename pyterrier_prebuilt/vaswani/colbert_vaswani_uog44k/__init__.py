
INDEXER_KWARGS={'overwrite' : True}

def index(dest_dir, variant=None):
    import pyterrier as pt
    import os
    dataset = pt.get_dataset("vaswani").get_corpus_iter()

    from pyterrier_colbert.indexing import ColBERTIndexer
    checkpoint="http://www.dcs.gla.ac.uk/~craigm/colbert.dnn.zip"

    indexer = ColBERTIndexer(checkpoint, os.path.dirname(dest_dir),os.path.basename(dest_dir), chunksize=3)
    indexer.index(dataset)
