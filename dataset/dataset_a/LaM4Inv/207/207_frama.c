//SyGuG2018_terminator_03_true-unreach-call_true-termination
/*@ ensures \result <= 1000000; */
int unknown1();

void foo(){
    int x;
    int y = unknown1();

    //pre-condition

    //loop-body
    while(x < 100 && y > 0){
        x = x + y;
    }
    //@ assert((y <= 0 || (y > 0 && x >= 100))==>(y <= 0 || (x >= 100 && y > 0)));
}