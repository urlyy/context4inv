//svcomp_eq1
int main() {
    int w;
    int x;
    int y;
    int z;

    //pre-condition
    x = w;
    z = y;
    //@ assume(x > 0);
    //@ assume(y > 0);
    //@ assume(z > 0);
    //@ assume(w > 0);
    int unknown1, unknown2, unknown3, unknown4;
    while(unknown1!=0) {
        unknown1 = unknown2;
        if (unknown3!=0) {
            w = w + 1; 
            x = x + 1;
        } else {
            y = y - 1; 
            z = z - 1;
        }
        unknown3 = unknown4;
    }

    //post-condition
    //@ assert(w == x);
}
