//svcomp_benchmark28_linear


/*@
    requires (i >= 1);
    requires(j >= 1);
    requires (i * i < j * j);
*/
void foo(int i,int j){
    //pre-condition

    //loop-body
    while (i < j) {
        j = j - i;
        if (j < i) {
            j = j + i;
            i = j - i;
            j = j - i;
        }
    }

    //post-condition
    //@ assert(j == i);
}