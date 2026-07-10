int main() {
  int A = 2;
  int B = 3;
  int C = 4;
  int i, j, k;
  int cnt = 0;

  for (i = 0; i < A; i++) {
    for (j = 0; j < B; j++) {
      for (k = 0; k < C; k++) {
        cnt = cnt + 2;
      }
    }
  }

  //@ assert(cnt == 48);
  return 0;
}
