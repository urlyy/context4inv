//svcomp_benchmark12_linear
/*@
    requires x != y;
*/
void ffoo(int x,int y){
    int t;

    //pre-condition
    y = t; 

    //loop-body
    while(unknown()){
        if(x > 0){
            y = y + x;
        }
    }

    //post-condition
    //@ assert(y >= t);
}