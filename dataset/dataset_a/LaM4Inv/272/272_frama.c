//svcomp_benchmark13_conjunctive
void foo(){
    int i;
    int j;
    int k;

    //pre-condition
    i = 0;
    j = 0;

    //loop-body
    while (i <= k) {
        i++;
        j = j + 1;
    }

    //post-condition
    //@ assert(i == j);
}