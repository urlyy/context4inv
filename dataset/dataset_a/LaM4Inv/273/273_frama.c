//svcomp_benchmark14_linear
/*@ ensures \result >= 0 && \result <= 200; */
int unknown1();

void foo(){
    int i = unknown1();

    //pre-condition

    //loop-body
    while (i > 0) {
        i = i - 1;
    }

    //post-condition
    //@ assert(i >= 0);
}