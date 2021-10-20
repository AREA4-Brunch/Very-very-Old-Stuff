#include <bits/stdc++.h>

using namespace std;

int main()
{
    freopen("input_int.txt", "r", stdin);
    freopen("output_hex.txt", "w", stdout);

    long long cur_num;
    while (cin >> cur_num) {
        cout << "0x";
        cout << hex << cur_num << "\n";
    }

    return 0;
}