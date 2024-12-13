#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

bool checkUpdate(const vector<int> &update,
                 const vector<pair<int, int>> &rules) {
  for (const auto &rule : rules) {
    auto it1 = find(update.begin(), update.end(), rule.first);
    auto it2 = find(update.begin(), update.end(), rule.second);
    if (it1 == update.end() || it2 == update.end()) {
      continue;
    }
    if (it1 > it2) {
      return false;
    }
  }
  return true;
}

int middle(vector<int> update) { return update[update.size() / 2]; }

int checkUpdate2(vector<int> &update, const vector<pair<int, int>> &rules) {
  bool anyInvalid = false;
  bool needFix = true;
  while (needFix) {
    needFix = false;
    for (const auto &rule : rules) {
      auto it1 = find(update.begin(), update.end(), rule.first);
      auto it2 = find(update.begin(), update.end(), rule.second);
      if (it1 == update.end() || it2 == update.end()) {
        continue;
      }
      if (it1 > it2) {
        anyInvalid = true;
        needFix = true;
        iter_swap(it1, it2);
      }
    }
  }
  return anyInvalid ? middle(update) : 0;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  vector<pair<int, int>> rules;

  string line;
  // Parse rules
  while (getline(cin, line)) {
    if (line.size() != 5)
      break;
    int v1 = stoi(line.substr(0, 2));
    int v2 = stoi(line.substr(3, 2));
    rules.emplace_back(v1, v2);
  }

  int part1 = 0;
  int part2 = 0;

  // Parse updates
  while (getline(cin, line)) {
    istringstream ss(line);
    string val;
    vector<int> update;
    while (getline(ss, val, ',')) {
      update.push_back(stoi(val));
    }

    if (checkUpdate(update, rules)) {
      part1 += middle(update);
    }

    part2 += checkUpdate2(update, rules);
  }

  cout << "Part 1: " << part1 << '\n';
  cout << "Part 2: " << part2 << '\n';
}
