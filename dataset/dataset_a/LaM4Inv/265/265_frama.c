//svcomp_benchmark02_linear
/*@ ensures \result > 0; */
int unknown1();

void foo(){
    int n;
    int i;
    int l = unknown1();

    //pre-condition
    i = l;

    //loop-body
    while (i < n) {
        i = i + 1;
    }

    //post-condition
    //@ assert(l >= 1);
}
