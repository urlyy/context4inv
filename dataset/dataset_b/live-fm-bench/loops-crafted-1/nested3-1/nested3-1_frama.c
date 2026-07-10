int foo()
{
  unsigned int x = 0;
  unsigned int y = 0;
  unsigned int z = 0;
  unsigned int w = 0;
  while (x < 1025) {
    y = 0;
    while (y < 1025) {
   	  z =0;
      while (z <1025) {
        z++;
      }
    	//@ assert(z % 4 == 1);
	    y++;
    }
    //@ assert(y % 2 == 1);
    x++;
  }
  //@ assert(x % 2==1);
  return 0;
}
