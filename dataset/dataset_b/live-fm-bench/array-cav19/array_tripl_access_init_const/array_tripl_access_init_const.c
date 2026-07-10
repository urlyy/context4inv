int main()
{
  int i;
  int N=100000;
  int a[3*N+1];
  for(i=0; i<= N; i++) {
    a[3*i] =0;
    a[3*i+1]=0;
    a[3*i+2]=0;
  }
  //@ assert(∀k((0<=k && k<=3*N)=>(a[k] >= 0)))
  return 0;
}
