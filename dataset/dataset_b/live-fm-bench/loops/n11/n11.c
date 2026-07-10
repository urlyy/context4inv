int main(){
   int a[5];
   unsigned int len=0;
   int i;
   int unknown1, unknown2;
   while(unknown1!=0){
      unknown1 = unknown2;
      if (len==4){
         len =0;
      }
      a[len]=0;
      len++;
   }
   //@ assert(len>=0 && len<5);
   return 1;
}
