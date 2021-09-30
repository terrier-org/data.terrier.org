from staticjinja import Site
from pygments import highlight, token
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import sys
import os
import markdown

INDEX_DIR="./indices/"

class PythonFunctionLexer(PythonLexer):
    def get_tokens(self, s):
        # A version of PythonLexer that also highlights functions when they are called
        it = super().get_tokens(s)
        prev = next(it)
        for tok in it:
            if prev[0] == token.Name and tok == (token.Punctuation, '('):
                yield prev[0].Function, prev[1]
            else:
                yield prev
            prev = tok
        yield prev

def python_pprint(code):
	return highlight(code, PythonFunctionLexer(ensurenl=False), HtmlFormatter(nowrap=True)).replace('\n', '<br/>')

def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def dirsize(path):
	import os
	#initialize the size
	total_size = 0

	#use the walk() method to navigate through directory tree
	for dirpath, dirnames, filenames in os.walk(path):
		for i in filenames:
			
			#use join to concatenate all the components of path
			f = os.path.join(dirpath, i)
			
			#use getsize to generate size in bytes and add it to the total size
			total_size += os.path.getsize(f)
	return total_size

def variant_size(dataset, variant):
	import os
	symlink_path = os.path.join(INDEX_DIR, dataset, variant, "latest")
	return sizeof_fmt(dirsize(symlink_path))

def variant_date(dataset, variant):
	import os
	symlink_path = os.path.join(INDEX_DIR, dataset, variant, "latest")
	dest = os.path.realpath(symlink_path)
	return os.path.basename(dest)

if __name__ == "__main__":
	args = sys.argv
	config = {
		"datasets" : []
	}

	import pyterrier_prebuilt as pb
	datasets = ["vaswani", "msmarco_document", "msmarco_passage", "msmarcov2_document", "msmarcov2_passage", "trec-covid"]
	for d in datasets:
		print("Dataset %s" % d)
		meta = pb.get_thing(d, "bla", "DOC_INFO")
		meta["name"] = d
		meta["desc"] = markdown.markdown(meta["desc"])
		config["datasets"].append(meta)
		variants = pb.get_variants(d, INDEX_DIR)
		meta["variants"] = []
		meta["lastupdate"] = "(unknown)"

		notebook_loc = os.path.join(INDEX_DIR, d, "retrieval.html")
		meta["notebook_present"] = os.path.exists(notebook_loc)
		print("Notebook found at %s: %s" % (notebook_loc, meta["notebook_present"]))

		for v in variants:
			print("Variant %s" % v)
			vmeta = {
				"name" : v,
				"desc" : markdown.markdown(pb.get_thing(d, v, 'get_variant_description')(v)),
				"pipes_header" : pb.get_thing(d, v, 'get_retrieval_head')(d,v),
				"pipes" : pb.get_thing(d, v, 'get_retrieval_pipelines')(d,v)
			}
			if vmeta["pipes_header"] is None:
				vmeta["pipes_header"] = []
			vmeta['example'] = python_pprint('\n\n'.join(
				vmeta["pipes_header"]
				+
				[f'{l} = {r}' for l, r in vmeta['pipes']]
				))
			vmeta["lastupdate"] = variant_date(d, v)
			vmeta["size"] = variant_size(d, v)
			# our string dates sort lexographically
			if vmeta["lastupdate"] > meta["lastupdate"]:
				meta["lastupdate"] = vmeta["lastupdate"]
			meta["variants"].append(vmeta)
		meta["variant_count"] = len(variants)
		#print(meta)

	configmap = { d["name"] : d for d in config["datasets"] }

	def get_dataset_context(template):
		import os
		print(template.filename)
		filename = os.path.basename(template.filename)
		if not ".dataset.html" in filename:
			return {}
		datasetname = filename.split(".")[0]		
		return {"dataset" : configmap[datasetname]}

	site = Site.make_site(
		outpath='wwwroot/', 
		env_globals=config,
		contexts=[('.*.dataset.html', get_dataset_context)], )
	if args[0] == '--reload':
		site.render(use_reloader=True)
	else:
		site.render()
