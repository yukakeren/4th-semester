#include <bits/stdc++.h>
using namespace std;

#define ll long long
#define md 1000000007

int main(){
    ll t;
    cin >> t;
    while(t--){
        ll n;
        cin >> n;
        
        ll sum = 3*((n*(n+1)/2)-n);

        cout << sum%md << endl;
    }

    return 0;
}

