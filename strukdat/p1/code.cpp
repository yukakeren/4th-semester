#include <bits/stdc++.h>
using namespace std;

int main() {
    
    int n;
    cin >> n;

    priority_queue<int> pq;
    int mood = 0;

    while(n--){
        string s;
        int st;
        cin >> s;
        if(s == "PLAN"){
            cin >> st;
            pq.push(st);
        }
        else if(s == "GO_OUT"){
            if(pq.empty()){
                cout << "No one is going out" << endl;
            }
            else{
                cout << pq.top() + mood << endl;
                pq.pop();
                mood = 0;
            }
        }
        else if(s == "MOOD"){
            cin >> st;
            mood = st;
        }
    }
    return 0;
}