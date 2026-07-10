//SyGuG2018_mirror1
int main(){
    int x;

    //pre-condition
    //@ assume(x <= -2);
    //@ assume(x >= -3);

    //loop-body
    int unknown1, unknown2;
    while(unknown1!=0){
        unknown1 = unknown2;
        if(x < 1){
            x = x + 2;
        }
        else if(x >= 1){
            x = x + 1;
        }
    }

    //post-condition
    //@ assert(x >= -5);
    
}