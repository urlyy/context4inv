//SyGuG2018_fig2
void foo(){
    int x, y, z, w;

    //pre-condition
    x = 0; y = 0; z = 0; w = 0;

    //loop-body
    /*@
        loop invariant x >= 0;
        loop invariant w == z;
        loop invariant (x < 4) ==> (y == 2 * x && z == 0);
        loop invariant (x >= 4) ==> (y == 3 * x - 4 && z == 10 * (x - 4));
        loop assigns x, y, z, w;
    */
    while(unknown()){
        if(x >= 4){
            x = x + 1;
            y = y + 3;
            z = z + 10;
            w = w + 10;
        }
        else if(x >= z && w > y){
            x = 0 - x;
            y = 0 - y;
        }
        else{
            x = x + 1;
            y = y + 2;
        }
    }

    //post-condition
    //@ assert 3 * x >= y;
}