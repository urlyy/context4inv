//svcomp_benchmark01_conjunctive
int main(){
    int x;
    int y;

    //pre-condition
    x = 1;
    y = 1;

    //loop-body
    int unknown1, unknown2;
    while(unknown1!=0){
        unknown1 = unknown2;
        x = x + y;
        y = x;
    }

    //post-condition
    //@ assert(y >= 1);
}
