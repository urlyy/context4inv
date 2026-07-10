//SyGuG2018_mirror2
/*@ ensures \result <= 1 && \result >= 0; */
int unknown1();

void foo(){
    int x = unknown1();
    int y;

    //pre-condition
    y = -3;
    //loop-body
    while(unknown()){
        if(x - y < 2){
            x = x - 1;
            y = y + 2;
        }
        else if(x - y >= 2){
            y = y + 1;
        }
    }

    //post-condition
    //@ assert(x <= 1);
    
}