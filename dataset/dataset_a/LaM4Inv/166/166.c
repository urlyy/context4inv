//SyGuG2018_fib_20
int main(){
    int x;
    int y;
    int k;
    int j;
    int i;
    int n;
    int m;

    //pre-condition
    m = 0;
    j = 0;
    //@ assume((x + y) == k);

    int unknown1, unknown2, unknown3, unknown4;

    //loop-body
    while(j < n){
        if(j == i){
            x = x + 1;
            y = y - 1;
            j = j + 1;
            if(unknown1!=0){
                m = j;
            }
            unknown1 = unknown2;
        }
        else if(j != i){
            x = x - 1;
            y = y + 1;
            j = j + 1;
            if(unknown3!=0){
                m = j;
            }
            unknown3=unknown4;
        }

    }

    //post-condition
    //@ assert((j >= n)=>((x + y) == k))
}