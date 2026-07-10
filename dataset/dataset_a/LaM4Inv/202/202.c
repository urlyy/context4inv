//SyGuG2018_mirror2
int main(){
    int x;
    int y;

    //pre-condition
    //@ assume(x <= 1);
    //@ assume(x >= 0);
    y = -3;
    //loop-body
    int unknown1, unknown2;
    while(unknown1!=0){
        unknown1 = unknown2;
        if(x - y < 2){
            x = x - 1;
            y = y + 2;
        }
        else if(x - y >= 2){
            y = y + 1;
        }
    }

    //post-condition
    //@ assert(y >= -3);
}