int foo(int x,int y) {
  if ((x==1 && y==0)){
    while (unknown()) {
      x=x+y;
      y++;
    }
    //@ assert(x >= y);
  }
  
  return 0;
}
