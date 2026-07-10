int main()
{
  int i;
  int N=100000;
  int a[N];
  int b[N];
  int c[N];
  for(i=0;i<N;i++) {
    a[i]=1;
    b[i]=2;
  }
  for(i=0;i<N;i++){
    c[i]=a[i]+b[i];
  }
  //@ assert(∀k((1<=k && k<N)=>(c[k]>=3)))
  return 0;
}
