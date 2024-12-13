#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <string_view>
using namespace std;

bool isNum(char c) { return c >= '0' && c <= '9'; }

struct Parser {
  string_view src;
  size_t i{0};
  size_t N{0};

  bool matchKeyword(const string_view keyword) {
    if (src.substr(i, keyword.size()) == keyword) {
      i += keyword.size();
      return true;
    }
    return false;
  }

  int parse1() {
    i = 0;
    int v1{}, v2{};
    int result{};
    while (i < N) {
      switch (peek()) {
      case 'm': {
        if (matchKeyword("mul(") && parseParams(v1, v2)) {
          result += v1 * v2;
        } else {
          i++;
        }
      } break;
      default:
        i++;
      }
    }
    return result;
  }

  int parse2() {
    i = 0;
    int v1{}, v2{};
    int result{};
    bool enabled = true;
    while (i < N) {
      switch (peek()) {
      case 'm': {
        if (matchKeyword("mul(") && parseParams(v1, v2)) {
          if (enabled) {
            result += v1 * v2;
          }
        } else {
          i++;
        }
      } break;
      case 'd': {
        if (matchKeyword("do()")) {
          enabled = true;
        } else if (matchKeyword("don't()")) {
          enabled = false;
        } else {
          i++;
        }
      } break;
      default:
        i++;
      }
    }
    return result;
  }

private:
  char peek() { return src[i]; }

  bool parseInt(int &val) {
    const int iStart = i;
    if (!isNum(src[iStart])) {
      return false;
    }

    for (; i < N; ++i) {
      if (!isNum(src[i])) {
        auto sub = src.substr(iStart, i - iStart);
        val = stoi(string{sub});
        return true;
      }
    }

    return false;
  }

  bool parseParams(int &v1, int &v2) {
    if (!parseInt(v1)) {
      goto parseParamsFailed;
    }

    if (peek() != ',') {
      goto parseParamsFailed;
    }
    i++;

    if (!parseInt(v2)) {
      goto parseParamsFailed;
    }

    if (peek() != ')') {
      goto parseParamsFailed;
    }
    i++;

    return true;

  parseParamsFailed:
    v1 = 0;
    v2 = 0;
    return false;
  }
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ifstream ifile("input.txt");

  ostringstream ss;
  ss << ifile.rdbuf();
  const auto s = ss.str();

  int part1{}, part2{};
  int v1{}, v2{};

  Parser parser{s, 0, s.size()};
  part1 = parser.parse1();
  part2 = parser.parse2();

  cout << "Part 1: " << part1 << '\n';
  cout << "Part 2: " << part2 << '\n';
}
