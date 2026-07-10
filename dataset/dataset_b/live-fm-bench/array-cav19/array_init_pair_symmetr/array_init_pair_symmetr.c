int main()
{
  int i;
  int N = 100000;
  int a[N];
  int b[N];
  int c[N];
  int unknown1, unknown2;
  for(i=0;i<N;i++) {
    //@ assume(unknown1 > -100000 && unknown1 < 100000);
    a[i]=unknown1;
    b[i]=0-unknown1;
    unknown1 = unknown2;
    //@ assume(unknown1 > -100000 && unknown1 < 100000);
  }
  for(i=0;i<N;i++){
    c[i]=a[i]+b[i];
  }
  //@ assert(∀k((1<=k && k<N)=>(c[k] == 0)))
  return 0;
}
