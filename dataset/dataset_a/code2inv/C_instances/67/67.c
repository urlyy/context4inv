
int main(int n, int y) {
    int x = 1;

    while (x <= n) {
        y = n - x;
        x = x +1;
    }
    //@ assert((n > 0)=>(y >= 0))
}
