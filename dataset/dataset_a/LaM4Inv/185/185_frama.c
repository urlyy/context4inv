//SyGuG2018_fib_44
/*@ ensures \result == 1 || \result == 2; */
int unknown1();

void foo(){
    int i;
    int j;
    int n = unknown1();
    int k;

    //pre-condition
    i = 0;
    j = 0;

    //loop-body
    while(i <= k){
        i = i + 1;
        j = j + n;
    }

    //post-condition
    //@ assert((i > k && i != j)==>(n != 1));
}