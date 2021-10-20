#include <bits/stdc++.h.>

using namespace std;


typedef vector<int> vi;


#define PB push_back


// functions:
void displayVector(vi vct);
vi encodeSignal(int decodedHex);
void convertToBinary(string &res, int num);



int main()
{
    freopen("input.txt", "r", stdin);
    freopen("output.txt", "w", stdout);

    int cur_number;
    while(cin >> cur_number) {  // something like: 4081
        //printf("%d as hex:", cur_number);
        //cout << hex << cur_number;
        //printf("\n");

        vi encoded_signal = encodeSignal(cur_number);
        displayVector(encoded_signal);
    }

    return 0;
}



vi encodeSignal(int number) {
    int frequency = 38000;
    double pulses = 1000000 / frequency;


    string binaryValueString = "";
    convertToBinary(binaryValueString, number);

    //cout << binaryValueString;

    vi encodedSignal;
    /*encodedSignal.PB(24 * pulses);  // 0 notify it is a learned IR code
    encodedSignal.PB(24 * pulses);*/
    for(int i = 0; i < binaryValueString.size(); ++i) {
        if(binaryValueString[i] == '1') {  // set the ON code
            encodedSignal.PB(48 * pulses);
        } else {
            encodedSignal.PB(24 * pulses);
        }
        encodedSignal.PB(24 * pulses);  // OFF
    }

    return encodedSignal;
}

void displayVector(vi vct) {
    printf("{");
    for(int i = 0, n = vct.size(); i < n - 1; i++) {
        printf("%d, ", vct[i]);
    }
    printf("%d},\n", vct[vct.size() - 1]);
}


void convertToBinary(string &res, int num) {
    if(num / 2 != 0) {
        convertToBinary(res, num / 2);
    }
    res += to_string(num % 2);
}
