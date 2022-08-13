
/**   
* Copyright: Copyright (c) 2018 Fan Li
* 
* @author: fan
* @date: 8 Feb 2018
*
*/
import java.sql.*;

public class DbConnect {

	// JDBC 驱动名及数据库 URL
	static final String DB_URL = "jdbc:mysql://localhost:3306/16212155?characterEncoding=utf8&useSSL=true";

	// 数据库的用户名与密码，需要根据自己的设置
	static final String USER = "root";
	static final String PASS = "697094";

	public static void main(String[] args) {
		Connection conn = null;
		Statement stmt = null;
		PreparedStatement pstmt = null;
		try {
			// 注册 JDBC 驱动
			Class.forName("com.mysql.jdbc.Driver");

			// 打开链接
			System.out.println("连接数据库...");
			conn = DriverManager.getConnection(DB_URL, USER, PASS);

			// 执行查询
			System.out.println("实例化Statement对...");
			stmt = conn.createStatement();
			String sql = "SELECT student_id, name, dept_name, age FROM student";
			ResultSet rs = stmt.executeQuery(sql);

			// pstmt = con.prepareStatement(
			// "UPDATE EMPLOYEES " +
			// "SET CAR_NUMBER = ? " +
			// "WHERE EMPLOYEE_NUMBER = ?");
			//
			// pstmt.setInt(1, carNo);
			// pstmt.setInt(2, empNo);
			// pstmt.executeUpdate();

			// 展开结果集数据库
			while (rs.next()) {
				// 通过字段检索
				int id = rs.getInt("student_id");
				String name = rs.getString("name");
				String dept_name = rs.getString("dept_name");
				int age = rs.getInt("age");

				// 输出数据
				System.out.print("ID: " + id);
				System.out.print(", Name: " + name);
				System.out.print(", Dept: " + dept_name);
				System.out.print(", Age: " + age);
				System.out.print("\n");
			}
			// 完成后关闭
			rs.close();
			stmt.close();
			conn.close();
		} catch (SQLException se) {
			// 处理 JDBC 错误
			se.printStackTrace();
		} catch (Exception e) {
			// 处理 Class.forName 错误
			e.printStackTrace();
		} finally {
			// 关闭资源
			try {
				if (stmt != null)
					stmt.close();
			} catch (SQLException se2) {
			} // 什么都不做
			try {
				if (conn != null)
					conn.close();
			} catch (SQLException se) {
				se.printStackTrace();
			}
		}
		System.out.println("Goodbye!");
	}
}