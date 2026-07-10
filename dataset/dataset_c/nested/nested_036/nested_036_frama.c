/*@
    requires N >= 1 && N <= 8;
    requires M >= 1 && M <= 8;
*/
int foo(int N, int M) {
  int i, j;
  int even = 0;
  int total = 0;


  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j++) {
      total = total + 1;
      if (j % 2 == 0) {
        even = even + 1;
      }
    }
  }

  //@ assert(even >= 0 && even <= total);
  return 0;
}
