#include <iostream>
#include <fstream>
#include <vector>
#include <deque>
#include <sstream>
#include <execution>
#include <numeric>
#include <algorithm>

std::istream &operator>>(std::istream &is, std::vector<std::vector<int>> &v)
{
    std::string line;
    int num;
    while (!is.eof() && !is.fail())
    {
        std::getline(is, line);
        std::stringstream ss(line);
        v.push_back(std::vector<int>());
        while (ss >> num)
            v.back().push_back(num);
    }
    return is;
}

int extrapolate(const std::vector<int> &v)
{
    std::vector<int> diff(v.size() - 1);
    for (int i = 0; i < diff.size(); i++)
        diff[i] = v[i + 1] - v[i];

    if (std::all_of(std::next(diff.begin()), diff.end(), [&](auto i)
                    { return i == diff[0]; }))
        return v.back() + diff[0];
    else
        return v.back() + extrapolate(diff);
}

int sum_extrapolated(const std::vector<std::vector<int>> &history)
{
    int sum = 0;
    for (const auto &v : history)
        sum += extrapolate(v);
    return sum;
}

int main()
{
    std::ifstream is("inputs/9.txt");
    std::vector<std::vector<int>> history;
    is >> history;

    std::cout << sum_extrapolated(history) << std::endl;

    for (auto &v : history)
        std::reverse(v.begin(), v.end());

    std::cout << sum_extrapolated(history) << std::endl;

    return 0;
}