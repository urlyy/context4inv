//svcomp_odd
int main(){
    int x;

    //pre-condition
    x = 1;

    //loop-body
    int unknown1, unknown2;
    while(unknown1!=0){
        unknown1 = unknown2;
        x = x + 2;
    }

    //post-condition
    //@ assert(x % 2 == 1);
    
}
