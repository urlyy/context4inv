int foo( int *a) {
  int SIZE = 100000;
  int i;
  i = 1;
  a[0] = 7;
  while( i < SIZE ) {
    a[i] = a[i-1] + 1;
    i = i + 1;
  }
  //@ assert( \forall int x;((1 <= x && x < SIZE) ==> (a[x] >= a[x-1])) );
  return 0;
}
