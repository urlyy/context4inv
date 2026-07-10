/*@
    requires N >= 1 && N <= 8;
    requires M >= 1 && M <= 8;
*/
int foo(int N, int M) {
  int i, j;
  int s = 0;
  int t = 0;


  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j++) {
      s = s + j;
      t = t + 1;
    }
  }

  //@ assert(t == N * M && s >= 0);
  return 0;
}
