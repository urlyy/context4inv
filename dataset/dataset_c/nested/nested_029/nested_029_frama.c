/*@
    requires N >= 1 && N <= 10;
    requires M >= 1 && M <= 10;
*/
int foo(int N, int M) {
  int i, j;
  int x = 0;
  int y = 0;


  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j++) {
      x = x + 1;
      y = y + i;
    }
  }

  //@ assert(x == N * M && y >= 0);
  return 0;
}
