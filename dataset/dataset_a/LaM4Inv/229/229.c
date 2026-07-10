//svcomp_benchmark32_linear
int main() {
    int x;

    //pre-condition
    //@ assume(x == 1 || x == 2);

    //loop-body
    int unknown1, unknown2;
    while(unknown1!=0){
        unknown1 = unknown2;
        if(x == 1) {
            x=2;
        }else if(x == 2){
            x=1;
        }
    }

    //post-condition
    //@ assert(x <= 8);
}