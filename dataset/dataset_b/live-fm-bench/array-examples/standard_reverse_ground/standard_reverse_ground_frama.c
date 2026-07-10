int foo( int *a,int *b) {
  int N = 100000;
  int i;
  for( i = 0 ; i < N ; i++ ) {
    b[i] = a[N-i-1];
  }
  //@ assert( \forall int x;((0 <= x && x < N) ==> (a[x] == b[N - x - 1])) );
  return 0;
}
