clean:
	rm -Rf venv lambda.zip

virtualenv:
	virtualenv --no-site-packages venv
	venv/bin/pip install -r requirements.txt

zip: clean virtualenv
	rm -f lambda.zip
	zip lambda.zip *.py
	cd venv/lib/python2.7/site-packages/; zip -r ../../../../lambda.zip *
