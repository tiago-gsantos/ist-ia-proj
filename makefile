# Nome do seu script Python
PYTHON_SCRIPT=seu_programa.py

# Diretório dos testes
TEST_DIR=tests

# Procurar todos os arquivos de input
INPUTS=$(wildcard $(TEST_DIR)/*.txt)

# Para cada arquivo de input, definir o arquivo de output esperado correspondente
OUTPUTS=$(INPUTS:.txt=.out)

# Regra padrão: Executar todos os testes
all: $(patsubst $(TEST_DIR)/%.txt,test-%,$(INPUTS))

# Regra para cada teste individual
test-%: $(TEST_DIR)/%.txt $(TEST_DIR)/%.out
	@echo "Running test $*..."
	@python3 $(PYTHON_SCRIPT) < $(TEST_DIR)/$*.txt > $(TEST_DIR)/$*.tmp
	@if diff -u $(TEST_DIR)/$*.out $(TEST_DIR)/$*.tmp; then \
	    echo "Test $* passed"; \
	else \
	    echo "Test $* failed"; \
	fi
	@rm $(TEST_DIR)/$*.tmp

.PHONY: all $(patsubst $(TEST_DIR)/%.txt,test-%,$(INPUTS))
