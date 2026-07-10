//svcomp_benchmark50_linear
/*@
    requires xa + ya > 0;
*/
void ffoo(int xa,int ya){
    //pre-condition
    //loop-body
    while (xa > 0) {
        xa--;
        ya++;
    }

    //post-condition
    //@ assert(ya >= 0);
}