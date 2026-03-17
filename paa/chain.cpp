#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;
typedef long long ll;

vector<ll> lookupTable = {1, 7, 23, 63, 159, 383, 895, 2047, 4607, 10239, 22527, 49151, 106495, 229375, 491519, 1048575, 2228223, 4718591, 9961471, 20971519, 44040191, 92274687, 192937983, 402653183, 838860799, 1744830463, 3623878655, 7516192767, 15569256447, 32212254719, 67108863, 134217727, 268435455, 536870911, 1073741823, 2147483647, 4294967295};

// void precompute() {
//     for (ll k = 0; k <= 40; ++k) {
//         ll max_n = (k + 1) * (1LL << (k + 1)) - 1;
//         cout<<max_n<<", ";
//         lookupTable.push_back(max_n);
//         if (max_n > 2e10) break; 
//     }
// }

void solve() {
    ll n;
    if (!(cin >> n)) return;
    auto it = lower_bound(lookupTable.begin(), lookupTable.end(), n);
    cout << distance(lookupTable.begin(), it) << endl;
}

int main() {
    // precompute();

    int t;
    if (!(cin >> t)) return 0;
    
    while (t--) {
        solve();
    }

    return 0;
}