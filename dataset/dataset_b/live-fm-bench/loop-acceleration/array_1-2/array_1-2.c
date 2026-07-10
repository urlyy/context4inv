int main(int *A) {
  int i;
  for (i = 0; i < 1024; i++) {
    A[i] = i;
  }
  //@ assert(A[1023] == 1023);
}
