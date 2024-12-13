#include <csignal>
#include <iostream>
#include <string>
#include <vector>

class NullStream : public std::ostream {
public:
  NullStream() : std::ostream(nullptr) {}
  template <typename T> NullStream &operator<<(const T &) { return *this; }
};

#define DEBUG 0

#if DEBUG
#define dout std::cout
#else
static NullStream nullStream_; // Don't use me directly
#define dout nullStream_
#endif

using namespace std;

int countForward(string_view line, string_view word) {
  int count = {};
  size_t i = 0;
  while (i < line.size()) {
    const auto pos = line.substr(i).find(word);
    if (pos != line.npos) {
      count++;
      i += pos + word.size();
    } else {
      break;
    }
  }
  return count;
}

int countForwardAndReverse(string line, string_view word) {
  int count = countForward(line, word);
  reverse(line.begin(), line.end());
  count += countForward(line, word);
  return count;
}

int countHorizontal(const vector<string> &lines, const string_view word) {
  int count = 0;
  for (const auto &line : lines) {
    count += countForwardAndReverse(line, word);
  }
  return count;
}

int countVertical(const vector<string> &lines, const string_view word) {
  int width = lines[0].size();
  int height = lines.size();
  if (height < word.size()) {
    return 0;
  }
  int count = 0;
  string curr;
  curr.resize(height);

  for (int j = 0; j < width; ++j) {
    for (int i = 0; i < height; ++i) {
      curr[i] = lines[i][j];
    }

    count += countForwardAndReverse(curr, word);
  }

  return count;
}

int countDiagonal(const vector<string> &lines, const string_view word) {
  const int width = lines[0].size();
  const int height = lines.size();
  if (height < word.size()) {
    return 0;
  }

  int count = 0;
  string curr;
  curr.resize(min(width, height));

  // Top right to bottom left
  {
    dout << "--- Top right to bottom left (horizontal left to right)---\n";
    int jStart = 0;
    for (int iStart = word.size() - 1; iStart < width; ++iStart) {
      int currSize = 0;
      for (int i = iStart, j = jStart; i >= 0 && j < height; --i, ++j) {
        curr[currSize++] = lines[j][i];
      }
      const auto sub = curr.substr(0, currSize);
      const auto subcount = countForwardAndReverse(sub, word);
      count += subcount;
      dout << "jStart " << jStart << " iStart " << iStart << " " << sub
           << "\tsubcount " << subcount << "\n";
    }

    dout << "--- Top right to bottom left (vertical top down)---\n";
    int iStart = width - 1;
    jStart = 1;
    for (; jStart <= height - word.size(); ++jStart) {
      int currSize = 0;
      for (int i = iStart, j = jStart; i >= 0 && j < height; --i, ++j) {
        curr[currSize++] = lines[j][i];
      }
      const auto sub = curr.substr(0, currSize);
      const auto subcount =
          countForwardAndReverse(curr.substr(0, currSize), word);
      count += subcount;
      dout << "jStart " << jStart << " iStart " << iStart << " " << sub
           << "\tsubcount " << subcount << "\n";
    }
  }

  // Top left to bottom right
  {
    dout << "--- Top left to bottom right (horizontal left to right)---\n";
    int jStart = 0;
    for (int iStart = 0; iStart <= width - word.size(); ++iStart) {
      int currSize = 0;
      for (int i = iStart, j = jStart; i < width && j < height; ++i, ++j) {
        curr[currSize++] = lines[j][i];
      }
      const auto sub = curr.substr(0, currSize);
      const auto subcount = countForwardAndReverse(sub, word);
      count += subcount;
      dout << "jStart " << jStart << " iStart " << iStart << " " << sub
           << "\tsubcount " << subcount << "\n";
    }

    dout << "--- Top left to bottom right (vertical down)---\n";
    int iStart = 0;
    jStart = 1;
    for (; jStart <= height - word.size(); ++jStart) {
      int currSize = 0;
      for (int i = iStart, j = jStart; i < width && j < height; ++i, ++j) {
        curr[currSize++] = lines[j][i];
      }
      const auto sub = curr.substr(0, currSize);
      const auto subcount =
          countForwardAndReverse(curr.substr(0, currSize), word);
      count += subcount;
      dout << "jStart " << jStart << " iStart " << iStart << " " << sub
           << "\tsubcount " << subcount << "\n";
    }
  }

  return count;
}

bool checkCorners(char c1, char c2, char c3, char c4) {
  return c1 == 'M' && c2 == 'M' && c3 == 'S' && c4 == 'S';
}

int x_mas(vector<string> lines) {
  const auto width = lines[0].size();
  const auto height = lines.size();
  int count = 0;

  for (size_t j = 1; j < height - 1; ++j) {
    for (size_t i = 1; i < width - 1; ++i) {
      /*
       * A valid X-MAS has A at the center and M M S S at the 4 corners
       */
      char center = lines[j][i];
      if (center == 'A') {
        char tl = lines[j - 1][i - 1];
        char tr = lines[j - 1][i + 1];
        char bl = lines[j + 1][i - 1];
        char br = lines[j + 1][i + 1];

        if (checkCorners(tl, tr, br, bl) || checkCorners(bl, tl, tr, br) ||
            checkCorners(br, bl, tl, tr) || checkCorners(tr, br, bl, tl)) {
          ++count;
        }
      }
    }
  }

  return count;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  vector<string> lines;
  string line;
  while (getline(cin, line)) {
    lines.push_back(line);
  }

  const string word = "XMAS";
  int hor = countHorizontal(lines, word);
  int vert = countVertical(lines, word);
  int diag = countDiagonal(lines, word);

  dout << "hor " << hor << " vert " << vert << " diag " << diag << '\n';
  cout << "Part 1: " << hor + vert + diag << '\n';

  cout << "Part 2: " << x_mas(lines) << '\n';
}
