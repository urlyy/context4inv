//SyGuG2018_fib_25n
int main(){
    int x;
    int y;
    int i;
    int j;
    int turn;

    //pre-condition
    x = 0;
    y = 0;
    i = 0;
    j = 0;
    turn = 0;

    //loop-body
    int unknown1, unknown2, unknown3, unknown4;
    while((turn >= 0) && (turn < 3)){
        if(turn == 0){
            if(unknown1!=0){
                turn = 1;
            }
            else{
                turn = 2;
            }
            unknown1 = unknown2;
        }
        else if(turn == 1 && x == y){
            if (x == y)
                i = i + 1;
            else{
                j = j + 1;
            }
            if(unknown3!=0){
                turn = 1;
            }
            else{
                turn = 2;
            }
            unknown3 = unknown4;
        }
        else if(turn == 2 && i >= j){
            if(i >= j)
                x = x + 1;
            y = y + 1;
            turn = 0;
        }
    }

    //post-condition
    //@ assert(i >= j);
}