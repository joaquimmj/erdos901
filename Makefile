CC ?= cc
CFLAGS ?= -O3 -march=native -fopenmp

all: verify/check2col search/oracle

search/oracle: search/oracle.c
	$(CC) -O3 -march=native $< -o $@

verify/check2col: verify/check2col.c
	$(CC) $(CFLAGS) $< -o $@

test: all
	bash verify/tests.sh

clean:
	rm -f verify/check2col
