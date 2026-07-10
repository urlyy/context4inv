int foo(int *a, int *b) {
  int SIZE=100000;
  int i = 0;
  int rv = 1;
  while ( i < SIZE ) {
    if ( a[i] != b[i] ) {
      rv = 0;
    }
    i = i+1;
  }
  //@ assert((rv!=0) ==> \forall int x; ((0 <= x && x < SIZE) ==> (a[x] == b[x])));
  return 0;
}
