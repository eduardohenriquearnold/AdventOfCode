#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <cmath>

std::istream &operator>>(std::istream &is, std::vector<int> &v)
{
    is.ignore(80, ':');

    std::string line;
    std::getline(is, line);

    std::stringstream ss(line);
    for (int t; ss >> t;)
        v.push_back(t);
    return is;
}

long long concatenate_numbers(const std::vector<int> &v)
{
    std::stringstream ss;
    for (int n : v)
        ss << n;
    long long conc;
    ss >> conc;
    return conc;
}

int count_possible_wins(int T, int D)
{
    int count = 0;
    for (int t = 1; t < T; t++)
        if (t * (T - t) > D)
            count++;
    return count;
}

template <typename intt>
int smart_count_possible_wins(intt T_, intt D_)
{
    double T = static_cast<double>(T_), D = static_cast<double>(D_);
    double root0 = 0.5 * (T - std::sqrt(T * T - 4. * D));
    double root1 = 0.5 * (T + std::sqrt(T * T - 4. * D));

    int minv = int(std::ceil(root0));
    int maxv = int(std::floor(root1));

    return maxv - minv + 1;
}

int count_all_ways(const std::vector<int> &time, const std::vector<int> &distance)
{
    int res = 1;
    for (auto it_t = time.begin(), it_d = distance.begin(); it_t != time.end() && it_d != distance.end(); it_t++, it_d++)
        res *= smart_count_possible_wins(*it_t, *it_d);
    return res;
}

int main()
{
    std::vector<int> time, distance;
    std::ifstream is("inputs/6.txt");
    is >> time >> distance;

    int count_ways = count_all_ways(time, distance);
    std::cout << count_ways << std::endl;

    count_ways = smart_count_possible_wins(concatenate_numbers(time), concatenate_numbers(distance));
    std::cout << count_ways << std::endl;
    return 0;
}