

DESTDIR=./indices
vaswani:
	python index.py vaswani terrier_stemmed ${DESTDIR}
	python index.py vaswani terrier_unstemmed ${DESTDIR}
	python index.py vaswani terrier_stemmed_text ${DESTDIR}
	python retrieval_nbs.py indices vaswani terrier_stemmed
	jupyter nbconvert --to notebook --execute  ${DESTDIR}/vaswani/retrieval.ipynb
	mv ${DESTDIR}/vaswani/retrieval.nbconvert.ipynb ${DESTDIR}/vaswani/retrieval.ipynb 
	jupyter nbconvert --to html ${DESTDIR}/vaswani/retrieval.ipynb --output ${DESTDIR}/vaswani/retrieval.html
	
msmarco_passage:
	python index.py msmarco_passage terrier_stemmed ${DESTDIR}
	python index.py msmarco_passage terrier_unstemmed ${DESTDIR}
	python index.py msmarco_passage terrier_stemmed_text ${DESTDIR}
	python index.py msmarco_passage terrier_unstemmed_text ${DESTDIR}

msmarco_document:
	python index.py msmarco_document terrier_stemmed ${DESTDIR}
	python index.py msmarco_document terrier_unstemmed ${DESTDIR}
	python index.py msmarco_document terrier_stemmed_text ${DESTDIR}
	python index.py msmarco_document terrier_unstemmed_text ${DESTDIR}
