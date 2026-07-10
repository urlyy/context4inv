//svcomp_benchmark29_linear
/*@
    requires x < y;
*/
void ffoo(int x, int y){
    //pre-condition

    //loop-body
    while (x < y) {
        x = x + 100;
    }

    //post-condition
    //@ assert(x >= y);
}