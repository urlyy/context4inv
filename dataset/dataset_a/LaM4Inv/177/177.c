//SyGuG2018_fib_33ns
int main(){
    int x;
    int y;
    int z;
    int c;
    int k;
    int turn;

    //pre-condition
    x = 0;
    y = 0;
    turn = 0;
    //@ assume(z == k);

    int unknown1, unknown2, unknown3, unknown4, unknown5, unknown6, unknown7, unknown8;

    //loop-body
    while(unknown1!=0){
        unknown1 = unknown2;
        if(turn == 0){
            c = 0;
            if(unknown3!=0){
                turn = 1;
            }
            else{
                turn = 2;
            }
            unknown3 = unknown4;
        }
        else if(turn == 1){
            if(z == (k + y - c)){
                y = y + 1;
                x = x + 1;
                c = c + 1;
                turn = 2;
            }
            else{
                y = y - 1;
                x = x + 1;
                c = c + 1;
                if(unknown5!=0){
                    turn = 2;
                }
                unknown5 = unknown6;
            }
        }
        else if(turn == 2){
            x = x - 1;
            y = y - 1;
            if(unknown7!=0){
                turn = 3;
            }
            unknown7 = unknown8;
        }
        else if(turn > 2 || turn < 0){
            z = x + y;
            turn = 0;
        }
    }

    //post-condition
    //@ assert(x == y)
}