int foo (int *a, int *b ) {
  int N=100000;
  int i = 0;
  while ( i < N ) {
    a[i] = 42;
    i = i + 1;
  }
  for ( i = 0 ; i < N ; i++ ) {
    b[i] = a[i];
  }
  //@ assert(\forall int x;((0 <= x && x < N) ==> (b[x] == 42)));
  return 0;
}
