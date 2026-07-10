int foo(int x,int y) {
  if ((x*y>=0)){
    while (unknown()) {
      if(x==0) {
        if (y>0) x++;
        else x--;
      } 
      if(x>0) y++;
      else x--;
    }
    //@ assert(x*y>=0);
  }
  return 0;
}
