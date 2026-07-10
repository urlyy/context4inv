int main() {
  int P = 2;
  int Q = 3;
  int R = 2;
  int i, j, k;
  int s = 0;
  int t = 0;

  for (i = 0; i < P; i++) {
    for (j = 0; j < Q; j++) {
      for (k = 0; k < R; k++) {
        s = s + i + j + k;
        t = t + 1;
      }
    }
  }

  //@ assert(s == 24 && t == 12);
  return 0;
}
