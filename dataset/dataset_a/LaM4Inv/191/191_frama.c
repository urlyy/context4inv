//SyGuG2018_hhk2008_true-unreach-call_true-termination
/*@ ensures \result <= 1000000; */
int unknown1();
/*@ ensures \result >= 0 && \result <= 1000000; */
int unknown2();

void foo(){
    int a = unknown1();
    int b = unknown2();
    int res;
    int cnt;

    //pre-condition
    res = a;
    cnt = b;

    //loop-body
    while(cnt > 0){
        cnt = cnt - 1;
        res = res + 1;
    }

    //post-condition
    //@ assert(res == a + b);
        
}