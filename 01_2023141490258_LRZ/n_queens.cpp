#include <cstdio>
#include <cmath>
#include <chrono>
int location[21];
int number;
int count = 0;

bool col[21] = {false}; 
bool d1[41] = {false};
bool d2[41] = {false};

using namespace std;

bool is_safe(int x, int y);
int print();

void n_queens(int now, int all) {

    if (now > all) {
        print();
        return;         // 边界条件
    }
    for (int y = 1; y <= all; y++) {
        if (is_safe(now, y)) {
            location[now] = y;
            col[y] = true;
            d1[now + y] = true;
            d2[now - y + number] = true;
            n_queens(now + 1, number);          // 取消标记
            col[y] = false;
            d1[now + y] = false;
            d2[now - y + number] = false;
        }
    }
}

bool is_safe(int x, int y) {
    if (col[y]) return false;
    if (d1[x + y]) return false;
    if (d2[x - y + number]) return false;
    return true;
}

int print() {
    /*for (int i = 1; i <= number; i++) {
        for (int j = 1; j <= number; j++) {
            if (location[i] != j) {
                putchar('o');
            } else {
                putchar('x');
            }
        }
        putchar('\n');
    }*/
    count++;
    //putchar('\n');
    return 0;
}

int main() {
    scanf("%d", &number);
    std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
    if (number < 4 || number > 20) {
        printf("Invalid input.\n");
        return -1;
    }
    n_queens(1, number);
    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
    std::chrono::duration<double> elapsed_miliseconds = end - start;
    printf("Total solutions: %d\n", count);
    printf("Time taken: %.3f ms\n", elapsed_miliseconds.count() * 1000);
    return 0;
}
