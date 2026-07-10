//SyGuG2018_fib_15
/*@
    requires n > 0;
    requires k > n;
*/
void foo(int n, int k){
    int j;

    //pre-condition
    j = 0;

    //loop-body
    while(j < n){
        j = j + 1;
        k = k - 1;
    }

    //post-condition
    //@ assert((j >= n)==>(k >= 0));
}