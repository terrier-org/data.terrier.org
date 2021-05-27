# pyterrier_prebuilt

This repository provides a tool to build standard indices for freely available corpora.


## Requirements:

 - MH: To make Terrier indices available for standard corpora via PyTerrier, hosted on a publicly accessible website
 - SH: To make non-Terrier indices available
 - SH: To have indices versioned, but still able to request latest index
 - SH: Indices should be verifiably correct, e.g. through md5sums
 - SH: Notebooks demonstrating retrieval effectiveness of using these pre-built indices can be made available, with pre-populated results

## Usage:

Initial operated through a Makefile,  specifying the dataset name:

```shell
make vaswani
```

All vaswani indices are then built into indices/vaswani/:
```shell
$ ls indices/vaswani 
terrier_stemmed         terrier_stemmed_text    terrier_unstemmed

$ ls indices/vaswani/terrier_stemmed
data.direct.bf                  data.lexicon.fsomapfile         data.meta.idx                   md5sums
data.document.fsarrayfile       data.lexicon.fsomaphash         data.meta.zdata
data.inverted.bf                data.lexicon.fsomapid           data.properties
```


## Accessing a prebuilt index.

This is planned to become as easy as:
```python
name='msmarco-passage'
variant='stemmed'
br = pt.BatchRetrieve.from_dataset(name, variant)
#or equivalently
br = pt.BatchRetrieve(pt.get_dataset(name).get_index(variant=variant))

```


## Credits

 - Craig Macdonald, University of Glasgow