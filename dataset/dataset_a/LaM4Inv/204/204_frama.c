//SyGuG2018_mirror3
/*@ ensures \result <= 5 && \result >= 4; */
int unknown1();
/*@ ensures \result <= 5 && \result >= 4; */
int unknown2();

void foo(){
    int x = unknown1();
    int y = unknown2();

    //pre-condition
    //loop-body
    while(unknown()){
        if(x >= 0 && y >= 0){
            x = x - 1;
        }
        else if(x < 0 && y >= 0){
            y = y - 1;
        }
        else if(y < 0){
            x = x + 1;
            y = y - 1;
        }
    }

    //post-condition
    //@ assert(y <= 5);
    
}