//svcomp_benchmark08_conjunctive
/*@ ensures \result >= 0; */
int unknown1();

void fmain(){
    int i;
    int sum;
    int n = unknown1();

    //pre-condition
    sum = 0; 
    i = 0; 

    //loop-body
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }

    //post-condition
    //@ assert(sum >= 0);
}