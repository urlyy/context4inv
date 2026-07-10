//SyGuG2018_fib_21
/*@ ensures \result > 0 && \result < 10; */
int unknown1();

void fmain(){
    int i;
    int j;
    int k;
    int n = unknown1();
    int v;

    //pre-condition
    k = 0;
    i = 0;

    //loop-body
    while(i < n){
        if(unknown()){
            i = i + 1;
            k = k + 4000;
            v = 0;
        }
        else{
            i = i + 1;
            k = k + 2000;
            v = 1;
        }
    }

    //post-condition
    //@ assert((i >= n)==>(k > n));
}