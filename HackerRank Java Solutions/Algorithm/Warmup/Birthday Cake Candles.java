// Birthday Cake Candles
// Colleen is turning  years old! Therefore, she has  candles of various heights on her cake, and candle  has height . Because the taller candles tower over the shorter ones, Colleen can only blow out the tallest candles.

// Given the  for each individual candle, find and print the number of candles she can successfully blow out.

// Input Format

// The first line contains a single integer, , denoting the number of candles on the cake.
// The second line contains  space-separated integers, where each integer  describes the height of candle .

// Output Format

// Print the number of candles Colleen blows out on a new line.

// Sample Input 0

// 4
// 3 2 1 3
// Sample Output 0

// 2

import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;

public class Solution {

    static int birthdayCakeCandles(int n, int[] ar) {
        // Complete this function
        int max = 0;
        int frequency = 0;
        for(int i = 0; i < n ; i++){
            int height = ar[i];
            if(height > max){
                max = height;
                frequency = 1;
            }else if(height == max){
                frequency++;
            }
        }
        return frequency;
    }

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int n = in.nextInt();
        int[] ar = new int[n];
        for(int ar_i = 0; ar_i < n; ar_i++){
            ar[ar_i] = in.nextInt();
        }
        int result = birthdayCakeCandles(n, ar);
        System.out.println(result);
    }
}

//Java 8
/*
Initial Thoughts:
We can keep a running max and update it if we
find something larger, if we find something smaller
we just keep looking and if we find something equal
then we increment a counter variable

Time Complexity: O(n) //We must check the height of every candle
Space Complexity: O(1) //We only store a max and a frequency
*/

public class Solution2 {

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int n = in.nextInt();
        int tallest = 0;
        int frequency = 0;


        for(int i=0; i < n; i++){
            int height = in.nextInt();

            if(height > tallest){
                tallest = height;
                frequency = 1;
            }
            else if(height == tallest) frequency++;
        }
        System.out.println(frequency);
    }
}
