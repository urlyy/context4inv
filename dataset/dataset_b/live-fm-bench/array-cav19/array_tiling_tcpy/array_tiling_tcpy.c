int main()
{
  int S;
  //@ assume(S>1 && S < 1073741823)
  int i;
  int a[2*S];
  int acopy[2*S];
  for(i=0;i < S;i++) {
    acopy[2*S - (i+1)] = a[2*S - (i+1)];
    acopy[i] = a[i];
  }
  //@ assert(∀k((0<=k && k<2*S)=>(acopy[k] == a[k])))
  return 0;
}
