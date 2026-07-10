//SyGuG2018_cars
/*@ 
  requires v3 >= 0;
  requires v1 <= 5;
  requires (v1 - v3) >= 0;
  requires v2 * 2 - v1 - v3 == 0;
  requires v2 + 5 >= 0;
  requires v2 <= 5;
*/
void foo(int v1,int v2, int v3){
    int x1;
    int x2;
    int x3;
    int t;

    //pre-condition
    x1 = 100;
    x2 = 75;
    x3 = -50;
    t = 0;
    while(v2 + 5 >= 0 && v2 <= 5){
        x1 = x1 + v1;
        x3 = x3 + v3;
        x2 = x2 + v2;
        if(x2 * 2 - x1 - x3 >= 0){
            v2 = v2 - 1;
        }
        else if(x2 * 2 - x1 - x3 <= 0){
            v2 = v2 + 1;
        }
        t = t + 1;
    }
    //post-confition
    //@ assert(v2 * 2 + t * 2 >= v1 + v3);
}
