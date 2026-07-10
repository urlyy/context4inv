//svcomp_benchmark27_linear
/*@
    requires (k > i - j);
    requires (i < j);
*/
void foo(int i, int j, int k){
    //pre-condition

    //loop-body
    while (i < j) {
        k = k + 1;
        i = i + 1;
    }

    //post-condition
    //@ assert(k > 0);
}