def get_thing(dataset : str, variant : str, name : str):
    import importlib, os
    module_name = "pyterrier_prebuilt.%s.%s" % (dataset, variant)
    kwargs={}
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        module_name = "pyterrier_prebuilt.%s" % (dataset)
        module = importlib.import_module(module_name)
        kwargs['variant'] = variant
    if hasattr(module, name):
        return getattr(module, name)
    return None
    
def get_variants(dataset : str, builddir : str):
    import os
    datasetdir = os.path.join(builddir, dataset)
    rtr = []
    for variant in os.listdir(datasetdir):
        variant_latest_dir = os.path.join(datasetdir, variant, "latest")
        if not os.path.exists(variant_latest_dir):
            continue
        if variant == 'default':
            # its a symlink
            continue
        rtr.append(variant)
    return rtr

def get_default_variant_description(variant : str) -> str:
    if variant == "terrier_unstemmed_text":
        return "Terrier index, no stemming, no stopword removal. Text is also saved in the MetaIndex to facilitate BERT-based reranking."
    if variant == "terrier_unstemmed":
        return "Terrier index, no stemming, no stopword removal."
    if variant == "terrier_unstemmed_positions":
        return "Terrier index, no stemming, no stopword removal. Position information is saved for proximity or phrase queries."
    if variant == "terrier_stemmed":
        return "Terrier's default Porter stemming, and stopwords removed."
    if variant == "terrier_stemmed_text":
        return "Terrier's default Porter stemming, and stopwords removed. Text is also saved in the MetaIndex to facilitate BERT-based reranking."
    if variant == "terrier_stemmed_positions":
        return "Terrier index, default Porter stemming, and stopwords removed. Position information is saved for proximity or phrase queries."
    return "unknown variant"