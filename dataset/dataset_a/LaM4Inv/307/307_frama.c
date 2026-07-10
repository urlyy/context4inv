//svcomp_sumt3
/*@ ensures \result <= 20000001; */
int unknown1();

void foo(){
    unsigned int n = unknown1();
    unsigned int j;
    unsigned int i;
    unsigned int k;
    unsigned int l;

    //pre-condition
    i = 0;
    k = 0;
    j = 0;
    l = 0;

    //loop-body
    while (l < n) {
        if ((l % 3) == 0) {
            i = i + 1;
        }
        else if((l % 2) == 0){
            j = j + 1;
        }
        else{
            k = k + 1;
        }
        l = l + 1;
    }

    //post-condition
    //@ assert((i + j + k) == l);
}