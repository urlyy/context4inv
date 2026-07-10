void fmain()
{
    int x = 0;
    int y, z;
    //@ LOOP_0 invariant: (z >= y || x == 0) && (x <= 5 && x >= 0) && (x <= 5) && (0 <= x)
    LOOP_0:while(x < 5) {
       x += 1;
       if( z <= y) {
          y = z;
       }
    }

    //@ assert(z >= y);
}