//svcomp_half
/*@ ensures \result >= 0 && \result <= 20000001; */
int unknown1();

void foo(){
    int n;
    int k = unknown1();
    int i;

    //pre-condition
    n = 0;
    i = 0;

    //loop-body
    while (i < 2 * k) {
        if(i % 2 == 0){
            n = n + 1;
        }
        i = i + 1;
    }

    //post-condition
    //@ assert(n == k);
}
