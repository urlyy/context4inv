//svcomp_benchmark49_linear
/*@
    requires r > i+j;
*/
void ffoo(int i,int j,int r){
    //pre-condition

    //loop-body
    while (i > 0) {
        i = i - 1;
        j = j + 1;
    }

    //post-condition
    //@ assert(r > i + j);
}