#include <iostream>
#include <sstream>
#include <string>
#include <vector>

using namespace std; // NOLINT

// Function to check if a vector is safe according to the rules
bool isSafe(const std::vector<int> &levels) {
  bool increasing = true;
  bool decreasing = true;
  for (size_t i = 1; i < levels.size(); ++i) {
    int diff = levels[i] - levels[i - 1];
    if (std::abs(diff) < 1 || std::abs(diff) > 3) {
      return false; // Difference is not between 1 and 3
    }
    if (diff < 0) {
      increasing = false; // Not strictly increasing
    }
    if (diff > 0) {
      decreasing = false; // Not strictly decreasing
    }
  }
  return increasing || decreasing; // Either all increasing or all decreasing
}

// check if a vector can be made safe by removing one element
bool isSafeWithRemoval(const std::vector<int> &levels) {
  for (size_t i = 0; i < levels.size(); ++i) {
    std::vector<int> modifiedLevels = levels;
    modifiedLevels.erase(modifiedLevels.begin() + i);
    if (isSafe(modifiedLevels)) {
      return true;
    }
  }
  return false;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int nsafeP1 = 0;
  int nsafeP2 = 0;
  std::string line;
  while (getline(cin, line)) {
    istringstream ss(line);
    std::vector<int> vec;
    int v = 0;
    while (ss >> v) {
      vec.push_back(v);
    }

    if (isSafe(vec)) {
      nsafeP1++;
    }

    if (isSafeWithRemoval(vec)) {
      nsafeP2++;
    }
  }

  cout << "Part 1: " << nsafeP1 << "\n";
  cout << "Part 2: " << nsafeP2 << "\n";
}
