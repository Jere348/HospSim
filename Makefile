ANTLR = java -jar /usr/local/lib/antlr-4.13.1-complete.jar

all: generate test

generate:
	$(ANTLR) -Dlanguage=Python3 -visitor -o gen HospSim.g4

test:
	python3 run_tests.py

clean:
	rm -rf gen/*.py gen/*.tokens gen/*.interp */__pycache__ __pycache__
