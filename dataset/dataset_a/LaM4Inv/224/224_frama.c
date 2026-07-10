//svcomp_mod4
void foo(){
    int x;

    //pre-condition
    x = 0;

    //loop-body
    while(unknown()){
        x = x + 4;
    }

    //post-condition
    //@ assert(x % 4 == 0);
    
}
