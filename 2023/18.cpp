#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using intt = unsigned long;
using Coord = std::pair<intt, intt>;

struct Instruction
{
    char dir;
    intt len;
    std::string color;
    Coord pos;
};

void advance_position(Coord &c, char dir, intt len)
{
    auto &[i, j] = c;
    switch (dir)
    {
    case 'R':
        j = j + len;
        break;
    case 'L':
        j = j - len;
        break;
    case 'U':
        i = i - len;
        break;
    case 'D':
        i = i + len;
        break;
    default:
        throw std::runtime_error("Invalid direction");
    }
}

std::istream &operator>>(std::istream &is, std::vector<Instruction> &v)
{
    Coord pos{0, 0};
    while (!is.eof() && !is.bad())
    {
        Instruction i;
        is >> i.dir >> i.len >> i.color;
        i.pos = pos;
        v.push_back(i);
        advance_position(pos, i.dir, i.len);
    }
    if (pos != Coord{0, 0})
        throw std::runtime_error("Expected closed loop in input!");
    return is;
}

// Based on https://nils-olovsson.se/articles/area_of_the_polygon_and_greens_theorem/
intt area_polygon(const std::vector<Instruction> &v)
{
    intt area = 0;
    const size_t N = v.size();
    if (N <= 2)
        return area;

    for (size_t i = 0; i < v.size(); i++)
    {
        const Coord &p0 = v[i].pos;
        const Coord &p1 = v[(i + 1) % N].pos;
        area += p1.first * p0.second - p0.first * p1.second;
    }
    return area / 2;
}

intt perimeter_polygon(const std::vector<Instruction> &v)
{
    intt per = 0;
    for (const auto i : v)
        per += i.len;
    return per;
}

// use Pick's theorem to get the number of interior points, given area and boundary points (perimeter)
// https://en.wikipedia.org/wiki/Pick%27s_theorem
intt volume_polygon(const std::vector<Instruction> &v)
{
    intt area = area_polygon(v);
    intt boundary = perimeter_polygon(v);

    // Pick's formula
    intt interior = area + 1 - boundary / 2;

    // volume is the number of interior points plus the number of points on the boundary
    return interior + boundary;
}

void fix_instructions(std::vector<Instruction> &v)
{
    Coord pos{0, 0};
    for (Instruction &ins : v)
    {
        std::string code = ins.color;
        code.pop_back();
        char dir = code.back();
        code.pop_back();
        switch (dir)
        {
        case '0':
            ins.dir = 'R';
            break;
        case '1':
            ins.dir = 'D';
            break;
        case '2':
            ins.dir = 'L';
            break;
        case '3':
            ins.dir = 'U';
            break;
        default:
            throw std::runtime_error("Invalid code!");
        }
        code.erase(0, 2);
        ins.len = std::stoul(code, nullptr, 16);
        ins.pos = pos;
        advance_position(pos, ins.dir, ins.len);
    }
}

int main()
{
    std::ifstream is("inputs/18.txt");
    std::vector<Instruction> vi;
    is >> vi;

    std::cout << volume_polygon(vi) << std::endl;
    fix_instructions(vi);
    std::cout << volume_polygon(vi) << std::endl;
    return 0;
}