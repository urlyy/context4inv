int main() {
  int N = 5;
  int M = 4;
  int i, j;
  int s = 0;

  for (i = 0; i < N; i += 2) {
    for (j = 0; j < M; j++) {
      s = s + 1;
    }
  }

  //@ assert(s == 12);
  return 0;
}
