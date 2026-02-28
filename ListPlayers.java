import java.sql.*;

public class ListPlayers {
    public static void main(String[] args) {

        String url = "jdbc:postgresql://localhost/photon";
		String user = "student";
		String password = "student";   // now required

        try (
            Connection conn = DriverManager.getConnection(url, user, password);
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT * FROM public.players");
        ) {
            System.out.println("Connected via peer authentication.\n");

            ResultSetMetaData meta = rs.getMetaData();
            int cols = meta.getColumnCount();

            int rows = 0;
            while (rs.next()) {
                rows++;
                for (int i = 1; i <= cols; i++) {
                    System.out.print(meta.getColumnName(i) + "=" + rs.getObject(i) + " ");
                }
                System.out.println();
            }

            System.out.println("\nRows returned: " + rows);

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
