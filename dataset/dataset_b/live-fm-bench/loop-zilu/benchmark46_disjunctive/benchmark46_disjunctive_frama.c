int foo(int x,int y,int z) {
  if ((y>0 || x>0 || z>0)){
    while (unknown()) {
      if (x>0) {
        x++;
      }
      if (y>0) {
        y++;
      } else {
        z++;
      }
    }
    //@ assert(x>0 || y>0 || z>0);
  }
 
  return 0;
}
