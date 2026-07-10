int main(int *A,int *B) {
  int SZ=2048;
  int i;
  int tmp;
  for (i = 0; i < SZ; i++) {
    tmp = A[i];
    B[i] = tmp;
  }
  //@ assert(A[SZ/2] == B[SZ/2]);
}
