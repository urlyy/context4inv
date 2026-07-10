//SyGuG2018_fib_14
int main(){
    int a;
    int j;
    int m;

    //pre-condition
    a = 0;
    j = 1;
    //@ assume(m > 0);

    //loop-body
    int unknown1, unknown2;
    while(j <= m){
        if(unknown1!=0){
            a = a + 1;
        }
        else{
            a = a - 1;
        }
        unknown1 = unknown2;
        j = j + 1;
    }

    //post-condition
    //@ assert((j > m)=>(a <= m))
}