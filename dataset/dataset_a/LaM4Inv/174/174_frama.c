//SyGuG2018_fib_28
/*@ ensures \result >= 0 && \result == y; */
int unknown1();
/*@ ensures \result >= 0; */
int unknown2();

void fmain(){
    int x = unknown1();
    int y = unknown2();
    int n;

    //pre-condition
    n = 0;

    //loop-body
    while(x != n){
        x = x - 1;
        y = y - 1;
    }

    //post-condition
    //@ assert((x == n)==>(y == n));
}