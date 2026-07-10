//SyGuG2018_fib_13
int main(){
    int j;
    int k;
    int t;

    //pre-condition
    j = 2;
    k = 0;

    //loop-body
    int unknown1, unknown2;
    while(unknown1!=0){
        if (t == 0){
            j = j + 4;
        }
        else {
            j = j + 2;
            k = k + 1;
        }
        unknown1 = unknown2;
    }

    //post-condition
    //@ assert((j != k * 2 + 2)=>(k == 0 && t == 0))
}