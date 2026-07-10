//svcomp_benchmark01_conjunctive
void foo(){
    int x;
    int y;

    //pre-condition
    x = 1;
    y = 1;

    //loop-body
    while(unknown()){
        x = x + y;
        y = x;
    }

    //post-condition
    //@ assert(y >= 1);
}