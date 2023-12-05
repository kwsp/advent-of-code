#include <bits/stdc++.h>
#include <vector>
using namespace std;
typedef long long ll;

vector<int> getInput(const string fname = "day07.txt") {
  ifstream fs(fname);
  string tmp;
  vector<int> v;
  while (getline(fs, tmp, ','))
    v.push_back(stoi(tmp));
  return v;
}

tuple<int, int> getLeastFuelPos(const vector<int> &inp) {
  int min_cost = 99999999, min_pos = 0;
  for (int pos = 0; pos < inp.size(); pos++) {
    int cost = 0;
    for (int i = 0; i < inp.size(); ++i) {
      cost += abs(inp[i] - pos);
    }
    if (min_cost > cost) {
      min_cost = cost;
      min_pos = pos;
    }
  }
  return {min_pos, min_cost};
}

tuple<ll, ll> getLeastFuelPos2(const std::vector<int> &inp) {
  ll min_cost = 999999999999, min_pos = 0;

  auto getCost = [](int i, int j) {
    int steps = abs(i - j);
    return (long long)(((double)(steps + 1)) / 2 * steps);
  };

  for (int pos = 0; pos < inp.size(); pos++) {
    ll cost = 0;
    for (int i = 0; i < inp.size(); ++i) {
      cost += getCost(inp[i], pos);
    }
    if (min_cost > cost) {
      min_cost = cost;
      min_pos = pos;
    }
  }
  return {min_pos, min_cost};
}

void part2(const vector<int> &inp) {
  auto res = getLeastFuelPos2(inp);
  cout << "Part 2: " << get<1>(res) << endl;
}

void part1(const vector<int> &inp) {
  auto res = getLeastFuelPos(inp);
  cout << "Part 1: " << get<1>(res) << endl;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);
  auto inp = getInput();
  part1(inp);
  part2(inp);
}
