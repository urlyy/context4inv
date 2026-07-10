//svcomp_loopv1
/*@ ensures \result <= 50000001; */
int unknown1();

void foo(){
    int n = unknown1();
    int i;
    int j;

    //pre-condition
    i = 0;
    j = 0;

    //loop-body
    while(i < n){  
        if(unknown())
            i = i + 6;
        else
            i = i + 3;
    }

    //post-condition
    //@ assert(i % 3 == 0);
}