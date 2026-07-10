int foo(int i,int j,int x,int y,int k) {
  j=0;
  if ((x+y==k)){
    while (unknown()) {
      if(j==i) {x++;y--;} else {y++;x--;} j++;
    }
    //@ assert(x+y==k);
  }
  return 0;
}