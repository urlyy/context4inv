//svcomp_benchmark04_conjunctive
/*@
    requires n >= 1;
    requires k >= n;
*/
void ffoo(int n, int k){
    int j;

    //pre-condition
    j = 0; 

    //loop-body
    while (j <= n - 1) {
        j = j + 1;
        k = k - 1;
    }

    //post-condition
    //@ assert(k >= 0);
}
