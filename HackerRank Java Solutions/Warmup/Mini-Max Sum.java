// Mini-Max Sum

// Given five positive integers, find the minimum and maximum values that can be calculated by summing exactly four of the five integers. Then print the respective minimum and maximum values as a single line of two space-separated long integers.

// Input Format

// A single line of five space-separated 【1，10^9】integers.

// Constraints

// Each integer is in the inclusive range .
// Output Format

// Print two space-separated long integers denoting the respective minimum and maximum values that can be calculated by summing exactly four of the five integers. (The output can be greater than 32 bit integer.)

// Sample Input

// 1 2 3 4 5
// Sample Output

// 10 14


import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;

public class Solution1 {
    // The idea is that always the max sum will be (totalSum - the min number) and min Sum will be (totalSum - maxNum)
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        long[] arr = new long[5];
        //typically wrong!!
        long min = 1, max = 1,  totalSum = 0;
        for(int arr_i=0; arr_i < 5; arr_i++){
            arr[arr_i] = in.nextLong();
            if(arr[arr_i] > max){
                max = arr[arr_i];
            }
            if(arr[arr_i] < min){
                min = arr[arr_i];
            }
            totalSum += arr[arr_i];
        }
        System.out.println( (totalSum - max) + " " + (totalSum - min));
    }
}

public class Solution2 {

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        long[] nums = new long[5];
        long max = 0, min= 0 , sum =0;
        nums[0] = max = min = sum = in.nextLong(); //Read the first value outside the loop, to handle min calculation
        for (int i = 1; i < 5; i++) {
            nums[i] = in.nextLong();
            if(nums[i]>max) max = nums[i];
            if(nums[i]<min) min = nums[i];
            sum += nums[i];
        }
        System.out.println( (sum - max) + " " + (sum - min));

    }
}

public class Solution3 {
    // avoid using array
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        long[] nums = new long[5];
        long max, min, sum;
        sum = max = min = in.nextLong();

        for(int i=1; i<5;i++){
            long temp = in.nextLong();
            sum += temp;
            if(max>temp){
                if(min > temp) {
                    min = temp;
                }
            } else {
                max = temp;
            }
        }
        System.out.print((sum -max) + " " + (sum - min));
    }
}
