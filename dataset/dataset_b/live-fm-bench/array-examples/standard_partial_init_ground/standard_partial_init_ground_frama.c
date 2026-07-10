int foo( int *A, int *B, int *C ) {
  int N = 100000;
  int i;
  int j = 0;
	for (i = 0; i < N ; i++) {
    if ( A[i] == B[i] ) {
      C[j] = i;
      j = j + 1;
    }
  }
  //@ assert( \forall int x;((0 <= x && x < j) ==> (C[x] <= x + i - j && C[x] >= x)) );
  return 0;
}
