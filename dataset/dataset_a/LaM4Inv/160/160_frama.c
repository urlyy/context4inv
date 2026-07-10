//SyGuG2018_fib_16
void foo(){
    int x;
    int y;
    int i;
    int j;

    //pre-condition
    x = i;
    y = j;

    //loop-body
    while(x != 0){
        x = x - 1;
        y = y - 1;
    }

    //post-condition
    //@ assert((i == j)==>(y == 0));
}