#include <array>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);

  int left, right;
  vector<int> lefts;
  array<int, 1000000> count{};

  string line;
  while (getline(cin, line)) {
    istringstream ss(line);
    ss >> left >> right;
    lefts.push_back(left);
    count[right]++;
  }

  cout << reduce(lefts.begin(), lefts.end(), 0,
                 [&](int acc, int val) { return acc + val * count[val]; });
}
