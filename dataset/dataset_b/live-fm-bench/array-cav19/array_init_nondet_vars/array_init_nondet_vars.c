int main()
{
  int i,j,n;
  //@ assume(n < 100000)
  //@ assume(j>0 && j < 10000)
  int a[n];
  int unknown1, unknown2;
  for(i=1;i<n;i++) {
    int unknown1;
    //@ assume(unknown1>0 && unknown1 < 10000)
    a[i]=i+j+unknown1;
    unknown1 = unknown2;
    //@ assume(unknown1>0 && unknown1 < 10000)
  }
  //@ assert(∀k((1<=k && k<n)=>(a[k]>=(i+2))))
  return 0;
}  
