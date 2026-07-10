//svcomp_loopv3
int main(){
    int i;
    int j;

    //pre-condition
    i = 0;

    //loop-body
    int unknown1,unknown2;
    while(i < 50000001){	
        if(unknown1!=0)
            i = i + 8;
        else
            i = i + 4;
        unknown1=unknown2;
	}

    //post-condition
    //@ assert((j == (i / 4))=>((j * 4) == i))
}