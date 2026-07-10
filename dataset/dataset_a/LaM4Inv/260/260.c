//svcomp_mine2017-ex4.8
int main(){
    int x;

    //pre-condition
    x = 0;

    //loop-body
    int unknown1, unknown2;
    while(unknown1!=0){
        unknown1 = unknown2;
        if(x == 0){
            x = 1;
        }
    }

    //post-condition
    //@ assert(x <= 1);
}
