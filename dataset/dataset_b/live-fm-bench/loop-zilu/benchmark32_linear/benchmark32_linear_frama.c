int foo(int x) {
  if ((x==1 || x==2)){
    while (unknown()) {
      if(x==1) x=2;
      else if (x==2) x=1;
    }
    //@ assert(x<=8);
  }
  return 0;
}
