
# build libtest.a
#INCLUDE_DIR="mylib-v1 mylib-v2"
LIBS_DIR="-L. -Lmylib-v2 -Lmylib-v1"

## mylib
g++ -c mylib-v1/mylib.cpp -o mylib-v1/mylib.o
ar rcs  mylib-v1/libmylib.v1.a mylib-v1/mylib.o # V1
g++ -c mylib-v2/mylib.cpp -o mylib-v2/mylib.o
ar rcs  mylib-v2/libmylib.v2.a mylib-v2/mylib.o # V2

## test
g++ -c test.cpp -o test.o
ar x mylib-v1/libmylib.v1.a
ar rcs  libtest.a test.o mylib.o
# ar rcs  libtest.a test.o mylib-v1/mylib.o

# build main exe
g++ -o main  $LIBS_DIR main.cpp -ltest -lmylib.v2

# rm test.o libtest.a mylib-v1/lib* mylib-v2/lib*