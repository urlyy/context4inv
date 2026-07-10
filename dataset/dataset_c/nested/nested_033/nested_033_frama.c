/*@
    requires A >= 1 && A <= 5;
    requires B >= 1 && B <= 5;
    requires C >= 1 && C <= 5;
*/
int foo(int A, int B, int C) {
  int i, j, k;
  int cnt = 0;


  for (i = 0; i < A; i++) {
    for (j = 0; j < B; j++) {
      for (k = 0; k < C; k++) {
        cnt = cnt + 1;
      }
    }
  }

  //@ assert(cnt == A * B * C);
  return 0;
}
