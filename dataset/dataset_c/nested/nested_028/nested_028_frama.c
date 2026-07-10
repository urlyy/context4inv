/*@
    requires N >= 0 && N <= 8;
    requires M >= 0 && M <= 8;
*/
int foo(int N, int M) {
  int i, j;
  int acc = 0;


  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j++) {
      acc = acc + i;
    }
  }

  //@ assert(acc >= 0 && acc <= N * N * M);
  return 0;
}
