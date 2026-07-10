//SyGuG2018_fib_01
int main(){
    int x;
    int y;

    //pre-condition
    x = 1;
    y = 1;
    int unknown1, unknown2;
    //loop-body
    while(unknown1!=0){
        x = x + y;
        y = x + y;
        unknown1 = unknown2;
    }

    //post-condtion
    //@ assert(y >= 1)
}