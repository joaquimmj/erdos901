/* oracle: list up to K proper 2-colourings (brute force, vertex v-1 = colour 0).
 * Search-side helper (NOT the verifier). Usage: oracle edges.txt K
 * Output: one mask per line; empty output = non-2-colourable. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <ctype.h>
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); int K=atoi(argv[2]);
  uint64_t E[200000]; int ne=0,maxv=-1; char line[4096];
  while(fgets(line,sizeof line,f)){char*p=line;while(isspace((unsigned char)*p))p++;if(!*p||*p=='#')continue;
    uint64_t m=0;char*t=strtok(p," \t\r\n,");while(t){long x=strtol(t,0,10);m|=1ULL<<x;if(x>maxv)maxv=x;t=strtok(0," \t\r\n,");}E[ne++]=m;}
  int v=maxv+1; uint64_t total=1ULL<<(v-1); int found=0;
  /* stride through colourings in a scrambled order so the K witnesses are diverse */
  uint64_t step=0x9E3779B97F4A7C15ULL|1; step&=total-1; if(!(step&1))step|=1;
  uint64_t c=0;
  for(uint64_t k=0;k<total&&found<K;k++){
    c=(c+step)&(total-1);
    int ok=1; for(int i=0;i<ne;i++){uint64_t x=c&E[i]; if(x==0||x==E[i]){ok=0;break;}}
    if(ok){printf("%llu\n",(unsigned long long)c);found++;}
  }
  return 0;
}
