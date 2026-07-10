/* 4. FUNC CONTRACT */
int foo()
{
  int N = 100000;
  int a[N];
  int b[N];
  int i;
  int sum=0;
  /* 1. LOOP INVARIANT */
  for (i=0;i<N;i++) {
    a[i] = i;
  }
  /* 2. LOOP INVARIANT */
  for (i=0;i<N;i++) {
    b[N-i-1]=i;
  }
  /* 3. LOOP INVARIANT */
  for (i=0;i<N;i++) {
    sum=sum+(a[i]-b[N-i-1]);
  }
  //@ assert(sum == 0);
  return 0;
}
