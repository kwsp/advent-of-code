#include <array>
#include <exception>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_set>
#include <vector>

typedef std::array<int, 3> Vertex;
typedef std::vector<Vertex> Inp;

std::ostream &operator<<(std::ostream &s, const Vertex &a) {
  s << "(" << a[0] << ", " << a[1] << ", " << a[2] << ")";
  return s;
}

auto parse_inp() {
  std::ifstream fs("day18.txt");
  std::string line, tok;
  Inp inp;

  auto next_int = [&tok](std::stringstream &ss) {
    std::getline(ss, tok, ',');
    return std::stoi(tok);
  };

  while (std::getline(fs, line)) {
    std::stringstream ss(line);
    std::array<int, 3> curr;

    curr[0] = next_int(ss);
    curr[1] = next_int(ss);
    curr[2] = next_int(ss);

    inp.push_back(curr);
  }
  return inp;
}

enum BlockType { air, lava, airpocket };

template <class T> struct Vec3d {
  size_t _x, _y, _z;
  std::vector<T> data;

  // Constructor
  Vec3d(size_t x, size_t y, size_t z, T val = 0)
      : _x(x), _y(y), _z(z), data(x * y * z, val) {}

  // Default Copy constructor
  bool _bound_check(size_t x, size_t y, size_t z) const {
    return x < _x && x >= 0 && y < _y && y >= 0 && z < _z && z >= 0;
  }

  // Element access
  T &operator()(size_t x, size_t y, size_t z) {
    if (!_bound_check(x, y, z))
      throw std::out_of_range("Out of bounds");
    return data[x * _y * _z + y * _z + z];
  }
  T operator()(size_t x, size_t y, size_t z) const {
    if (!_bound_check(x, y, z))
      throw std::out_of_range("Out of bounds");
    return data[x * _y * _z + y * _z + z];
  }
  T &operator()(const Vertex &v) { return (*this)(v[0], v[1], v[2]); }
  T operator()(const Vertex &v) const { return (*this)(v[0], v[1], v[2]); }

  auto get_neighbours(const Vertex &_v) const {
    if (!_bound_check(_v[0], _v[1], _v[2]))
      throw std::out_of_range("Out of bounds");

    std::vector<Vertex> res;
    res.reserve(6);
    Vertex v(_v);
    v[0] += 1;
    if (v[0] < _x)
      res.push_back(v);
    v[0] -= 2;
    if (v[0] >= 0)
      res.push_back(v);
    v[0] += 1;

    v[1] += 1;
    if (v[1] < _y)
      res.push_back(v);
    v[1] -= 2;
    if (v[1] >= 0)
      res.push_back(v);
    v[1] += 1;

    v[2] += 1;
    if (v[2] < _z)
      res.push_back(v);
    v[2] -= 2;
    if (v[2] >= 0)
      res.push_back(v);

    return res;
  }
};

inline int dist(const Vertex &v1, const Vertex &v2) {
  return std::abs(v1[0] - v2[0]) + std::abs(v1[1] - v2[1]) +
         std::abs(v1[2] - v2[2]);
}

auto part1naive(const Inp &inp) {
  int faces = inp.size() * 6;
  for (int i = 0; i < inp.size(); i++) {
    for (int j = i + 1; j < inp.size(); j++) {
      if (dist(inp[i], inp[j]) == 1) {
        faces -= 2;
      }
    }
  }
  return faces;
}

auto make_grid(const Inp &inp) {
  int x = 0, y = 0, z = 0;
  for (const auto &v : inp) {
    x = std::max(x, v[0]);
    y = std::max(y, v[1]);
    z = std::max(z, v[2]);
  }

  // Set all vertex that have a cube present to 1
  Vec3d<BlockType> g(x + 1, y + 1, z + 1, air);
  for (const auto &v : inp)
    g(v) = lava;

  return g;
}

bool is_pocket(Vec3d<BlockType> &g, const Vertex &v) {
  // do DFS connect component analysis to make sure its lava in all directions
  if (g(v) == air) {
    g(v) = airpocket;

    const auto nbs = g.get_neighbours(v);

    // if size is not 6, reached edge without finding lava. not pocket
    if (nbs.size() != 6)
      return false;

    for (const auto nb : nbs)
      if (!is_pocket(g, nb))
        return false;
  }
  return true;
}

auto part(const Inp &inp) {
  auto g = make_grid(inp);

  int faces1 = inp.size() * 6;
  for (const auto &v : inp) {
    // For every node, check its 6 neighbours
    for (const auto nb : g.get_neighbours(v)) {

      if (g(nb) == lava) {
        // If a neighbour is lava, decrease faces by 1
        faces1 -= 1;

      } else if (g(nb) == air) {
        auto _g = g; // copy construct grid

        if (is_pocket(_g, nb)) {
          // else if its unchecked air, check if its an air pocket
          // verified air pockets are marked as 2
          // if the pocket is found, assign _g as g
          g = std::move(_g); // move assignment
        }
      }
    }
  }

  // Count faces lost due to pockets
  int faces2 = faces1;
  for (const auto &v : inp) {
    for (const auto nb : g.get_neighbours(v)) {
      if (g(nb) == airpocket)
        faces2--;
    }
  }

  std::cout << "Part 1: " << faces1 << "\n";
  std::cout << "Part 2: " << faces2 << "\n";
}

int main() {
  // Read inp
  const auto inp = parse_inp();

  part(inp);
  return 0;
}
