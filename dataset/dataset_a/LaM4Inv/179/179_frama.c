//SyGuG2018_fib_37
/*@ ensures \result > 0; */
int unknown1();

void foo(){
    int x;
    int n = unknown1();
    int m;

    //pre-condition
    x = 0;
    m = 0;

    //loop-body
    while(x < n){
        if(unknown()){
            m = x;
        }
        x = x + 1;
    }

    //post-condition
    //@ assert((x >= n && n > 0)==>(0 <= m));
}