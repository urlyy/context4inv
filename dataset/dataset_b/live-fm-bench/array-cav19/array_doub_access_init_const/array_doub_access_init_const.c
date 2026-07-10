int main()
{
  int i;
  int N=100000;
  int a[2*N+2];
  for(i=0;i<=N;i++) {
    a[2*i]=0;
    a[2*i+1]=0;
  }
  //@ assert(∀j((0<=j && j<=2*N)=>(a[j]>=0) ))
  return 0;
}
