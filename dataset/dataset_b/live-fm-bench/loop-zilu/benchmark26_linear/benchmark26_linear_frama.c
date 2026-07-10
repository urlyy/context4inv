int foo(int x,int y) {
  if ((x<y)){
    while (x<y) {
      x=x+1;
    }
    //@ assert(x==y);
  }
  return 0;
}
