/*@
    requires N >= 1 && N <= 10;
    requires M >= 1 && M <= 10;
*/
int foo(int N, int M) {
  int i, j;
  int p = 0;
  int q = 0;


  for (i = 1; i <= N; i++) {
    for (j = 1; j <= M; j++) {
      p = p + i;
      q = q + j;
    }
  }

  //@ assert(p >= N && q >= M);
  return 0;
}
