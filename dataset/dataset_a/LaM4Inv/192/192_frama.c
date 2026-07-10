//SyGuG2018_inria-00615623
/*@
    requires i < n;
*/
void ffoo(int i, int n){
    int b;

    //pre-condition
    i = 0;

    //loop-body
    while(i < n && b != 0){
        i = i + 1;
    }

    //post-condition
    //@ assert((i >= n)==>(i == n && b != 0));
}