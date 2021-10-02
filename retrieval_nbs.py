from pyterrier_prebuilt.msmarco_passage import TOPICS_QRELS
import nbformat as nbf
import pyterrier_prebuilt as pb
from typing import List

def create_notebook(builddir: str, dataset : str, variants : List[str]):

    DATASET_META = pb.get_thing(dataset, 'bla', 'DOC_INFO')
    cells = []
    cell1 = "# PyTerrier demonstration for %s\n\n" % dataset
    meta = pb.get_thing(dataset, "bla", "DOC_INFO")
    cell1 += "This notebook demonstrates retrieval using PyTerrier on the "+ meta["friendlyname"] + " corpus.\n\n"
    cell1 += "About the corpus: " + meta["desc"]

    cells.append(nbf.v4.new_markdown_cell(
        cell1    
    ))
    cells.append(nbf.v4.new_code_cell(
        """
#!pip install -q python-terrier
import pyterrier as pt
if not pt.started():
    pt.init()

from pyterrier.measures import *
dataset = pt.get_dataset('%s')
        """ % dataset))

    TOPICS_QRELS = pb.get_thing(dataset, 'bla', 'TOPICS_QRELS')

    systems = []
    for var in variants:
        if len(variants) > 1:
            variant_desc =  "## Systems using index variant %s" % var
            text = pb.get_thing(dataset, var, 'get_variant_description')(var)
            variant_desc += "\n" + text
            cells.append(nbf.v4.new_markdown_cell(variant_desc))
        
        
        # add any pre-requisite stuff
        syscells = []
        HEADER_LINES = pb.get_thing(dataset, var, 'get_retrieval_head')(dataset, var)
        if HEADER_LINES is not None:
            for line in HEADER_LINES:
                syscells.append(line)
        if len(syscells) > 0:
            cells.append(nbf.v4.new_code_cell(
                "\n".join(syscells)
            ))
        

        syscells = []
        for varname, expression in pb.get_thing(dataset, var, 'get_retrieval_pipelines')(dataset, var):
            # syscells.append("from jnius import JavaException")
            # syscells.append("try:")
            # syscells.append("  %s = %s" % (varname, expression))
            # syscells.append("except JavaException as ja:")
            # syscells.append('  raise ValueError("\\n\\t".join(ja.stacktrace))')
            syscells.append("%s = %s" % (varname, pb.format_pipeline(expression)))
            syscells.append("")

            # keep track of names and variable names
            systems.append(varname)

        cells.append(nbf.v4.new_code_cell(
            "\n".join(syscells)
        ))

    for queryset in TOPICS_QRELS:

        # if we have multiple queryset, we should detail the queryset 
        if "name" in queryset:
            desccell1 = "## Evaluation on %s topics and qrels" % (queryset["name"])
            desccell2 = ""
            if "desc" in queryset:
                desccell2 = "\n%s" % queryset["desc"]

            cells.append(nbf.v4.new_markdown_cell(
                desccell1 + desccell2
            ))
        
        topics_dataset = queryset.get("location", [dataset] )[0]
        topics_variant = queryset.get("location", ["bla", None] )[1:]
        if topics_variant is not None and len(topics_variant) == 1:
            topics_variant = topics_variant[0]
            qrels_variant = topics_variant
        if topics_variant is not None and len(topics_variant) == 2:
            topics_variant, qrels_variant = topics_variant

        if topics_variant is None:
            topics_variant = ''
        else:
            topics_variant = "'%s'" % topics_variant

        if qrels_variant is None:
            qrels_variant = ''
        else:
            qrels_variant = "'%s'" % qrels_variant
        cells.append(nbf.v4.new_code_cell(
            """
pt.Experiment(
    [%s],
    pt.get_dataset('%s').get_topics(%s),
    pt.get_dataset('%s').get_qrels(%s),
    batch_size=200,
    filter_by_qrels=True,
    eval_metrics=%s,
    names=%s)
        """ % (
            ', '.join(systems),
            topics_dataset,
            topics_variant,
            topics_dataset,
            qrels_variant,
            str(queryset.get("metrics", ["map"] )),
            #", ".join( map( lambda s : "'%s'" % s, queryset.get("metrics", ["map"] ) ) ),
            str(systems)
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