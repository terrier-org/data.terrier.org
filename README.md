# data.terrier.org

This repository contains the source code for the (Py)Terrier Data Repository - http://data.terrier.org.

In particular, it contains the Python scripts to build indices for well-known test collections, as well as to create and execute notebooks to document the known performances of those indices.

## Features

 - Builds Terrier indices (and those from other PyTerrier plugsin, such as [pyterrier_colbert](https://github.com/terrierteam/pyterrier_colbert)) available for standard corpora via PyTerrier, hosted on a publicly accessible website
 - Indices are versioned, and are verifiably correct, e.g. through md5sums
 - PyTerrier code snippets are provided for instantiating different PyTerrier retrieval pipelines
 - There are notebooks demonstrating retrieval effectiveness of using these pre-built indices can be made available, with pre-populated results. For many corpora, these indices are small enough to allow running on [Google Colab](https://colab.research.google.com/).

## Accessing a prebuilt index

Different PyTerrier retrieval transformers can intantiated via a `from_dataset()` function. If necsssary, this downloads and verifies the index from http://data.terrier.org.

```python
name='msmarco-passage'
variant='stemmed'
br = pt.TerrierRetrieve.from_dataset(name, variant)
#or equivalently
br = pt.TerrierRetrieve(pt.get_dataset(name).get_index(variant=variant))
```

## Building an Index

The Terrier Data Repository means that you should not required to build indices that are available through the repository. 

However, should you wish to contribute an index, you can see how indices are built using the Makefile, and specifying the dataset name:

```shell
make vaswani
```

All vaswani indices are then built into indices/vaswani/:
```shell
$ ls indices/vaswani 
terrier_stemmed         terrier_stemmed_text    terrier_unstemmed

$ ls indices/vaswani/terrier_stemmed/latest
data.direct.bf                  data.lexicon.fsomapfile         data.meta.idx                   md5sums
data.document.fsarrayfile       data.lexicon.fsomaphash         data.meta.zdata                 files
data.inverted.bf                data.lexicon.fsomapid           data.properties
```


## Credits

 - Craig Macdonald, University of Glasgow
 - Sean MacAvaney, University of Glasgow
