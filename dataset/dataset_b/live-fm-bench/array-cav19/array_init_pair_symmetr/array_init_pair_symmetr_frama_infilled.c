/*@ ensures \result  > -100000 &&  < 100000; */
int unknown1();

int foo()
{
  int i;
  int N = 100000;
  int a[N];
  int b[N];
  int c[N];
  /*@
  loop invariant i <= N;
  loop invariant 0 <= i;
  loop assigns i;
  loop assigns b[0..N-1];
  loop assigns a[0..N-1];
  */
  for(i=0;i<N;i++) {
    int unknown_1 = unknown();
    a[i]=unknown_1;
    b[i]=0-unknown_1;
  }
  /*@
  >>> INFILL <<<
  loop invariant i <= N;
  loop invariant 0 <= i;
  loop assigns i;
  loop assigns c[0..N-1];
  */
  for(i=0;i<N;i++){
    c[i]=a[i]+b[i];
  }
  // @ assert \forall int k; (1<=k && k<N) ==> (c[k] == 0);
  return 0;
}