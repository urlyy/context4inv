//SyGuG2018_fib_05_x
int main(){
    int x;
    int y;
    int i;
    int j;

    //pre-condition
    x = 0;
    y = 0;
    j = 0;
    i = 0;    


    int unknown1, unknown2, unknown3, unknown4;
    //loop-body
    while(unknown1!=0){
        x = x + 1;
        y = y + 1;
        i = x + i;
        if(unknown2!=0){
            j = y + j;
        }
        else{
            j = y + j + 1;
        }
        unknown1 = unknown3;
        unknown2 = unknown4;
    }

    //post-condtion
    //@ assert(j >= i);
}