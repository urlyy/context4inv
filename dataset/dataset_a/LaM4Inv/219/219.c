//svcomp_const
int main() {
    int s;

    //pre-condition
    s = 0;

    //loop-body
    int unknown1, unknown2;
    while(unknown1!=0){
        unknown1 = unknown2;
        if (s != 0){
            s = s + 1;
        }
    }

    //post-condition
    //@ assert(s == 0);

}
