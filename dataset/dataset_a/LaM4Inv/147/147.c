//SyGuG2018_ex1
int main(){
    int x;
    int y;
    int xa;
    int ya;

    //pre-condition
    xa = 0;
    ya = 0;

    //loop-body
    int unknown1, unknown2, unknown3, unknown4;
    while(unknown1!=0){
        x = xa + ya * 2 + 1;
        if(unknown2!=0){
            y = ya - xa * 2 + x;
        }
        else{
            y = ya - xa * 2 - x;
        }
        xa = x - y * 2;
        ya = x * 2 + y;
        unknown1 = unknown3;
        unknown2 = unknown4;
    }
    
    //post-condtion
    //@ assert(xa + ya * 2 >= 0)
}