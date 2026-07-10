/*@
    requires N >= 0 && N <= 12;
    requires M >= 0 && M <= 12;
*/
int foo(int N, int M) {
  int i, j;
  int r = 0;


  for (i = 0; i < N; i++) {
    for (j = i; j < i + M; j++) {
      r = r + 1;
    }
  }

  //@ assert(r == N * M);
  return 0;
}
