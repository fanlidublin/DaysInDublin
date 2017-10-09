// Time conversion
// Given a time in -hour AM/PM format, convert it to military (-hour) time.

// Note: Midnight is 12:00:00 am on a 12-hour clock, and 00:00:00 on a 24-hour clock. Noon is 12:00:00 pm on a 12-hour clock, and 12:00:00 on a 24-hour clock.

// Sample Input

// 07:05:45PM

// Sample Output

// 19:05:45

import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.lang.*;
import java.util.regex.*;

public class Solution1{
    //Can not meet common test case due to the String outString format
    static String timeConversion(String s) {
        // Complete this function
        String[] newS = s.split(":");
        String ampm = newS[2].substring(2,4);
        int h = Integer.parseInt(newS[0]);
        // int m = Integer.parseInt(newS[1].substring(0,2));
        String m = newS[1];
        // int ss = Integer.parseInt(newS[2].substring(0,2));
        String ss = newS[2].substring(0,2);
        if(ampm.equals("AM") && h==12){
            h = 0;
        }else if(ampm.equals("PM") && h<12){
            h = h+12;
        }
        String outString = h + ":" + m + ":" + ss;
        return outString;
    }

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        String s = in.next();
        String result = timeConversion(s);
        System.out.println(result);
    }
}



public class Solution2{

    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String time = scan.next();
        String tArr[] = time.split(":");
        String AmPm = tArr[2].substring(2,4);
        int hh,mm,ss;
        hh = Integer.parseInt(tArr[0]);
        mm = Integer.parseInt(tArr[1]);
        ss = Integer.parseInt(tArr[2].substring(0,2));

        String checkPM = "PM",checkAM ="AM";
        int h = hh;
        if(AmPm.equals(checkAM) && hh==12)
            h=0;
        else if(AmPm.equals(checkPM)&& hh<12)
            h+=12;
        System.out.printf("%02d:%02d:%02d",h,mm,ss);
    }
}
