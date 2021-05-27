

DESTDIR=./indices
vaswani:
	python index.py vaswani terrier_stemmed ${DESTDIR}
	python index.py vaswani terrier_unstemmed ${DESTDIR}
	python index.py vaswani terrier_stemmed_text ${DESTDIR}
	
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
