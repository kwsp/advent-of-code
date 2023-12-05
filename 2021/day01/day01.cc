// https://adventofcode.com/2021/day/1
#include <bits/stdc++.h>
using namespace std;

template <class T> vector<T> readFileItems(string fname) {
  ifstream fs(fname);
  T tmp;
  vector<T> v;
  while (fs >> tmp)
    v.push_back(tmp);
  return v;
}

template <class T> int countInc(vector<T> vec) {
  if (vec.size() < 2)
    return 0;
  int prev = vec[0];
  int acc = 0;
  for (int i = 1; i < vec.size(); i++) {
    acc += vec[i] > prev;
    prev = vec[i];
  }
  return acc;
}

int part1() {
  const auto inp = readFileItems<int>("day01.txt");
  return countInc(inp);
}

int part2() {
  const auto inp = readFileItems<int>("day01.txt");
  vector<int> wind(inp.size() - 2);
  for (int i = 0; i < inp.size() - 2; i++)
    wind[i] = inp[i] + inp[i + 1] + inp[i + 2];
  return countInc(wind);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);
  cout << part1() << endl;
  cout << part2() << endl;
}
