//svcomp_benchmark43_conjunctive
/*@ ensures \result < 100; */
int unknown1();
/*@ ensures \result < 100; */
int unknown2();

void foo(){
    int x = unknown1();
    int y = unknown2();

    //pre-condition

    //loop-body
    while (x < 100 && y < 100) {
        x = x + 1;
        y = y + 1;
    }

    //post-condition
    //@ assert(x == 100 || y == 100);
}