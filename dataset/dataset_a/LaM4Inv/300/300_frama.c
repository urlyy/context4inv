//svcomp_iftelse
/*@ ensures \result <= 20000001; */
int unknown1();

void foo(){
    int n = unknown1();
    int i;
    int k;
    int j;

    //pre-condition
    i = 0;
    j = 0;
    k = 0;

    //loop-body
    while(i < n){	
		i = i + 3;
        if((i % 2) != 0)
            j = j + 3;
        else
            k = k + 3;
	}

    //@ assert((n > 0)==>(i / 2 <= j));
    //post-condition
}