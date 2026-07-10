/*@
    requires N >= 1 && N <= 8;
    requires M >= 1 && M <= 8;
*/
int foo(int N, int M) {
  int i, j;
  int sum = 0;


  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j++) {
      sum = sum + 1;
    }
  }

  //@ assert(sum == N * M);
  return 0;
}
