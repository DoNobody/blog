import java.util.List;
import java.util.Vector;

public class Test {
   
    public static int fib(int N) {
       if (N < 1)
           return 0;
       Vector<Integer> v = new Vector<Integer>(N);
       for (int i = 0; i < N; i++) {
           v.add(i,0);
       }
       return helper(v, N);
    }

    public static int helper(Vector<Integer> v, int n) {
       if (n == 1 || n == 2)
           return 1;
       if (!v.get(n-1).equals(0))
           return v.get(n-1);
       v.set(n-1, helper(v, n - 1) + helper(v, n - 2));
       return v.get(n-1);
   }

   public static void main(String[] args) {
       System.out.println(fib(10));
   }
}
