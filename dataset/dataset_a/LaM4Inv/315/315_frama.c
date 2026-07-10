//svcomp_vnew2
/*@ ensures \result <= 20000001; */
int unknown1();

void foo(){
    unsigned int n = unknown1();
    unsigned int j;
    unsigned int i;
    unsigned int k;

    //pre-condition
    i = 0;
    k = 0;
    j = 0;

    //loop-body
    while (i < n) {
        i = i + 3;
        j = j + 3;
        k = k + 3;
    }

    //post-condition
    //@ assert(k == j);
}