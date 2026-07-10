//svcomp_gauss_sum
/*@ ensures \result >= 1 && \result <= 1000; */
int unknown1();

void foo(){
    int n = unknown1();
    int sum;
    int i;

    //pre-condition
    sum = 0;
    i = 0;

    //loop-body
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }

    //post-condition
    //@ assert(2 * sum == n * (n - 1));
}
