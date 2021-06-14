from pyterrier_prebuilt.msmarco_passage import TOPICS_QRELS
import nbformat as nbf
import pyterrier_prebuilt as pb
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

systems=[]
names=[]
dataset = pt.get_dataset('%s')
        """ % dataset))

    TOPICS_QRELS = pb.get_thing(dataset, 'bla', 'TOPICS_QRELS')

    for queryset in TOPICS_QRELS:

        # if we have multiple queryset, we should detail the queryset 
        if "name" in queryset:
            desccell = "## Evaluation for %s topics and qrels\n%s" % (queryset)
            if "desc" in queryset:
                desccell += "\n%s" % queryset["desc"]

            cells.append(nbf.v4.new_markdown_cell(
                desccell
            ))

        for var in variants:
            cells.append(nbf.v4.new_code_cell(
                """
#%s = pt.BatchRetrieve(dataset.get_index(variant='%s'))
%s = pt.BatchRetrieve(dataset.get_index()) # TODO add back %s
systems.append(%s)
names.append(%s)
                """ % (var, var, var, var, var, var)))

        topics_dataset = queryset.get("location", [dataset] )[0]
        topics_variant = queryset.get("location", ["bla", None] )[1]
        if topics_variant is None:
            topics_variant = ''
        else:
            topics_variant = "'%s'" % topics_variant
        cells.append(nbf.v4.new_code_cell(
            """
pt.Experiment(
    systems,
    pt.get_dataset('%s').get_topics(%s),
    pt.get_dataset('%s').get_qrels(%s),
    batch_size=200,
    eval_metrics=[%s],
    names=names)
        """ % (
            topics_dataset,
            topics_variant,
            topics_dataset,
            topics_variant,
            ", ".join( map( lambda s : "'%s'" % s, queryset.get("metrics", ["map"] ) ) )
                ) ))

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
    if len(args) < 4:
        usage(args[0])
        sys.exit(1)
    else:
        builddir=args[1]
        dataset=args[2]
        variants=args[3:]
        create_notebook(builddir, dataset, variants)