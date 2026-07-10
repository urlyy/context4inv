//svcomp_benchmark48_linear
/*@ ensures \result > 0; */
int unknown2();

/*@
    requires i < j;
*/
void foo(int i,int j){
    int k = unknown2();

    //pre-condition

    //loop-body
    while (i < j) {
        k = k + 1;
        i = i + 1;
    }

    //post-condition
    //@ assert(k > j - i);
}