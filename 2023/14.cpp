#include <iostream>
#include <fstream>
#include <list>
#include <vector>
#include <unordered_map>
#include <utility>
#include <algorithm>
#include <functional>

using Coord = std::pair<int, int>;

struct Map
{
    std::list<Coord> round_rocks, squared_rocks;
    Coord bounds;

    int total_load() const
    {
        int cmax = bounds.first;
        int sum = 0;
        for (const auto& [row, col]: round_rocks)
            sum += (cmax - row) + 1;
        return sum;
    }

    std::unordered_map<int, std::list<int>> get_fixed_rocks_row_by_col() const
    {
        std::unordered_map<int, std::list<int>> rocks;
        for (const auto& [row, col] : squared_rocks)
        {
            if (!rocks.contains(col))
                rocks[col] = std::list<int>{-1}; // we have an imaginary fixed rock at the top
            rocks[col].push_back(row);
        }

        // sort each list by row in descending order
        for (auto& [col, list_row]: rocks)
            list_row.sort(std::greater<>());

        // also adds imaginary top for round_rocks (in case col doesn't exist already)
        for (const auto& [row, col] : round_rocks)
            if (!rocks.contains(col))
                rocks[col] = std::list<int>{-1};

        return rocks;
    }

    void tilt_north()
    {
        // sort round rocks by row so we don't overrun ourselves
        round_rocks.sort([&](Coord& c0, Coord& c1){return c0.first < c1.first;});

        // Get all fixed rocks per column
        auto fixed_rocks_by_col = get_fixed_rocks_row_by_col();

        for(auto& [row, col]: round_rocks)
        {
            auto& fixed_in_row = fixed_rocks_by_col[col];
            auto it = fixed_in_row.begin();
            while (it!= fixed_in_row.end() && row < *it)
                ++it;
            int &fixed_row = *it;
            row = ++fixed_row;
        }
    }

    void transform_rocks(std::function<void(Coord&)> trans_fn)
    {
        std::for_each(round_rocks.begin(), round_rocks.end(), trans_fn);
        std::for_each(squared_rocks.begin(), squared_rocks.end(), trans_fn);
    }

    void tilt_cycle()
    {
        Coord cmax(bounds);
        auto rot90ccwdeg = [&](Coord& c){std::swap(c.first, c.second); c.second = cmax.first - c.second;};
        for (int i=0; i<4; i++)
        {
            tilt_north();
            transform_rocks(rot90ccwdeg);
        }
    }
};

std::istream& operator>>(std::istream& is, Map& map)
{
    char c;
    int i=0, j=0;
    while (!is.eof() && !is.bad())
    {
        is.get(c);
        switch (c)
        {
        case '#':
            map.squared_rocks.push_back(std::make_pair(i, j++));
            break;
        case 'O':
            map.round_rocks.push_back(std::make_pair(i, j++));
            break;
        case '\n':
            i++;
            j=0;
            break;
        case '.':
            j++;
            break;
        default:
            throw std::runtime_error("Unexpected condition");
            break;
        }
    }
    map.bounds = std::make_pair(i, j-2);
    return is;
}

int periodic_result(Map& m, long iter)
{
    // skip any transient state before periodic behaviour
    constexpr int burn = 200;
    for (int i=0; i< burn; i++)
        m.tilt_cycle();

    // fills a vector with values
    constexpr int max_size = 600;
    std::vector<int> v(max_size);
    for (auto it = v.begin(); it!=v.end(); ++it)
    {
        *it = m.total_load();
        m.tilt_cycle();
    }
        
    // tries to identify the period
    bool valid_period = false;
    constexpr int max_period_mul = 30;
    int T;
    for (T=1; T<max_size && !valid_period; T++)
    {
        valid_period = true;
        for (int period_multiple=1; period_multiple<max_period_mul && valid_period; period_multiple++)
            for(int i=0; i<T && valid_period && i+period_multiple*T < max_size; i++)
                if (v[i] != v[i+period_multiple*T])
                    valid_period = false;
    }

    if (!valid_period)
        throw std::runtime_error("Could not identify periodic behaviour!");

    // uses the periodic behavior to get the answer
    return v[(iter - burn) % T];
}


int main()
{
    Map map_original;
    std::ifstream is("inputs/14.txt");
    is >> map_original;
    Map map1(map_original), map2(map_original);

    map1.tilt_north();
    std::cout << map1.total_load() << std::endl;

    std::cout << periodic_result(map2, 1000000000) << std::endl;
    return 0;
}