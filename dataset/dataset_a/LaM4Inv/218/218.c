//svcomp_bin-suffix-5
int main(){
    int x;

    //pre-condiiton
    x = 5;

    //loop-body
    int unknown1, unknown2;
    while(unknown1!=0){
        unknown1 = unknown2;
        x = x + 8;
    }

    //post-condition
    //@ assert((x % 8) == 5);
}
