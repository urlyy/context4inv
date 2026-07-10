/*@
    requires N >= 0 && N <= 20;
*/
int foo(int N) {
  int i, j;
  int cnt = 0;


  for (i = 0; i < N; i++) {
    for (j = 0; j <= i; j++) {
      cnt = cnt + 1;
    }
  }

  //@ assert(cnt >= N && cnt <= N * N);
  return 0;
}
