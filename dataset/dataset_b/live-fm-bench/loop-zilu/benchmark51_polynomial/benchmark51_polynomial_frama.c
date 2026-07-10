int foo(int x) {
  if (((x>=0) && (x<=50))){
    while (unknown()) {
      if (x>50) x++;
      if (x == 0) { 
        x ++;
      } else x--;
    }
    //@ assert((x>=0) && (x<=50));
  }
  return 0;
}
