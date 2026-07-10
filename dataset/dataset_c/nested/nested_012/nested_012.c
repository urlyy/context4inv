int main() {
  int N = 4;
  int M = 3;
  int i, j;
  int sum = 0;
  int cnt = 0;

  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j++) {
      sum = sum + i - j;
      cnt = cnt + 1;
    }
  }

  //@ assert(cnt == 12 && sum >= -12 && sum <= 12);
  return 0;
}
