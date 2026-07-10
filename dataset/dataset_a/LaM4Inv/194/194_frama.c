//SyGuG2018_jm2006_invariant_true-unreach-call_true-termination.sl
/*@ ensures \result >= 0; */
int unknown1();

void foo(){
    int i;
    int x;
    int y;
    int z;

    //pre-condition
    x = i;
    y = i;
    z = 0;

    i = unknown1();

    //loop-body
    while(x != 0){
        x = x - 1;
        y = y - 2;
        z = z + 1;
    }

    //post-condition
    //@ assert(y == 0 - z);
    
}