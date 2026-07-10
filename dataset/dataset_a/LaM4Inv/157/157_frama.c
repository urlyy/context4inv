//SyGuG2018_fib_14
/*@ ensures \result > 0; */
int unknown1();

void foo(){
    int a;
    int j;
    int m = unknown1();

    //pre-condition
    a = 0;
    j = 1;

    //loop-body
    while(j <= m){
        if(unknown()){
            a = a + 1;
        }else{
            a = a - 1;
        }
        j = j + 1;
    }

    //post-condition
    //@ assert((j > m)==>(a >= 0 - m));
}