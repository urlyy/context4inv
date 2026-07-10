
int main() {
    int n;
    int c = 0;
    //@ assume(n > 0)
    int unknown1, unknown2;
    while (unknown1!=0) {
        if(c == n) {
            c = 1;
        }
        else {
            c = c + 1;
        }
        unknown1 = unknown2;
    }
    //@ assert( (c == n)=>(c >= 0) )
}
