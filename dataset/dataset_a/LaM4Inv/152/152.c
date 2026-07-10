//SyGuG2018_fib_09s
int main(){
    int i;
    int pvlen;
    int t;
    int k;
    int n;
    int j;
    int turn;

    //pre-condition
    k = 0;
    i = 0;
    turn = 0;

    //loop-body
    int unknown1, unknown2, unknown3, unknown4, unknown5, unknown6;
    while(turn < 5){
        if(turn == 0){
            i = i + 1;
            if(unknown1!=0){
                turn = 1;
            }
            unknown1 = unknown2;
        }
        else if(turn == 1){
            if(i > pvlen){
                pvlen = i;
            }
            i = 0;
            turn = 2;
        }
        else if(turn == 2){
            t = i;
            i = i + 1;
            k = k + 1;
            if(unknown3!=0){
                turn = 3;
            }
            unknown3 = unknown4;
        }
        else if(turn == 3){
            if(unknown5!=0){
                turn = 4;
            }
            unknown5 = unknown6;
        }
        else if(turn == 4){
            n = i;
            j = 0;
            turn = 5;
        }
    }

    //post-condition
    //@ assert(k >= 0);
}