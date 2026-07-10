//SyGuG2018_fib_19
/*@ 
  requires n >= 0;
  requires m >= 0;
  requires m < n;
*/
void ffoo(int n, int m){
    int x;
    int y;

    //pre-condition
    x = 0;
    y = m;

    //loop-body
    while(x < n){
        if(x + 1 <= m){
            x = x + 1;
        }
        else if (x + 1 > m){
            x = x + 1;
            y = y + 1;
        }
    }

    //post-condition
    //@ assert((x >= n)==>(y == n));
}