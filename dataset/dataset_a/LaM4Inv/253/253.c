//svcomp_ddlm2013
int main(){
    int i;
    int j;
    int a;
    int b;

    //pre-condition
    a = 0;
    b = 0;
    j = 1;
    i = 1;

    //loop-body
    int unknown1, unknown2;
    while(unknown1!=0){
        unknown1 = unknown2;
        a = a + 1;
        b = b + j - i;
        i = i + 2;
        if (i % 2 == 0){
            j = j + 2;
        }
        else{
            j = j + 1;
        }
    }
    
    //post-condition
    //@ assert((a != 0)=>(a != b))
}
