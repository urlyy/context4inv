//svcomp_benchmark21_disjunctive
/*@
    requires x > 0 || y > 0;
*/
void ffoo(int x,int y){

    //pre-condition

    //loop-body
    while (x + y <= -2) {
        if (x > 0) {
            x++;
        } 
        else {
            y++;
        }
  }

    //post-condition
    //@ assert(x > 0 || y > 0);
}