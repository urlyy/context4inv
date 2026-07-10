//SyGuG2018_mirror1
/*@ ensures \result <= -2 && \result >= -3; */
int unknown1();

void foo(){
    int x = unknown1();

    //pre-condition

    //loop-body
    while(unknown()){
        if(x < 1){
            x = x + 2;
        }
        else if(x >= 1){
            x = x + 1;
        }
    }

    //post-condition
    //@ assert(x >= -5);
    
}