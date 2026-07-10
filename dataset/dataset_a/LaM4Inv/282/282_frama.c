//svcomp_benchmark34_conjunctive
/*@ ensures \result > 0; */
int unknown1();

void foo(){
    int i;
    int k;
    int n = unknown1();

    //pre-condition
    i = 0;
    k = n;

    //loop-body
    while (i < n && n > 0) {
        k--;
        i++;
    }

    //post-condition
    //@ assert(k == 0);
}