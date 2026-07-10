//svcomp_bin-suffix-5
void foo(){
    int x;

    //pre-condiiton
    x = 5;

    //loop-body
    while(unknown()){
        x = x + 8;
    }

    //post-condition
    //@ assert((x % 8) == 5);
}
