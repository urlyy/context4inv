//svcomp_mine2017-ex4.7
int main(){
    int x;

    //pre-condition
    x = 0;

    //loop-body
    int unknown1, unknown2,unknown3,unknown4;
    while (unknown1!=0) {
        unknown1 = unknown2;
        if(unknown3!=0){
            x = x + 1;
            if(x > 40){
                x = 0;
            }
        }
        unknown3=unknown4;

    }

    //post-condition
    //@ assert(x >= 0);
}
