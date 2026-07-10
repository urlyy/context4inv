//svcomp_mod3
int main() {
    unsigned int x;
    unsigned int y;

    //pre-condition
    y = 1;

    //loop-body
    int unknown1, unknown2, unknown3,unknown4;
    while(unknown1!=0){
        unknown1=unknown2;
        if(x % 3 == 1){
            x = x + 2; 
            y = 0;
        }
        else{
            if(x % 3 == 2){
                x = x + 1; 
                y = 0;
            }
            else{
                if(unknown3!=0){
                    x = x + 4; 
                    y = 1;
                }
                else{
                    x = x + 5; 
                    y = 1;
                }
                unknown3=unknown4;
            }
        }
    }

    //post-condition
    //@ assert((y == 0)=>(x % 3 == 0))
}