int main() {
  int N = 4;
  int M = 3;
  int i, j;
  int cnt = 0;
  int s = 0;

  for (i = 0; i < N; i++) {
    for (j = 0; j < M; j += 2) {
      cnt = cnt + 1;
      s = s + i + j;
    }
  }

  //@ assert(cnt == 8 && s == 28);
  return 0;
}
