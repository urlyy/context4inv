/*@ ensures \result  > -100000 &&  < 100000; */
int unknown1();

/* 3. FUNC CONTRACT */
int foo()
{
  int i;
  int N = 100000;
  int a[N];
  int b[N];
  int c[N];
  /* 1. LOOP INVARIANT */
  for(i=0;i<N;i++) {
    int unknown_1 = unknown();
    a[i]=unknown_1;
    b[i]=0-unknown_1;
  }
  /* 2. LOOP INVARIANT */
  for(i=0;i<N;i++){
    c[i]=a[i]+b[i];
  }
  //@ assert \forall int k; (1<=k && k<N) ==> (c[k] == 0);
  return 0;
}