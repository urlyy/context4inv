int foo(int i,int n,int sum) {
  if ((i==0 && n>=0 && n<=100 && sum==0)){
    while (i<n) {
      sum = sum + i;
      i++;
    }
    //@ assert(sum>=0);
  }
  return 0;
}
