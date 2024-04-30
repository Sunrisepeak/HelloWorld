#include <iostream>

class Matrix {

public:
    const int * operator[](int index) const {
        return mData_e + (index * mCol);
    }

    int * operator[](int index) {
        //...
        return mData_e + (index * mCol);
    } 

    bool empty() const {
        return mData_e == nullptr;
    }

    void reshape(int r, int c, int val = 0) {
        //...
        if (mData_e != nullptr) delete [] mData_e;
        mRow = r; mCol = c;
        mData_e = new int [mRow * mCol];
        for (int i = 0; i < mRow * mCol; i++) {
            mData_e[i] = val;
        }
    }

    int mRow, mCol;

private:
    int *mData_e;

    void copy_data_e(int *data1, int *data2) {
        std::cout << "~1ms" << std::endl;
        for (int i = 0; i < mRow * mCol; i++) {
            data1[i] = data2[i];
        }
    }

public:
    Matrix() : mRow { 0 }, mCol { 0 } {
        mData_e = nullptr;
    }

    ~Matrix() {
        if (mData_e) delete [] mData_e;
        mData_e = nullptr;
    }

    Matrix(const Matrix &m) : mRow { m.mRow }, mCol { m.mCol } {
        std::cout << "Matrix(const Matrix &m)" << std::endl;
        this->mData_e = new int[mRow * mCol];
        copy_data_e(this->mData_e, m.mData_e);
    }

    Matrix & operator=(const Matrix &m) {
        std::cout << "Matrix & operator=(const Matrix &m)" << std::endl;
        if (this != &m) {
            if (mData_e != nullptr) delete [] mData_e;
            mRow = m.mRow; mCol = m.mCol;
            mData_e = new int[mRow * mCol];
            copy_data_e(mData_e, m.mData_e);
        }
        return *this;
    }

    Matrix(Matrix &&m) = delete;
    Matrix & operator=(Matrix &&m) = delete;
};

void print_matrix(const Matrix &m, const char *msg = "M") {
    std::cout << msg << " <" << m.mRow << "x" << m.mCol << ">:" << std::endl;
    for (int r = 0; r < m.mRow; r++) {
        std::cout << "\t[ ";
        for (int c = 0; c < m.mCol; c++) {
            std::cout << m[r][c] << " ";
        }
        std::cout << "]" << std::endl;
    }
}

// g++ cpp/move_sem/main.cpp && ./a.out

int main() {
    Matrix m1, m2;

    m1.reshape(3, 4, 2);
    m2.reshape(3, 4);
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 4; j++) {
            m2[i][j] = i * 4 + j;
        }
    }

    print_matrix(m1, "m1");
    print_matrix(m2, "m2");

// copy
    Matrix m3 = m1;
    print_matrix(m3, "m3");
    m3 = m2;
    print_matrix(m3, "m1");

/* move
    Matrix m4 = std::move(m1);
    print_matrix(m4, "m4");
    m4 = std::move(m2);
    print_matrix(m4, "m4");
*/

    return 0;
}