int foo(int x,int y) {
  if ((y>0 || x>0)){
    while (unknown()) {
      if (x>0) {
        x++;
      } else {
        y++;
      }
    }
    //@ assert(x>0 || y>0);
  }
  return 0;
}
