//SyGuG2018_fib_08
int main(){
    int x;
    int y;

    //pre-condition
    x = 0;
    y = 0;
    int unknown1, unknown2;
    //loop-body
    while(unknown1!=0){
        if(x >= 4){
            x = x + 1;
            y = y + 1;
        }
        else if(x < 0){
            y = y - 1;
        }
        else{
            x = x + 1;
            y = y + 100;
        }
        unknown1 = unknown2;
    }

    //post-condition
    //@ assert((x >= 4)=>(y > 2))
}