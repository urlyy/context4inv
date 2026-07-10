//svcomp_eq2
/*@ ensures \result > 0; */
int unknown1();
/*@ ensures \result > 0; */
int unknown2();
/*@ ensures \result > 0; */
int unknown3();
/*@ ensures \result > 0; */
int unknown4();

void fmain(){
    int w = unknown4();
    int x = unknown1();
    int y = unknown2();
    int z = unknown3();

    //pre-condition
    x = w;
    z = x + 1;
    y = w + 1;

    //loop-body
    while(unknown()){
        y = y + 1;
        z = z + 1;
    }

    //post-conditon
    //@ assert(y == z);
}
