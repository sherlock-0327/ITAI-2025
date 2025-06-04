
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class NQueens {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = getValidN(scanner);
        System.out.println("是否只输出一个解？(y/n)");
        boolean onlyOneSolution = scanner.nextLine().equalsIgnoreCase("y");

        long startTime = System.currentTimeMillis(); // 开始计时

        NQueensSolver solver = new NQueensSolver(n);
        List<int[]> solutions = solver.solve(onlyOneSolution);

        long endTime = System.currentTimeMillis(); // 结束计时
        long totalTime = endTime - startTime;

        if (solutions.isEmpty()) {
            System.out.println("无解");
        } else {
            for (int i = 0; i < solutions.size(); i++) {
                System.out.println("解 " + (i + 1) + ":");
                printBoard(solutions.get(i));
                System.out.println();
            }
            System.out.println("总共有 " + solutions.size() + " 个解");
        }

        System.out.println("程序运行时间：" + totalTime + " 毫秒"); // 输出运行时间

        scanner.close();
    }

    private static int getValidN(Scanner scanner) {
        int n;
        while (true) {
            System.out.print("请输入N (N ≥ 4): ");
            try {
                n = Integer.parseInt(scanner.nextLine());
                if (n >= 4) {
                    return n;
                } else {
                    System.out.println("错误：N必须大于等于4，请重新输入。");
                }
            } catch (NumberFormatException e) {
                System.out.println("错误：请输入有效的整数。");
            }
        }
    }

    private static void printBoard(int[] solution) {
        int n = solution.length;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                System.out.print(solution[i] == j ? "Q " : ". ");
            }
            System.out.println();
        }
    }
}

class NQueensSolver {
    private final int n;
    private final List<int[]> solutions = new ArrayList<>();

    public NQueensSolver(int n) {
        this.n = n;
    }

    public List<int[]> solve(boolean onlyOneSolution) {
        int[] board = new int[n];
        backtrack(0, board, onlyOneSolution);
        return solutions;
    }

    private void backtrack(int row, int[] board, boolean onlyOneSolution) {
        if (row == n) {
            solutions.add(Arrays.copyOf(board, n));
            return;
        }

        for (int col = 0; col < n; col++) {
            if (isValid(row, col, board)) {
                board[row] = col;
                backtrack(row + 1, board, onlyOneSolution);
                if (onlyOneSolution && !solutions.isEmpty()) {
                    return;
                }
            }
        }
    }

    private boolean isValid(int row, int col, int[] board) {
        for (int i = 0; i < row; i++) {
            int otherCol = board[i];
            if (otherCol == col || Math.abs(row - i) == Math.abs(col - otherCol)) {
                return false;
            }
        }
        return true;
    }
}    