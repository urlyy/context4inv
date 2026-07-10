//svcomp_benchmark09_conjunctive
/*@ ensures \result >= 0; */
int unknown1();

void foo(){
    int x;
    int y = unknown1();

    //pre-condition
    x = y;

    //loop-body
    while (x != 0) {
        x = x - 1;
        y = y - 1;
    }

    //post-condition
    //@ assert(y == 0);
}