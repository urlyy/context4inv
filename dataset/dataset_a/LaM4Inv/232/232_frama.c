//svcomp_phases_2-1
/*@ ensures \result > 2; */
int unknown1();

void foo() {
    int x;
    int y = unknown1();

    //pre-condition
    x = 2;

    //loop-body
    while (x < y) {
        if (x < y / x) {
            x *= x;
        } 
        else {
            x++;
        }
    }

    //post-condition
    //@ assert(x == y);

}