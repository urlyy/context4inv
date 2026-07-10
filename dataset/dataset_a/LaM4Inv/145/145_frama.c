//SyGuG2018_cggmp2005_variant_true-unreach-call_true-termination
/*@ ensures /result > 0; */
int unknown1();

void foo(){
    int lo;
    int mid = unknown1();
    int hi;

    //pre-condition
    lo = 0;
    hi = 2 * mid;
    
    //loop-body
    while(mid > 0){
        lo = lo + 1;
        hi = hi - 1;
        mid = mid - 1;
    }

    //post-condition
    //@ assert(lo == hi);
}