G4_FILE=HospSim.g4
GEN_DIR=gen

all: generate run

generate:
	antlr4 -Dlanguage=Python3 -visitor -o $(GEN_DIR) $(G4_FILE)

run:
	python3 main.py tests/entrada_correcta.txt

test_error:
	python3 main.py tests/entrada_error.txt

clean:
	rm -rf $(GEN_DIR)/*.py $(GEN_DIR)/*.tokens $(GEN_DIR)/*.interp __pycache__ semantic/__pycache__
