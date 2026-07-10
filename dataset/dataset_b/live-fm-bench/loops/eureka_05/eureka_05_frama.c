int foo(int *array){
   int SIZE = 5;
   int n = SIZE;
   int i;
	for(i=SIZE-1; i>=0; i--){
		array[i]=i;
   }
	int lh, rh, temp;
   for (lh = 0; lh < n; lh++) {
      rh = lh;
      for (i = lh + 1; i < n; i++){
         if (array[i] < array[rh]){
            rh = i;
         }
      }
      temp = array[lh];
      array[lh] = array[rh];
      array[rh] = temp;
   }
	//@ assert(\forall integer k; 0 <= k < SIZE ==> array[k] == k);
   return 0;
}
