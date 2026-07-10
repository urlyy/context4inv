//SyGuG2018_terminator_02_true-unreach-call_true-termination
int main(){
    int x;
    int z;

    //pre-condition
    //@ assume(x > -100);
    //@ assume(x < 200);
    //@ assume(z > 100);
    //@ assume(z < 200);

    //loop-body
    int unknown1, unknown2;
    while(x < 100 && z > 100){
        if(unknown1!=0){
            x = x + 1;
        }else{
            x = x - 1;
            z = z - 1;
        }
        unknown1=unknown2;
    }

    //post-condition
    //@ assert((x < 100 && z > 100) || x >= 100 || z <=100);
    
}