int foo(int xa,int ya) {
  if ((xa + ya > 0)){
    while (xa > 0) {
      xa--;
      ya++;
    }
    //@ assert(ya >= 0);
  }
  return 0;
}
