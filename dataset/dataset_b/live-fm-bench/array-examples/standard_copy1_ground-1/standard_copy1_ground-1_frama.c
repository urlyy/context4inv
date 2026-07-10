int foo(int *a1, int *a2) {
  int N=100000;
  int a;
  int i;
  for ( i = 0 ; i < N ; i++ ) {
    a2[i] = a1[i];
  }
  //@ assert(\forall int x; ((0 <= x && x < N) ==> (a1[x] == a2[x])));
  return 0;
}
