.PHONY: dev
dev:
	py src/main.py

.PHONY: test
test:
	py src/test.py

.PHONY: build
build:
	py src/build.py


.PHONY: compile
compile:
	gcc -o cache/main cache/main.c -lm && ./cache/main 

