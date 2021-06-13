from staticjinja import Site
import sys

if __name__ == "__main__":
	args = sys.argv
	config = {
		"datasets" : [ 
			{
				"friendlyname" : "Vaswani",
				"name" : "vaswani",
				"desc" : "The Vaswani NPL corpus is a small test collection of 11,000 abstracts has been used by the Glasgow IR group for many years (created 1990). "+
					"Due to its small size, it is used for many test cases used in both Terrier and PyTerrier.",
				"lastupdate" : "unknown",
				"variants" : [
					{
						"name" : "terrier_stemmed",
						"desc" : "Terrier's default Porter stemming, and stopwords removed",
						"lastupdate" : "today!",
					},
					{
						"name" : "terrier_stemmed_text",
						"desc" : "Terrier's default Porter stemming, and stopwords removed. Text is also saved in the MetaIndex.",
						"lastupdate" : "today!",
					},
					{
						"name" : "terrier_unstemmed",
						"desc" : "Terrier index, no stemming",
						"lastupdate" : "today!",
					},
				],
			},

			{
				"friendlyname" : "MSMARCO Passage Ranking",
				"name" : "msmarco_passage",
				"desc" : "A passage ranking task based on a corpus of 8.8 million passages released by Microsoft, which should be rank based on their relevance to questions.  Also used by the TREC Deep Learning track.",
				"lastupdate" : "unknown",
				"variants" : [
					{
						"name" : "terrier_stemmed",
						"desc" : "Terrier's default Porter stemming, and stopwords removed",
						"lastupdate" : "today!",
					},
					{
						"name" : "terrier_stemmed_text",
						"desc" : "Terrier's default Porter stemming, and stopwords removed. Text is also saved in the MetaIndex to facilitate BERT-based reranking.",
						"lastupdate" : "today!",
					},
					{
						"name" : "terrier_unstemmed",
						"desc" : "Terrier index, no stemming, no stopword removal",
						"lastupdate" : "today!",
					},
					{
						"name" : "terrier_unstemmed_text",
						"desc" : "Terrier's index, no stemming, no stopword removal. Text is also saved in the MetaIndex to facilitate BERT-based reranking.",
						"lastupdate" : "today!",
					},
					{
						"name" : "terrier_stemmed_deepct",
						"desc" : "Terrier index using DeepCT. Porter stemming and stopword removal applied",
						"lastupdate" : "today!",
					},
					{
						"name" : "terrier_stemmed_docT5query",
						"desc" : "Terrier index using docT5query. Porter stemming and stopword removal applied",
						"lastupdate" : "today!",
					},
				],
			},

			{
				"friendlyname" : "MSMARCO Document Ranking",
				"name" : "msmarco_document",
				"desc" : "A document ranking corpus containing 3.2 million documents. Also used by the TREC Deep Learning track.",
				"lastupdate" : "unknown",
				"variants" : [
					{
						"name" : "terrier_stemmed",
						"desc" : "Terrier's default Porter stemming, and stopwords removed",
						"lastupdate" : "today!",
					},
					{
						"name" : "terrier_stemmed_text",
						"desc" : "Terrier's default Porter stemming, and stopwords removed. Text is also saved in the MetaIndex to facilitate BERT-based reranking.",
						"lastupdate" : "today!",
					},
					{
						"name" : "terrier_unstemmed",
						"desc" : "Terrier index, no stemming, no stopword removal",
						"lastupdate" : "today!",
					},
					{
						"name" : "terrier_unstemmed_text",
						"desc" : "Terrier index, no stemming, no stopword removal. Text is also saved in the MetaIndex to facilitate BERT-based reranking.",
						"lastupdate" : "today!",
					},
					{
						"name" : "terrier_stemmed_docT5query",
						"desc" : "Terrier index using docT5query. Porter stemming and stopword removal applied",
						"lastupdate" : "today!",
					},
				],
			}
		]
	}

	configmap = { d["name"] : d for d in config["datasets"] }
	for k in configmap:
		configmap[k]["variant_count"] = len(configmap[k]["variants"])

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
