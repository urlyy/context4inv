//SyGuG2018_jmbl_hola_20
/*@
    requires k == x + y;
*/
void foo(int x, int y, int k){
    int i;
    int j;
    int m;
    int n;

    //pre-condition
    m = 0;
    j = 0;

    //loop-body
    while(j < n){
        if(unknown()){
            m = j;
        }
        if(j == i){
            x = x + 1;
            y = y - 1;
        }
        else{
            x = x - 1;
            y = y + 1;
        }
        j = j + 1;
    }

    //post-condition
    //@ assert((m >= n)==>(n <= 0));
}