// A Very Big Sum

// You are given an array of integers of size . You need to print the sum of the elements in the array, keeping in mind that some of those integers may be quite large.

// Input Format

// The first line of the input consists of an integer . The next line contains  space-separated integers contained in the array.

// Output Format

// Print a single value equal to the sum of the elements in the array.

// Constraints


// Sample Input

// 5
// 1000000001 1000000002 1000000003 1000000004 1000000005
// Output

// 5000000015


import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;

public class Solution {

    static long aVeryBigSum(int n, long[] ar) {
        // Complete this function
        long sum = 0;
        for(int i = 0; i < n; i++){
            sum += ar[i];
        }
        return sum;
    }

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int n = in.nextInt();
        long[] ar = new long[n];
        for(int ar_i = 0; ar_i < n; ar_i++){
            ar[ar_i] = in.nextLong();
        }
        long result = aVeryBigSum(n, ar);
        System.out.println(result);
    }
}
