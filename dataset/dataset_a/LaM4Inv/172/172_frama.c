//SyGuG2018_fib_23_x
/*@ ensures \result > 0; */
int unknown1();

void fmain(){
    int i;
    int n = unknown1();
    int sum;

    //pre-condition
    sum = 0;
    i = 0;

    //loop-body
    while(i < n){
        sum = sum + i;
        i = i + 1;
    }

    //post-condition
    //@ assert((i >= n)==>(sum));
}