//SyGuG2018_fib_35
/*@ ensures \result > 0; */
int unknown1();

void foo(){
    int x;
    int n = unknown1();

    //pre-condition
    x = 0;

    //loop-body
    while(x < n){
        x = x + 1;
    }

    //post-condition
    //@ assert((x >= n)==>(x == n));
}