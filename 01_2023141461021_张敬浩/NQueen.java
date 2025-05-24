import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class NQueen {
    //记录答案数量
    private static long cnt = 0;

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n;
        while (true) {
            System.out.print("请输入棋盘大小");
            if (!scanner.hasNextInt()) {
                System.out.println("请输入一个大于等于4的数字");
                scanner.next();
                continue;
            }
            n = scanner.nextInt();
            if (n < 3) {
                System.out.println("数字必须大于等于4");
                continue;
            }
            break;
        }

        boolean showOnlyOneSolution = false;
        while (true) {
            System.out.print("是否只需求解出一个解？(是/否)");
            String choice = scanner.next();
            if (choice.equalsIgnoreCase("是")) {
                showOnlyOneSolution = true;
                break;
            }
            if (choice.equalsIgnoreCase("否")) {
                showOnlyOneSolution = false;
                break;
            }
            System.out.println("请输入“是”或“否”");
        }

        //进行n皇后的计算
        System.out.println("棋盘布局为");
        long startTime = System.nanoTime() / 1000;
        solveNQueens(n, showOnlyOneSolution);
        long endTime = System.nanoTime() / 1000;
        if (!showOnlyOneSolution) {
            System.out.println("共有" + cnt + "个解");
            System.out.println("共消耗" + (endTime - startTime) + " 微秒");
        }
    }

    private static void solveNQueens(int n, boolean showOnlyOneSolution) {
        //创建参数
        int[] row = new int[n];
        boolean[] col = new boolean[n];
        boolean[] diagonal1 = new boolean[2 * n - 1];
        boolean[] diagonal2 = new boolean[2 * n - 1];
        //进行回溯
        backtracking(n, 0, row, col, diagonal1, diagonal2, showOnlyOneSolution);
    }

    /**
     * @param m         棋盘大小为m×m
     * @param n         已经放了n个皇后
     * @param row       将第i行的皇后放在第row[i - 1]列，即(i,row[i - 1] + 1)（如果从0开始计数应该为(i - 1,row[i - 1])）
     * @param col       这一列放皇后了吗
     * @param diagonal1 这一主对角线放皇后了吗，以该行号减列号（还需再加一个偏移量）来唯一标识一个主对角线
     * @param diagonal2 这一副对角线放皇后了吗，以该行号加列号来唯一标识一个副对角线
     */
    private static void backtracking(int m, int n, int[] row, boolean[] col, boolean[] diagonal1, boolean[] diagonal2, boolean showOnlyOneSolution) {
        /**
         * 已经放了n个皇后了，打印结果即可
         */
        if (n == m) {
            List<String> board = new ArrayList<>();
            for (int i : row) {
                //对于每一行，皇后放在了第row位置，取出打印即可
                char[] c = new char[n];
                Arrays.fill(c, '.');
                c[i] = 'Q';
                board.add(new String(c));
            }
            System.out.println(board);
            cnt++;
            return;
        }
        /**
         * 这是要放置的第n+1个皇后
         * 默认将第n+1个皇后放置在第n行上（总共为0到m-1行）
         * 遍历每一列，找到那些没被其他皇后占的列，即col的值为false，并将皇后放置在该列
         * 假设皇后放置在了(n,i)，就将该位置的列，主对角线，副对角线的值设置为true表示被占领
         * 遍历下一个该放置的皇后
         * 取下这次放置的皇后进行回溯，将该位置的列，主对角线，副对角线的值设置为false表示未被占领
         */
        for (int i = 0; i < m; i++) {
            //如果该(n,i)位置所在的列，主对角线，副对角线没有被占就将该皇后放在这
            if (!col[i] && !diagonal1[n + i] && !diagonal2[n - i + m - 1]) {
                //标记n行皇后放在了第i列
                row[n] = i;
                //占领该列和对角线
                col[i] = true;
                diagonal1[n + i] = true;
                diagonal2[n - i + m - 1] = true;
                //放下一个（行）的皇后
                backtracking(m, n + 1, row, col, diagonal1, diagonal2, showOnlyOneSolution);
                //如果只求一个解，直接return
                if (cnt == 1 && showOnlyOneSolution) {
                    return;
                }
                //将这一行的皇后取下
                col[i] = false;
                diagonal1[n + i] = false;
                diagonal2[n - i + m - 1] = false;
            }
        }
    }
}