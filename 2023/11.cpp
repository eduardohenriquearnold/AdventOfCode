#include <iostream>
#include <fstream>
#include <sstream>
#include <list>
#include <vector>
#include <string>
#include <utility>
#include <algorithm>
#include <cmath>

using intt = long long;
using Coord = std::pair<intt, intt>;

std::istream &operator>>(std::istream &is, std::list<Coord> &l)
{
    std::string line;
    intt i = 0;
    while (std::getline(is, line))
    {
        intt j = 0;
        for (char &c : line)
        {
            if (c == '#')
                l.push_back(std::make_pair(i, j));
            j++;
        }
        i++;
    }
    return is;
}

template <bool dim_x>
size_t bound(const std::list<Coord> &l)
{
    constexpr size_t dim = dim_x ? 1 : 0;
    auto it = std::max_element(l.begin(), l.end(), [&](auto v0, auto v1)
                               { return std::get<dim>(v0) < std::get<dim>(v1); });
    return std::get<dim>(*it);
}

template <bool dim_x>
void expand_galaxies(std::list<Coord> &l, intt expansion_rate = 2)
{
    expansion_rate--;
    size_t max_size = bound<dim_x>(l) + 1;
    constexpr size_t dim = dim_x ? 1 : 0;

    // cum-sum of empty rows up to n-th row
    std::vector<intt> cum_empty(max_size);
    for (size_t i = 0; i < max_size; i++)
    {
        bool empty = !std::any_of(l.begin(), l.end(), [&](Coord c)
                                  { return std::get<dim>(c) == i; });
        if (i == 0)
            cum_empty[i] = expansion_rate * intt(empty);
        else
            cum_empty[i] = cum_empty[i - 1] + expansion_rate * intt(empty);
    }
    for (Coord &c : l)
        std::get<dim>(c) += cum_empty[std::get<dim>(c)];
}

// Distance between galaxies in Manhattan grid
intt distance(const Coord &g0, const Coord &g1)
{
    return std::abs(g0.first - g1.first) + std::abs(g0.second - g1.second);
}

intt sum_distances(const std::list<Coord> &l)
{
    intt sum = 0;
    for (auto it0 = l.begin(); it0 != l.end(); it0++)
        for (auto it1 = std::next(it0); it1 != l.end(); it1++)
            sum += distance(*it0, *it1);
    return sum;
}

int main()
{
    std::list<Coord> galaxies;
    std::ifstream is("inputs/11.txt");
    is >> galaxies;

    std::list<Coord> galaxies0(galaxies);
    expand_galaxies<false>(galaxies0);
    expand_galaxies<true>(galaxies0);
    std::cout << sum_distances(galaxies0) << std::endl;

    std::list<Coord> galaxies1(galaxies);
    expand_galaxies<false>(galaxies1, 1000000);
    expand_galaxies<true>(galaxies1, 1000000);
    std::cout << sum_distances(galaxies1) << std::endl;
    return 0;
}