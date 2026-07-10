//svcomp_benchmark38_conjunctive
int main(){
    int x;
    int y;

    //pre-condition
    x = 0;
    y = 0;

    //loop-body
    int unknown1, unknown2;
    while(unknown1!=0){
        unknown1 = unknown2;
        x += 4;
        y++;
    }

    //post-condition
    //@ assert(x == 4 * y);
}