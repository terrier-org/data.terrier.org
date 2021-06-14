
DATE=$(shell date +'%Y-%m-%d')
PYTHON=/users/tr.craigm/anaconda3/envs/pyterrier/bin/python
NBCONVERT=jupyter nbconvert --ExecutePreprocessor.kernel_name=pyterrier
DESTDIR=./indices
vaswani:
	#${PYTHON} index.py vaswani terrier_stemmed ${DESTDIR}
	#${PYTHON} index.py vaswani terrier_unstemmed ${DESTDIR}
	#${PYTHON} index.py vaswani terrier_stemmed_text ${DESTDIR}
	#${PYTHON} retrieval_nbs.py indices vaswani terrier_stemmed
	#${NBCONVERT} --to notebook --execute  ${DESTDIR}/vaswani/retrieval.ipynb
	#mv ${DESTDIR}/vaswani/retrieval.nbconvert.ipynb ${DESTDIR}/vaswani/retrieval.ipynb 
	#${NBCONVERT} --to html ${DESTDIR}/vaswani/retrieval.ipynb --output retrieval.html
	${PYTHON} promote_index.py vaswani ${DATE} ${DESTDIR}
	
msmarco_passage:
	${PYTHON} index.py msmarco_passage terrier_stemmed ${DESTDIR}
	${PYTHON} index.py msmarco_passage terrier_unstemmed ${DESTDIR}
	${PYTHON} index.py msmarco_passage terrier_stemmed_text ${DESTDIR}
	${PYTHON} index.py msmarco_passage terrier_unstemmed_text ${DESTDIR}
	${PYTHON} index.py msmarco_passage terrier_stemmed_docT5query ${DESTDIR}
	${PYTHON} index.py msmarco_passage terrier_stemmed_deepct ${DESTDIR}

msmarco_document:
	${PYTHON} index.py msmarco_document terrier_stemmed ${DESTDIR}
	${PYTHON} index.py msmarco_document terrier_unstemmed ${DESTDIR}
	${PYTHON} index.py msmarco_document terrier_stemmed_text ${DESTDIR}
	${PYTHON} index.py msmarco_document terrier_unstemmed_text ${DESTDIR}
	${PYTHON} index.py msmarco_document terrier_stemmed_docT5query ${DESTDIR}

docs:
	${PYTHON} docs.py
