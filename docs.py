from staticjinja import Site
import sys
import os

INDEX_DIR="./indices/"

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
	datasets = ["vaswani", "msmarco_document", "msmarco_passage"]
	for d in datasets:
		meta = pb.get_thing(d, "bla", "DOC_INFO")
		meta["name"] = d
		config["datasets"].append(meta)
		variants = pb.get_variants(d, INDEX_DIR)
		meta["variants"] = []
		meta["lastupdate"] = "(unknown)"

		meta["notebook_present"] = os.path.exists(os.path.join(INDEX_DIR, d, "retrieval.html"))

		for v in variants:
			vmeta = {
				"name" : v,
				"desc" : pb.get_thing(d, v, 'get_variant_description')(v),
			}
			vmeta["lastupdate"] = variant_date(d, v)
			if vmeta["lastupdate"] >  meta["lastupdate"]:
				meta["lastupdate"] = vmeta["lastupdate"]
			meta["variants"].append(vmeta)
		meta["variant_count"] = len(variants)
		print(meta)

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
