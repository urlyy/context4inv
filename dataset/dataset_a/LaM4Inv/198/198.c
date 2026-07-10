//SyGuG2018_jmbl_hola_20
int main(){
    int x;
    int y;
    int i;
    int j;
    int k;
    int m;
    int n;

    //pre-condition
    m = 0;
    j = 0;
    //@ assume(k == x + y);

    //loop-body
    int unknown1, unknown2;
    while(j < n){
        if(unknown1!=0){
            m = j;
        }
        unknown1 = unknown2;
        if(j == i){
            x = x + 1;
            y = y - 1;
        }
        else{
            x = x - 1;
            y = y + 1;
        }
        j = j + 1;
    }

    //post-condition
    //@ assert((n > 0)=>(m < n))
}