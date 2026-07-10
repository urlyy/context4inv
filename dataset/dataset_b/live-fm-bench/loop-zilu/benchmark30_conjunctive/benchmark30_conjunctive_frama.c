int foo(int x,int y) {
  if ((y == x)){
    while (unknown()) {
      x++;
      y++;
    }
    //@ assert(x == y);
  }
  return 0;
}
