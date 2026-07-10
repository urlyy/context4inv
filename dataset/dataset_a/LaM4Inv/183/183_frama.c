//SyGuG2018_fib_43
/*@ 
  requires x != y;
  requires t == y;
*/
void foo(int x,int y,int t){
    int i;

    //pre-condition
    i = 0;

    //loop-body
    while(x > 0){
        y = x + y;
    }

    //post-condition
    //@ assert(y >= t);
}