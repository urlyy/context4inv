//svcomp_benchmark32_linear
/*@ ensures \result == 1 || \result == 2; */
int unknown1();

void fmain() {
    int x = unknown1();

    //pre-condition

    //loop-body
    while(unknown()){
        if(x == 1) {
            x=2;
        }else if(x == 2){
            x=1;
        }
    }

    //post-condition
    //@ assert(x <= 8);
}