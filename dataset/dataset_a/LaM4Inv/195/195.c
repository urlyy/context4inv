//SyGuG2018_jmbl_hola_05
int main(){
    int x;
    int y;
    int i;
    int j;

    //pre-condition
    i = 0;
    j = 0;
    x = 0;
    y = 0;

    //loop-body
    int unknown1, unknown2, unknown3, unknown4;
    while(unknown1!=0){
        unknown1 = unknown2;
        i = i + x + 1;
        if(unknown3!=0){
            j = j + y + 1;
        }
        else{
            j = j + y + 2;
        }
        unknown3 = unknown4;
        x = x + 1;
        y = y + 1;
    }

    //post-condition
    //@ assert(j >= i);
}