
/*@ ensures \result <= m; */
int unknown1();

void fmain() {
    int a,c,m,j,k;

    
    j = 0;
    k = 0;

    while ( k < c) {
        if(m < a) {
            m = a;
        }
        k = k + 1;
    }

    //@ assert( a <=  m);
}
