/* 3. FUNC CONTRACT */
int foo()
{
  int i;
  int N=100000;
  int a[N];
  int b[N];
  int c[N];
  /* 1. LOOP INVARIANT */
  for(i=0;i<N;i++) {
    a[i]=1;
    b[i]=2;
  }
  /* 2. LOOP INVARIANT */
  for(i=0;i<N;i++){
    c[i]=a[i]+b[i];
  }
  //@ assert \forall int k; (1<=k && k<N) ==> (c[k]>=3);
  return 0;
}