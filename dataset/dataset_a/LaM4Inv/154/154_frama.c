//SyGuG2018_fib_11
/*@ ensures \result > 0; */
int unknown1();

void foo(){
    int x = unknown1();
    int i;
    int j;

    //pre-condition
    j = 0;
    i = 0;

    //loop-body
    while(i < x){
        j = j + 2;
        i = i + 1;
    }

    //post-condition
    //@ assert((i >= x)==>(j == 2 * x));
}