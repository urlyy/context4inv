int foo(int i,int k,int n) {
  if (i==0 && k==0){
    while (i<n) {
      i++;
      k++;
    }
    //@ assert(k>=n);
  }
  return 0;
}
