//svcomp_benchmark42_conjunctive
/*@
    requires (x == y);
    requires (x >= 0);
    requires (x + y + z == 0);
*/
void ffoo(int x,int y,int z){
    //pre-condition

    //loop-body
    while (x > 0) {
        x--;
        y--;
        z += 2;
    }

    //post-condition
    //@ assert(z <= 0);
}