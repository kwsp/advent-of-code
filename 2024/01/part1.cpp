#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);

  int left, right;
  vector<int> lefts, rights;

  std::string line;
  while (getline(cin, line)) {
    istringstream ss(line);
    ss >> left >> right;
    lefts.push_back(left);
    rights.push_back(right);
  }

  sort(lefts.begin(), lefts.end(), std::less());
  sort(rights.begin(), rights.end(), std::less());

  int dist{};
  for (int i = 0; i < lefts.size(); ++i) {
    int d = std::abs(lefts[i] - rights[i]);
    dist += d;
  }
  cout << dist;
}
