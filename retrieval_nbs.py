import nbformat as nbf
from typing import List

def create_notebook(builddir: str, dataset : str, variants : List[str]):

    cells = []
    cells.append(nbf.v4.new_markdown_cell(
        "# PyTerrier demonstration for %s" % dataset
    ))
    cells.append(nbf.v4.new_code_cell(
        """
import pyterrier as pt
if not pt.started():
    pt.init()

dataset = pt.get_dataset('%s')

systems=[]
names=[]
        """ % dataset))
    for var in variants:
        cells.append(nbf.v4.new_code_cell(
            """
#%s = pt.BatchRetrieve(dataset.get_index(variant='%s'))
%s = pt.BatchRetrieve(dataset.get_index()) # TODO add back %s
systems.append(%s)
names.append(%s)
            """ % (var, var, var, var, var, var)))
    cells.append(nbf.v4.new_code_cell(
        """
pt.Experiment(
    systems,
    dataset.get_topics(),
    dataset.get_qrels(),
    batch_size=200,
    eval_metrics=["map"],
    names=names)
        """))

    nb = nbf.v4.new_notebook()
    nb['cells'] = cells
    fname = '%s/%s/retrieval.ipynb' % (builddir, dataset)  

    with open(fname, 'w') as f:
        nbf.write(nb, f)

def usage(name):
    print("Usage:")
    print("%s builddir dataset variantnames..." % name)

if __name__ == '__main__':
    import sys
    args = sys.argv
    if len(args) != 4:
        usage(args[0])
    else:
        builddir=args[1]
        dataset=args[2]
        variants=args[3:]
        create_notebook(builddir, dataset, variants)