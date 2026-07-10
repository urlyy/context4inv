//SyGuG2018_terminator_02_true-unreach-call_true-termination
/*@ ensures \result > -100 && \result < 200; */
int unknown1();
/*@ ensures \result > 100 && \result < 200; */
int unknown2();

void foo(){
    int x = unknown1();
    int z = unknown2();

    //pre-condition

    //loop-body
    while(x < 100 && z > 100){
        if(unknown()){
            x = x + 1;
        }else{
            x = x - 1;
            z = z - 1;
        }
    }

    //post-condition
    //@ assert((x < 100 && z > 100) || x >= 100 || z <=100);
    
}