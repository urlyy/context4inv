//svcomp_eq1
/*@ ensures \result > 0; */
int unknown1();
/*@ ensures \result > 0; */
int unknown2();
/*@ ensures \result > 0; */
int unknown3();
/*@ ensures \result > 0; */
int unknown4();

void foo() {
    int w = unknown4();
    int x = unknown1();
    int y = unknown2();
    int z = unknown3();

    //pre-condition
    x = w;
    z = y;
    while(unknown()) {
        if (unknown()) {
            w = w + 1; 
            x = x + 1;
        } 
        else {
            y = y - 1; 
            z = z - 1;
        }
    }

    //post-condition
    //@ assert(y == z);
}
