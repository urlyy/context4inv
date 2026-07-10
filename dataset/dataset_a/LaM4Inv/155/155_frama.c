//SyGuG2018_fib_13
void foo(){
    int j;
    int k;
    int t;

    //pre-condition
    j = 2;
    k = 0;

    //loop-body
    while(unknown()){
        if (t == 0){
            j = j + 4;
        }
        else {
            j = j + 2;
            k = k + 1;
        }
    }

    //post-condition
    //@ assert((k != 0)==>(t != 0 && j == k * 2 + 2));
}
