//SyGuG2018_fib_18
/*@ ensures \result > 0; */
int unknown1();

void foo(){
    int b;
    int j;
    int n = unknown1();
    int flag;

    //pre-condition
    j = 0;
    b = 0;

    //loop-body
    while(b < n){
        if(flag == 1){
            j = j + 1;
            b = b + 1;
        }
        else if (flag != 1){
            b = b + 1;
        }
    }

    //post-condition
    //@ assert((flag == 1)==>(j == n));
}