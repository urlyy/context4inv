//svcomp_Mono5_1
void fmain(){
    int x;
    int z;

    //pre-condition
    x = 0;
    z = 5000000;

    //loop-body
    while(x < 10000000){	
		if(x >= 5000000){
            z--;
        }
		x++;
	}


    //post-condition
    //@ assert(z == 0);
}