int main() {
  int N = 5;
  int M = 3;
  int i, j;
  int cnt = 0;

  for (i = 0; i < N; i++) {
    for (j = i; j < M + i; j++) {
      cnt = cnt + 1;
    }
  }

  //@ assert(cnt == 15);
  return 0;
}
