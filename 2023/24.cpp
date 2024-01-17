#include <iostream>
#include <fstream>
#include <vector>
#include <cassert>

using intt = long;

struct Line
{
    intt x, y, z, vx, vy, vz;
    double tmin, tmax;
    static intt min_interval, max_interval;

    // disregard Z
    bool intersect(const Line &other) const
    {
        intt det = vy * other.vx - vx * other.vy;
        if (det == 0)
            return false;
        intt delta_x = other.x - x;
        intt delta_y = other.y - y;
        double t0 = double(other.vx * delta_y - other.vy * delta_x) / det;
        double t1 = double(vx * delta_y - vy * delta_x) / det;
        return (t0 > tmin && t0 < tmax) && (t1 > other.tmin && t1 < other.tmax);
    }

    Line(std::istream &is)
    {
        std::string garbage;
        is >> x >> garbage >> y >> garbage >> z >> garbage >> vx >> garbage >> vy >> garbage >> vz;

        // compute minimum and maximum values of t such that ray is within box intervals
        double tx1 = double(min_interval - x) / vx;
        double tx2 = double(max_interval - x) / vx;
        tmin = std::min(tx1, tx2);
        tmax = std::max(tx1, tx2);
        double ty1 = double(min_interval - y) / vy;
        double ty2 = double(max_interval - y) / vy;
        tmin = std::max(tmin, std::min(ty1, ty2));
        tmax = std::min(tmax, std::max(ty1, ty2));

        // cannot be in the past
        tmin = std::max(0., tmin);
        tmax = std::max(0., tmax);
    }
};

std::ostream &operator<<(std::ostream &os, const Line &l)
{
    return os << l.x << ", " << l.y << ", " << l.z << " @ " << l.vx << ", " << l.vy << ", " << l.vz;
}

intt Line::min_interval = 200000000000000;
intt Line::max_interval = 400000000000000;

int count_intersections(const std::vector<Line> &lines)
{
    int count = 0;
    for (auto it0 = lines.begin(); it0 != lines.end(); it0++)
        for (auto it1 = std::next(it0); it1 != lines.end(); it1++)
            if (it0->intersect(*it1))
                count++;

    return count;
}

int main()
{
    std::ifstream is("inputs/24.txt");
    std::vector<Line> lines;
    while (!is.eof())
        lines.push_back(Line(is));

    std::cout << count_intersections(lines) << std::endl;
    return 0;
}
