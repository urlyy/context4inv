//SyGuG2018_gsv2008_true-unreach-call_true-termination
/*@ ensures \result > -1000 && \result < 1000; */
int unknown1();

void foo(){
    int x;
    int y = unknown1();

    //pre-condition
    x = -50;

    //loop-body
    while(x < 0){
        x = x + y;
        y = y + 1;
    }

    //post-condition
    //@ assert(y > 0);
        
}