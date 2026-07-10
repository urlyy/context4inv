int foo(int i) {
  if (i>=0 && i<=200){
    while (i>0) {
      i--;
    }
    //@ assert(i>=0);
  }
  return 0;
}
