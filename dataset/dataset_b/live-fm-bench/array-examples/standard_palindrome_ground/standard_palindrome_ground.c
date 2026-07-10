int main( int *A) {
  int N = 100000;
  int i;
  for (i = 0; i < N/2 ; i++ ) {
    A[i] = A[N-i-1];
  }
  //@ assert( ∀x((0 <= x && x < N/2) => (A[x] == A[N - x - 1])) );
  return 0;
}
