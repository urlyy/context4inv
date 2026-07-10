int main() {
  int N = 4;
  int M = 3;
  int i, j;
  int s = 0;

  for (i = N - 1; i >= 0; i--) {
    for (j = 0; j < M; j++) {
      s = s + i;
    }
  }

  //@ assert(s == 18);
  return 0;
}
