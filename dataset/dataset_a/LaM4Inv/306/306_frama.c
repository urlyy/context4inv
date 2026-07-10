//svcomp_sumt2
/*@ ensures \result <= 20000001; */
int unknown1();

void foo(){
    unsigned int n = unknown1();
    unsigned int j;
    unsigned int i;
    unsigned int l;

    //pre-condition
    i = 0;
    j = 0;
    l = 0;

    //loop-body
    while (l < n) {
        if ((l % 2) == 0) {
            i = i + 1;
        }
        else{
            j = j + 1;
        }
        l = l + 1;
    }

    //post-condition
    //@ assert((i + j) == l);
}