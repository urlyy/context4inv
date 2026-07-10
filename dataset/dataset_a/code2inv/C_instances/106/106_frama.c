
/*@ ensures \result <= m; */
int unknown1();
/*@ ensures \result < 1; */
int unknown2();

void fmain() {
    int a,m,j,k;

    
    
    k = 0;

    while ( k < 1) {
        if(m < a) {
            m = a;
        }
        k = k + 1;
    }

    //@ assert( a >= m);
}
