int a = 3;
int b = 4;

int main() {
    int ret = 0;
    if (a) {
        int a = 0;
        ret = 4;
    }

    return ret + b;
}