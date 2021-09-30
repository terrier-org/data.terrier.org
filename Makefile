
PWD=$(shell pwd)
DATE=$(shell date +'%Y-%m-%d')
PYTHON=/users/tr.craigm/anaconda3/envs/pyterrier/bin/python
NBCONVERT=jupyter nbconvert --ExecutePreprocessor.kernel_name=pyterrier --ExecutePreprocessor.timeout=-1
DESTDIR=./indices
vaswani:
	#${PYTHON} index.py vaswani terrier_stemmed ${DESTDIR}
	#${PYTHON} index.py vaswani terrier_unstemmed ${DESTDIR}
	#${PYTHON} index.py vaswani terrier_stemmed_text ${DESTDIR}
	${PYTHON} retrieval_nbs.py indices vaswani terrier_stemmed
	${NBCONVERT} --to notebook --execute  ${DESTDIR}/vaswani/retrieval.ipynb
	mv ${DESTDIR}/vaswani/retrieval.nbconvert.ipynb ${DESTDIR}/vaswani/retrieval.ipynb 
	${NBCONVERT} --to html ${DESTDIR}/vaswani/retrieval.ipynb --output retrieval.html
	#${PYTHON} promote_index.py vaswani ${DATE} ${DESTDIR}
	
msmarco_passage:
	#${PYTHON} index.py msmarco_passage terrier_stemmed ${DESTDIR}
	#${PYTHON} index.py msmarco_passage terrier_unstemmed ${DESTDIR}
	#${PYTHON} index.py msmarco_passage terrier_stemmed_text ${DESTDIR}
	#${PYTHON} index.py msmarco_passage terrier_unstemmed_text ${DESTDIR}
	#${PYTHON} index.py msmarco_passage terrier_stemmed_docT5query ${DESTDIR}
	#${PYTHON} index.py msmarco_passage terrier_stemmed_deepct ${DESTDIR}
	#${PYTHON} promote_index.py msmarco_passage ${DATE} ${DESTDIR}
	#mkdir -p pyt_home/corpora/msmarco_passage/index/
	#bash -c 'for i in  $PWD/indices/msmarco_passage/*/latest; do VARNAME=`dirname $i| xargs basename `; ln -s $i pyt_home/corpora/msmarco_passage/index/$VARNAME; done'
	${PYTHON} retrieval_nbs.py indices msmarco_passage terrier_stemmed terrier_stemmed_docT5query terrier_stemmed_deepct
	#PYTERRIER_HOME=${PWD}/pyt_home/ ${NBCONVERT} --to notebook --execute  ${DESTDIR}/msmarco_passage/retrieval.ipynb
	${NBCONVERT} --to html ${DESTDIR}/msmarco_passage/retrieval.ipynb --output retrieval.html

msmarco_document:
	${PYTHON} index.py msmarco_document terrier_stemmed ${DESTDIR}
	${PYTHON} index.py msmarco_document terrier_unstemmed ${DESTDIR}
	${PYTHON} index.py msmarco_document terrier_stemmed_text ${DESTDIR}
	${PYTHON} index.py msmarco_document terrier_unstemmed_text ${DESTDIR}
	${PYTHON} index.py msmarco_document terrier_stemmed_docT5query ${DESTDIR}

msmarcov2_document:
	${PYTHON} index.py msmarcov2_document terrier_stemmed ${DESTDIR}
	${PYTHON} index.py msmarcov2_document terrier_stemmed_positions ${DESTDIR}
	${PYTHON} index.py msmarcov2_document terrier_unstemmed ${DESTDIR}
	${PYTHON} index.py msmarcov2_document terrier_unstemmed_positions ${DESTDIR}
	${PYTHON} promote_index.py msmarcov2_document ${DATE} ${DESTDIR}

trec-covid:
	${PYTHON} index.py trec-covid terrier_stemmed ${DESTDIR}
	${PYTHON} index.py trec-covid terrier_unstemmed ${DESTDIR}
	${PYTHON} index.py trec-covid terrier_stemmed_text ${DESTDIR}
	${PYTHON} index.py trec-covid terrier_unstemmed_text ${DESTDIR}
	${PYTHON} index.py trec-covid terrier_stemmed_positions ${DESTDIR}
	${PYTHON} index.py trec-covid terrier_unstemmed_positions ${DESTDIR}
	${PYTHON} index.py trec-covid terrier_stemmed_doct5query ${DESTDIR}
	${PYTHON} index.py trec-covid terrier_stemmed_doct5query_text ${DESTDIR}
	${PYTHON} promote_index.py trec-covid ${DATE} ${DESTDIR}
	${PYTHON} retrieval_nbs.py indices trec-covid terrier_stemmed terrier_unstemmed
	PYTERRIER_HOME=${PWD}/pyt_home/ ${NBCONVERT} --to notebook --execute  ${DESTDIR}/trec-covid/retrieval.ipynb

docs:
	${PYTHON} docs.py
