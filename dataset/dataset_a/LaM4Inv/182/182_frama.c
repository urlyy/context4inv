//SyGuG2018_fib_41
/*@ ensures \result >= 0 && \result <= 20000001; */
int unknown1();
/*@ ensures \result >= 0 && \result <= 20000001; */
int unknown2();

void foo(){
    int k = unknown2();
    int n = unknown1();
    int i;
    int j;

    //pre-condition
    j = 0;
    i = 0;

    //loop-body
    while(i <= n){
        i = i + 1;
        j = j + 1;
    }

    //post-condition
    //@ assert((i > n)==>((k + i + j) > (2 * n)));
}