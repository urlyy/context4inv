int foo(int x,int y) {
  if ((x == y && y == 0)){
    while (unknown()) {
      x++;y++;
    }
    //@ assert(x == y && x >= 0);
  }
  
  return 0;
}
