//svcomp_benchmark39_conjunctive
/*@ ensures \result >= 0 && \result <= 20000001; */
int unknown1();

void fmain(){
    int x;
    int y = unknown1();

    //pre-condition
    x = 4 * y;


    //loop-body
    while (x > 0) {
        x -= 4;
        y--;
    }

    //post-condition
    //@ assert(y >= 0);
}