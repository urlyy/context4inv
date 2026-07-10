int main(int n) {
    int sum, i;
    if ((1 <= n && n <= 1000)){
        sum = 0;
        for(i = 1; i <= n; i++) {
            sum = sum + i;
        }
        //@ assert(2*sum == n*(n+1));
    }
    return 0;
}
