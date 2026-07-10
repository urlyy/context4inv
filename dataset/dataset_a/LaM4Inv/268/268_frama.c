//svcomp_benchmark05_conjunctive
/*@ ensures \result >= 0 && \result <= y; */
int unknown1();
/*@ ensures \result < n; */
int unknown2();
/*@
    requires x >= 0;
    requires x <= y;
    requires y < n;
*/
void foo(int x, int y, int n){

    //pre-condition

    //loop-body
    while (x < n) {
        x = x + 1;
        if(x > y){
            y = y + 1;
        }
    }

    //post-condition
    //@ assert(y == n);
}
