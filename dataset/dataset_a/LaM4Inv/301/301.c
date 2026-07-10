//svcomp_loopv1
int main(){
    int n;
    int i;
    int j;

    //pre-condition
    i = 0;
    j = 0;
    //@ assume(n <= 50000001);

    //loop-body
    int unknown1,unknown2;
    while(i < n){	
        if(unknown1!=0)
            i = i + 6;
        else
            i = i + 3;
        unknown1=unknown2;
	}


    //post-condition
    //@ assert(i % 3 == 0);
}