#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <tuple>
#include <vector>

struct Move {
  int n, from, to;
};

struct Input {
  std::vector<std::string> stacks;
  std::vector<Move> moves;

  Input(std::string fname) {
    std::ifstream fs(fname);
    std::string curr;
    assert(fs.is_open());

    std::vector<std::string> _stacks;
    while (std::getline(fs, curr) && curr.size() != 0)
      _stacks.push_back(curr);

    std::string tok;
    int n, from, to;
    while (std::getline(fs, curr)) {
      std::istringstream ss(curr);
      ss >> tok >> tok;
      n = std::stoi(tok);
      ss >> tok >> tok;
      from = std::stoi(tok) - 1;
      ss >> tok >> tok;
      to = std::stoi(tok) - 1;
      moves.push_back({n, from, to});
    }

    // Parse initial stack
    const auto nums = _stacks.back();
    for (int i = 0; i < nums.size(); i++) {
      if (nums[i] == ' ')
        continue;

      std::string stack;
      for (int j = _stacks.size() - 2; j >= 0; j--) {
        if (_stacks[j][i] != ' ')
          stack.push_back(_stacks[j][i]);
      }

      stacks.push_back(stack);
    }
  }
};

std::string get_res(const std::vector<std::string> &stacks) {
  return std::accumulate(stacks.cbegin(), stacks.cend(), std::string{},
                         [](std::string s, const auto &stack) -> std::string {
                           s.push_back(stack.back());
                           return s;
                         });
};

int main(int argc, char *argv[]) {
  {
    // Part 1
    Input input("./day05.txt");
    auto stacks = input.stacks;
    auto moves = input.moves;

    for (const auto &move : input.moves) {
      auto &from = stacks[move.from];
      auto &to = stacks[move.to];
      int n = move.n;
      assert(from.size() >= n);
      while (n--) {
        to.push_back(from.back());
        from.pop_back();
      }
    }
    std::cout << "Part 1: " << get_res(stacks) << "\n";
  }

  {
    // Part 2
    Input input("./day05.txt");
    auto stacks = input.stacks;
    auto moves = input.moves;

    for (const auto &move : input.moves) {
      auto &from = stacks[move.from];
      auto &to = stacks[move.to];
      int n = move.n;
      assert(from.size() >= n);
      to += from.substr(from.size() - n, n);
      from = from.substr(0, from.size() - n);
    }
    std::cout << "Part 2: " << get_res(stacks) << "\n";
  }
  return 0;
}
