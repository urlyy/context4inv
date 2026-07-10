//svcomp_benchmark24_conjunctive
/*@ ensures \result >= 0 && \result <= 20000001; */
int unknown1();

void foo(){
    int i;
    int k;
    int n = unknown1();

    //pre-condition
    i = 0;
    k = n;

    //loop-body
    while (i < n) {
        k--;
        i += 2;
    }

    //post-condition
    //@ assert(2 * k >= n - 1);
}