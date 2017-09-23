// Staircase
// Consider a staircase of size :

//    #
//   ##
//  ###
// ####
// Observe that its base and height are both equal to n, and the image is drawn using # symbols and spaces. The last line is not preceded by any spaces.

// Write a program that prints a staircase of size n .

// Input Format

// A single integer, , denoting the size of the staircase.

// Output Format

// Print a staircase of size  using # symbols and spaces.

// Note: The last line must have  spaces in it.

// Sample Input

// 6
// Sample Output

//      #
//     ##
//    ###
//   ####
//  #####
// ######


import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;

public class Solution1 {

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int n = in.nextInt();
        String rstr="";
        for(int i=0; i < n; i++){
            rstr+="#";
            System.out.format("%"+n+"s%n",rstr);
        }
    }
}

public class Solution2 {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int n = in.nextInt();
        char [] arreglo = new char [n];
        Arrays.fill(arreglo, ' ');
        int i = 0;
        for (i = 1; i <= n; i++){
            arreglo[n-i] = '#';
            System.out.println(arreglo);
        }
    }
}

public class Solution3 {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();

        for (int i = 1; i <= n; i++) {
            int pt = n - i;
            for (int c = 1; c <= pt; c++) {
                System.out.print(" ");
            }
            for (int c = 1; c <= i; c++) {
                System.out.print("#");
            }
            if (i < n) {
                System.out.println();
            }
        }
    }
}


public class Solution4 {
    // 理论正确 但不满足最后一行空白
    // nb ： print  println的区别
   public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        for (int i = 0; i < n; i++) {
            int pt = n - i;
            for (int c = 0; c < pt; c++) {
                System.out.print(" ");
            }
            for (int c = 0; c < i + 1; c++) {
                System.out.print("#");
            }
            if (i < n) {
                System.out.println();
            }
        }
    }
}
