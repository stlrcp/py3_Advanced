#include <iostream>
#include <iomanip>    // setw(6) 方法的头文件
#include <vector>
using namespace std;

void show(vector<vector<float>> matrix, int M, int N){
    for (int i = 0; i < M; i++){
        for (int j = 0; j < N; j++){
            cout << setw(6) << matrix[i][j];
        }
        cout << endl;
    }
}

vector<vector<float>> tranpose1(vector<vector<float>> matrix){
    int row = matrix.size();
    int col = matrix[0].size();
    vector<vector<float>> res_mat(col, vector<float>(row));
    for (int i = 0; i < col; i++)
    {
        for (int j = 0; j < row; j++){
            cout << setw(6) << matrix[j][i];
            res_mat[i][j] = matrix[j][i];
        }
        cout << endl;
    }
    return res_mat;
}

int main(){
    int M = 8;
    int N = 6;
    // vector<vector<float>> matrix(M,vector<float>(N));   // vector 二维数组的初始化
    vector<vector<float>> matrix(M,vector<float>(N, 1));  // vector 二维数组初始化并赋值
    show(matrix, M, N);
    for (int i = 0; i < M; i++)
    {
        for (int j = 0; j < N; j++)
            matrix[i][j] = (i*N+j) * 0.01;
    }
    show(matrix, M, N);
    vector<vector<float>> res_mat(N, vector<float>(M));
    res_mat = tranpose1(matrix);
    cout << "=====================" << endl;
    show(res_mat, N, N);
    return 0;
}
