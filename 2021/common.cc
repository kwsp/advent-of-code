#include <bits/stdc++.h>
using namespace std;

bool isdigit(string s) {
  return count_if(s.begin(), s.end(),
                  [](unsigned char c) { return std::isalnum(c); }) > 0;
}
