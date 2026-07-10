//SyGuG2018_fib_20
/*@ 
  requires (x + y) == k;
*/
void foo(int x, int y, int k){
    int j;
    int i;
    int n;
    int m;

    //pre-condition
    m = 0;
    j = 0;

    //loop-body
    while(j < n){
        if(j == i){
            x = x + 1;
            y = y - 1;
            j = j + 1;
            if(unknown()){
                m = j;
            }
        }
        else if(j != i){
            x = x - 1;
            y = y + 1;
            j = j + 1;
            if(unknown()){
                m = j;
            }
        }

    }

    //post-condition
    //@ assert((j >= n && n > 0)==>(0 <= m));
}