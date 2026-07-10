int main() {
  int N = 4;
  int i, j;
  int cnt = 0;
  int total = 0;

  for (i = 1; i <= N; i++) {
    for (j = 1; j <= i; j++) {
      cnt = cnt + 1;
      total = total + j;
    }
  }

  //@ assert(cnt == 10 && total == 20);
  return 0;
}
