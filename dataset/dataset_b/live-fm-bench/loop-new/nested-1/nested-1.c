int main(int n,int m) {
    int k = 0;
    int i,j;
    if (10 <= n && n <= 10000 && 10 <= m && m <= 10000){
        for (i = 0; i < n; i++) {
            for (j = 0; j < m; j++) {
                k ++;
            }
        }
        //@ assert(k >= 100);
    }
    return 0;
}
