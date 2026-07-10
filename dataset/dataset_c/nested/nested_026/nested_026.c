int main() {
  int N = 4;
  int i, j;
  int above = 0;
  int diag = 0;

  for (i = 0; i < N; i++) {
    for (j = 0; j < N; j++) {
      if (j > i) {
        above = above + 1;
      }
      if (j == i) {
        diag = diag + 1;
      }
    }
  }

  //@ assert(diag == 4 && above == 6);
  return 0;
}
