//SyGuG2018_fib_32
/*@ ensures \result > 0 && \result < 20000001; */
int unknown1();
/*@ ensures \result == j; */
int unknown2();

void foo(){
    int i = unknown2();
    int j;
    int n;
    int k = unknown1();
    int b;

    //pre-condition
    n = 0;
    b = 1;

    //loop-body
    while(n < (2 * k)){
        n = n + 1;
        if(b == 1){
            b = 0;
            i = i + 1;
        }
        else{
            b = 1;
            j = j + 1;
        }
    }

    //post-condition
    //@ assert((n >= (2 * k))==>(i == j));
}