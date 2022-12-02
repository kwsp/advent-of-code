#include <bits/stdc++.h>
using namespace std;

vector<int> readInput(const string &fname) {
  ifstream fs(fname);
  string tmp;
  vector<int> v;
  while (getline(fs, tmp, ',')) {
    v.push_back(stoi(tmp));
  }
  return v;
}

long long calc(const vector<int> &inp, int days) {
  typedef unordered_map<int, long long> fish_t;
  fish_t fish;
  for (int i = 0; i <= 8; i++) {
    fish[i] = count(inp.begin(), inp.end(), i);
  }

  while (days--) {
    const auto f0 = fish[0];
    for (int i = 0; i <= 7; i++)
      fish[i] = fish[i + 1];
    fish[8] = f0;
    fish[6] += f0;
  }

  long long tot = accumulate(
      fish.begin(), fish.end(), 0ll,
      [](long long sum, fish_t::value_type p) { return sum + p.second; });

  return tot;
}

void part2() {
  auto inp = readInput("day06.txt");
  cout << "Part 2: " << calc(inp, 256) << endl;
}

void part1() {
  auto inp = readInput("day06.txt");
  cout << "Part 1: " << calc(inp, 80) << endl;
}

int main() {
  part1();
  part2();
}
