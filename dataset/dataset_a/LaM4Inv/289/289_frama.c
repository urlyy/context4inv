//svcomp_benchmark44_disjunctive
/*@
    requires x < y;
    requires y <= 20000001;
*/
void ffoo(int x,int y){

    //pre-condition

    //loop-body
    while (x < y) {
        if ((x < 0 && y < 0)){
            x = x + 7; 
            y = y - 10;
        }
        else if ((x < 0 && y >= 0)){
            x = x + 7; 
            y = y + 3;
        } 
        else {
            x = x + 10; 
            y = y + 3;
        }

    }

    //post-condition
    //@ assert(x <= y + 16);
}