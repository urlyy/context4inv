//svcomp_benchmark03_linear
int main(){
    int x;
    int y;
    int i;
    int j;
    int flag;

    //pre-condition
    x = 0; 
    y = 0;
    i = 0;
    j = 0;

    //loop-body
    int unknown1, unknown2;
    while(unknown1!=0){
        unknown1 = unknown2;
        x = x + 1;
        y = y + 1;
        i = i + x;
        j = j + y;
        if(flag != 0) {
            j = j + 1;
        }
    }

    //post-condition
    //@ assert(j >= i);
}
