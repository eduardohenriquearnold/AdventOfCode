#include <iostream>
#include <fstream>
#include <vector>

// Requires installing libeigen3-dev
// and compiling with flag -I/usr/include/eigen3
#include <Eigen/Core>
#include <Eigen/Dense>

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

Eigen::Matrix3d cross_matrix(Eigen::Vector3d v)
{
    Eigen::Matrix3d result;
    result << 0, -v[2], v[1],
        v[2], 0, -v[0],
        -v[1], v[0], 0;
    return result;
}

// had to resort to Eigen and online wisdom
intt armageddon_rock(const std::vector<Line> &lines)
{
    // let p0, v0 be the R^3 position and velocity of the rock, and pi, vi the equivalent for i-th hailstone
    // then p0 + ti * v0 = pi + ti * vi
    // =>  p0 - pi = ti * (vi - v0), ti \in Z+
    // =>  (p0 - pi) is parallel to (vi - v0) ==> (p0 - pi) x (vi - v0) = 0
    // replacing the non-linear p0*v0 terms for different i's
    // we get p0 x (v1 - v2) + v0 x (p1 - p2) = p1 x v1 - p2 x v2
    // this above equation gives 3 lines in the system Ax = b, where x = [x, y, z, vx, vy, vz] of the stone
    Eigen::MatrixXd A(6, 6);
    Eigen::VectorXd b(6);
    auto Vec3p = [](const Line &l)
    { return Eigen::Vector3d(l.x, l.y, l.z); };
    auto Vec3v = [](const Line &l)
    { return Eigen::Vector3d(l.vx, l.vy, l.vz); };

    b.segment<3>(0) = -Vec3p(lines[0]).cross(Vec3v(lines[0])) + Vec3p(lines[1]).cross(Vec3v(lines[1]));
    b.segment<3>(3) = -Vec3p(lines[0]).cross(Vec3v(lines[0])) + Vec3p(lines[2]).cross(Vec3v(lines[2]));
    A.block<3, 3>(0, 0) = cross_matrix(Vec3v(lines[0])) - cross_matrix(Vec3v(lines[1]));
    A.block<3, 3>(3, 0) = cross_matrix(Vec3v(lines[0])) - cross_matrix(Vec3v(lines[2]));
    A.block<3, 3>(0, 3) = -cross_matrix(Vec3p(lines[0])) + cross_matrix(Vec3p(lines[1]));
    A.block<3, 3>(3, 3) = -cross_matrix(Vec3p(lines[0])) + cross_matrix(Vec3p(lines[2]));
    Eigen::VectorXd result = A.inverse() * b;
    std::cout << result << std::endl;
    intt sum = 0;
    for (int i = 0; i < 3; i++)
        sum += intt(result[i]);
    return sum;
}

int main()
{
    std::ifstream is("inputs/24.txt");
    std::vector<Line> lines;
    while (!is.eof())
        lines.push_back(Line(is));

    std::cout << count_intersections(lines) << std::endl;
    std::cout << armageddon_rock(lines) << std::endl;
    return 0;
}
