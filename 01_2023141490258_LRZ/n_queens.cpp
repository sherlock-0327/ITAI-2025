#include<cstdio>
#include<cmath>
int location[21];
int number;
int count = 0;
using namespace std;

bool is_safe(int x,int y);
int print();

void n_queens(int now,int all){
    for(int y=1;y<=all;y++){
        if(now>all){
            print();
            break;
        }
        if(is_safe(now,y)){
            location[now]=y;
            n_queens(now+1,number);
        }
    }
}

bool is_safe(int x,int y){
    int i=1;
    for(i;i<=x-1;i++){
        if(y == location[i] || abs(x - i) == abs(y - location[i]))return 0;
    }
    return 1;
}

int print(){
    for(int i=1;i<=number;i++){
        for(int j=1;j<=number;j++){
            if(location[i]!=j){
                putchar('o');
            }else{
                putchar('x');
            }
        }
        putchar('\n');
    }
    count++;
    putchar('\n');
    return 0;
}

int main(){
    scanf("%d",&number);
    if(number<4||number>20){
        printf("Invaild input.\n");
        return -1;
    }
    n_queens(1,number);
    printf("Total solutions: %d\n", count);
    return 0;
}