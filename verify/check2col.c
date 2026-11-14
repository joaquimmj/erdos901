/* check2col: exhaustive 2-colourability test for a uniform hypergraph.
 *
 * Input file: one edge per line, vertices as non-negative integers
 * (whitespace separated). Lines starting with '#' are ignored.
 * Vertex count v = max vertex + 1 (must be <= 40 for brute force).
 *
 * Enumerates all 2^(v-1) colourings (vertex v-1 fixed to colour 0, which
 * loses nothing by red/blue symmetry). An edge e is monochromatic under
 * colouring c iff (c & e) == 0 or (c & e) == e.
 *
 * Output (stdout):
 *   NON-2-COLORABLE v=<v> E=<E> n=<n>     (exit code 0)
 *   PROPER <mask>  v=<v> E=<E> n=<n>      (exit code 1)  mask = colour-1 vertices
 * Exit code 2 on input error.
 *
 * Independent of the search code on purpose: no shared sources.
 * Build: cc -O3 -march=native -fopenmp check2col.c -o check2col
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <ctype.h>

#define MAXE 2000000

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: %s edges.txt\n", argv[0]); return 2; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 2; }
    uint64_t *E = malloc(sizeof(uint64_t) * MAXE);
    int ne = 0, maxv = -1, n = -1;
    char line[4096];
    while (fgets(line, sizeof line, f)) {
        char *p = line;
        while (isspace((unsigned char)*p)) p++;
        if (*p == '#' || *p == 0) continue;
        uint64_t m = 0; int cnt = 0;
        char *tok = strtok(p, " \t\r\n,");
        while (tok) {
            long x = strtol(tok, NULL, 10);
            if (x < 0 || x >= 64) { fprintf(stderr, "vertex out of range: %ld\n", x); return 2; }
            if (m & (1ULL << x)) { fprintf(stderr, "repeated vertex in edge\n"); return 2; }
            m |= 1ULL << x; cnt++;
            if (x > maxv) maxv = (int)x;
            tok = strtok(NULL, " \t\r\n,");
        }
        if (n < 0) n = cnt;
        else if (cnt != n) { fprintf(stderr, "not uniform: edge of size %d vs %d\n", cnt, n); return 2; }
        for (int i = 0; i < ne; i++) if (E[i] == m) { fprintf(stderr, "duplicate edge\n"); return 2; }
        if (ne >= MAXE) { fprintf(stderr, "too many edges\n"); return 2; }
        E[ne++] = m;
    }
    fclose(f);
    int v = maxv + 1;
    if (ne == 0) { printf("PROPER 0 v=0 E=0 n=0\n"); return 1; }
    if (v > 40) { fprintf(stderr, "v=%d too large for brute force (max 40)\n", v); return 2; }

    uint64_t total = 1ULL << (v - 1);   /* vertex v-1 always colour 0 */
    volatile int found = 0;
    uint64_t witness = 0;

    #pragma omp parallel for schedule(dynamic, 65536) shared(found, witness)
    for (uint64_t c = 0; c < total; c++) {
        if (found) continue;
        int proper = 1;
        for (int i = 0; i < ne; i++) {
            uint64_t x = c & E[i];
            if (x == 0 || x == E[i]) { proper = 0; break; }
        }
        if (proper) {
            #pragma omp critical
            { if (!found) { found = 1; witness = c; } }
        }
    }
    if (found) {
        printf("PROPER %llu v=%d E=%d n=%d\n", (unsigned long long)witness, v, ne, n);
        return 1;
    }
    printf("NON-2-COLORABLE v=%d E=%d n=%d\n", v, ne, n);
    return 0;
}
