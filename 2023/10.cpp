#include <string>
#include <vector>
#include <list>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <unordered_set>

class Coordinate
{
public:
    int u, v;
    Coordinate(int u_, int v_) : u(u_), v(v_){};
    Coordinate(const Coordinate &other) : u(other.u), v(other.v){};

    Coordinate operator+(const Coordinate &other) const
    {
        return Coordinate(u + other.u, v + other.v);
    }

    Coordinate operator-(const Coordinate &other) const
    {
        return Coordinate(u - other.u, v - other.v);
    }

    Coordinate &operator+=(const Coordinate &other)
    {
        u += other.u;
        v += other.v;
        return *this;
    }

    std::vector<Coordinate> neighbours() const
    {
        std::vector<Coordinate> n(4, *this);
        n[0].u++;
        n[1].u--;
        n[2].v++;
        n[3].v--;
        return n;
    }

    bool operator==(const Coordinate &other) const
    {
        return (u == other.u && v == other.v);
    }

    bool operator!=(const Coordinate &other) const
    {
        return !operator==(other);
    }
};

// Hash function/class for Coordinate
template <>
struct std::hash<Coordinate>
{
    // Compute individual hash values for u, v then combine them using XOR and bit shifting
    std::size_t operator()(const Coordinate &k) const
    {
        return (std::hash<int>()(k.u) >> 1) ^ (std::hash<int>()(k.u) << 1);
    }
};

class Map
{
public:
    std::vector<std::string> map;

    Coordinate find_start() const
    {
        for (int v = 0; v < map.size(); v++)
            for (int u = 0; u < map[v].size(); u++)
                if (map[v][u] == 'S')
                    return Coordinate(u, v);

        throw std::runtime_error("Could not find start");
    }

    char operator[](const Coordinate &c) const
    {
        if (c.u >= 0 && c.u < map[0].size() && c.v >= 0 && c.v < map.size())
            return map[c.v][c.u];
        return '\0';
    }

    Coordinate next(Coordinate &cur, Coordinate &dir) const
    {
        switch ((*this)[cur])
        {
        case '|':
            if (dir.u == 0)
                return cur + dir;
            break;
        case '-':
            if (dir.v == 0)
                return cur + dir;
            break;
        case 'L':
            if (dir == Coordinate(0, 1))
                return cur + Coordinate(1, 0);
            else if (dir == Coordinate(-1, 0))
                return cur + Coordinate(0, -1);
            break;
        case 'J':
            if (dir == Coordinate(1, 0))
                return cur + Coordinate(0, -1);
            else if (dir == Coordinate(0, 1))
                return cur + Coordinate(-1, 0);
            break;
        case '7':
            if (dir == Coordinate(1, 0))
                return cur + Coordinate(0, 1);
            else if (dir == Coordinate(0, -1))
                return cur + Coordinate(-1, 0);
            break;
        case 'F':
            if (dir == Coordinate(-1, 0))
                return cur + Coordinate(0, 1);
            else if (dir == Coordinate(0, -1))
                return cur + Coordinate(1, 0);
            break;
        default:
            break;
        }
        throw std::runtime_error("Not a valid move");
    }

    std::list<Coordinate> find_loop() const
    {
        std::list<Coordinate> loop;

        // add start of the loop
        loop.push_back(find_start());

        // add first valid pipe after start
        for (auto &neigh : loop.back().neighbours())
        {
            try
            {
                Coordinate dir = neigh - loop.back();

                // next line will throw error if invalid
                next(neigh, dir);

                // add neigh to the loop (if previous didn't throw error)
                loop.push_back(neigh);
                break;
            }
            catch (std::exception &e)
            {
                continue;
            }
        }

        if (loop.size() != 2)
            throw std::runtime_error("Could not find loop");

        // keep walking until get back to start
        while (loop.back() != loop.front())
        {
            Coordinate dir = loop.back() - *std::prev(loop.end(), 2);
            loop.push_back(next(loop.back(), dir));
        }

        // drop last position (it's already in the list)
        loop.pop_back();

        return loop;
    }

    // point is inside loop if number of crossings of a line towards infinity is odd
    // use diagonal line to avoid colinear line with loop
    bool is_inside_loop(const std::unordered_set<Coordinate> &loop, const Coordinate &c) const
    {
        // if c is part of the boundary it is not IN the loop
        if (loop.contains(c))
            return false;

        int crossings = 0;
        Coordinate cur(c);
        while ((*this)[cur] != '\0')
        {
            if (loop.contains(cur) && (*this)[cur] != '7' && (*this)[cur] != 'L')
                crossings++;
            cur += Coordinate(1, 1);
        }
        return crossings % 2 == 1;
    }

    int count_tiles_within_loop(const std::list<Coordinate> &loop_) const
    {
        int area = 0;
        std::list<Coordinate> queue(loop_);
        std::unordered_set<Coordinate> loop{loop_.begin(), loop_.end()};
        std::unordered_set<Coordinate> visited;
        while (!queue.empty())
        {
            auto current = queue.front();
            queue.pop_front();

            // check we have not visited this already
            if (visited.contains(current))
                continue;
            visited.insert(current);

            // add neighbours that are within boundary and have not yet been visited
            for (auto &neigh : current.neighbours())
                if ((*this)[neigh] != '\0' && !visited.contains(neigh))
                    queue.push_back(neigh);

            if (is_inside_loop(loop, current))
                area++;
        }
        return area;
    }
};

std::istream &operator>>(std::istream &is, Map &map)
{
    std::string line;
    while (std::getline(is, line))
        map.map.push_back(line);
    return is;
}

int main()
{
    std::ifstream is("inputs/10.txt");
    Map map;
    is >> map;

    std::list<Coordinate> loop = map.find_loop();
    std::cout << (loop.size() / 2) << std::endl;
    std::cout << map.count_tiles_within_loop(loop) << std::endl;
    return 0;
}