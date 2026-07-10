//svcomp_loopv3
void foo(){
    int i;
    int j;

    //pre-condition
    i = 0;

    //loop-body
    while(i < 50000001){  
        if(unknown())
            i = i + 8;
        else
            i = i + 4;
    }

    //post-condition
    //@ assert((j == (i / 4))==>((j * 4) == i));
}