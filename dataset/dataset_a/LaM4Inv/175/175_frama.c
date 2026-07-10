//SyGuG2018_fib_30_x
/*@ ensures \result > 0; */
int unknown1();

void foo(){
    int i;
    int c;
    int n = unknown1();

    //pre-condition
    i = 0;
    c = 0;

    //loop-body
    while(i < n){
        c = c + i;
        i = i + 1;
    }

    //post-condition
    //@ assert((i >= n)==>(c));
}