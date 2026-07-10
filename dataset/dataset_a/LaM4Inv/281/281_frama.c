//svcomp_benchmark29_linear
/*@
    requires x < y;
    requires y <= 20000001;
*/
void foo(int x,int y){
    //pre-condition

    //loop-body
    while (x < y) {
        x = x + 100;
    }

    //post-condition
    //@ assert(x <= y + 99);
}