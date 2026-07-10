//svcomp_css2003
/*@ ensures \result >= 0 && \result <= 1; */
int unknown1();

void foo(){
    int i;
    int j;
    int k = unknown1();

    //pre-condition
    i = 1;
    j = 1;

    //loop-body
    while(unknown()){
        i = i + 1;
        j = j + k;
        k = k - 1;
    }

    //post-condition
    //@ assert(i + k <= 2);
}
