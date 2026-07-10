//SyGuG2018_fib_37
int main(){
    int x;
    int n;
    int m;

    //pre-condition
    x = 0;
    m = 0;
    //@ assume(n > 0);

    //loop-body
    int unknown1, unknown2;
    while(x < n){
        if(unknown1!=0){
            m = x;
        }
        unknown1=unknown2;
        x = x + 1;
    }

    //post-condition
    //@ assert((x >= n && n > 0)=>(m < n))
}