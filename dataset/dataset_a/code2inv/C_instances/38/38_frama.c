/*@ ensures \result > 0; */
int unknown1();

void fmain() {
    int n = unknown1();
    int c = 0;
    
    while (unknown()) {
        if(c == n) {
            c = 1;
        }
        else {
            c = c + 1;
        }
    }
    //@ assert( (c == n)==>(c >= 0) );
}