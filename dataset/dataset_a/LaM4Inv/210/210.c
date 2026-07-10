//SyGuG2018_vardep
int main(){
    int x;
    int y;
    int z;

    //pre-condition
    x = 0;
    y = 0;
    z = 0;

    //loop-body
    int unknown1, unknown2;
    while(unknown1!=0){
        unknown1 = unknown2;
        x = x + 1;
        y = y + 2;
        z = z + 3;
    }

    //post-condition
    //@ assert(y >= 0);
    
}