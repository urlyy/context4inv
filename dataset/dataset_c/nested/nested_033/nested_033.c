int main() {
  int A;
  int B;
  int C;
  int i, j, k;
  int cnt = 0;

  //@ assume(A >= 1 && A <= 5);
  //@ assume(B >= 1 && B <= 5);
  //@ assume(C >= 1 && C <= 5);

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
