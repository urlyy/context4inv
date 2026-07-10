int foo()
{
  int N = 100000;
  int a[N];
  int b[N];
  int i;
  int sum=0;
  /*@
  loop invariant i <= N;
  loop invariant \forall integer j; 0 <= j < i ==> a[j] == j;
  loop invariant 0 <= i;
  loop assigns i;
  loop assigns a[0..N-1];
  */
  for (i=0;i<N;i++) {
    a[i] = i;
  }
  /*@
  loop invariant i <= N;
  loop invariant \forall integer j; 0 <= j < i ==> b[N-j-1] == j;
  loop invariant 0 <= i;
  loop assigns i;
  loop assigns b[0..N-1];
  */
  for (i=0;i<N;i++) {
    b[N-i-1]=i;
  }
  /* @ >>> INFILL <<< */
  for (i=0;i<N;i++) {
    sum=sum+(a[i]-b[N-i-1]);
  }
  //@ assert(sum == 0);
  return 0;
}
