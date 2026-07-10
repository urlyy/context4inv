//svcomp_simple_4-1
void fmain() {
    unsigned int x;

    //pre-condition
    x = 268435441;

    //loop-body
    while (x > 1) {
        x -= 2;
    }

    //post-condition
    //@ assert(x % 2 == 1);

}