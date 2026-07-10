//svcomp_benchmark12_linear
int main(){
    int x;
    int y;
    int t;

    //pre-condition
    y = t; 
    //@ assume(x != y);

    //loop-body
    int unknown1, unknown2;
    while(unknown1!=0){
        unknown1 = unknown2;
        if(x > 0){
            y = y + x;
        }
    }

    //post-condition
    //@ assert(y >= t);
}