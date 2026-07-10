//svcomp_benchmark23_conjunctive
void foo(){
    int i;
    int j;

    //pre-condition
    i = 0;
    j = 0;

    //loop-body
    while (i < 100) {
        j += 2;
        i++;
    }

    //post-condition
    //@ assert(j == 200);
}