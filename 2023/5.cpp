#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <list>
#include <tuple>
#include <algorithm>
#include <limits>
#include <iterator>

using intType = unsigned long long;
using interval = std::tuple<intType, intType>;

class Mapping
{
    private:
        std::vector<std::tuple<intType, intType, intType>> intervals;

    public:
        intType operator ()(intType i) const{
            for (const auto& [source, source_max, dest]: intervals)
            {
                if (i >= source)
                {
                    if (i< source_max)
                        return dest + i - source;
                }
                else
                    break;
            }
            return i;
        }

        // break input intervals to match mapping intervals
        // note: both start and end of the interval are inclusive
        std::list<interval> break_intervals(const std::list<interval>& ints) const
        {
           std::list<interval> broken;
            for (auto [start, end]: ints)
            {
                bool pushed = false;
                for (const auto& [source, source_max, dest]: intervals)
                {
                    if ((start < source && end < source) || (start >= source && end < source_max))
                    {
                        broken.push_back(std::make_tuple(start, end));
                        pushed = true;
                        break;
                    }
                    else if (start < source && end >= source && end < source_max)
                    {
                        broken.push_back(std::make_tuple(start, source-1));
                        broken.push_back(std::make_tuple(source, end));
                        pushed = true;
                        break;
                    }
                    else if (start < source && end > source_max)
                    {
                        broken.push_back(std::make_tuple(start, source-1));
                        broken.push_back(std::make_tuple(source, source_max-1));
                        start = source_max;
                    }
                    else if (start >= source && start < source_max && end >= source_max)
                    {
                        broken.push_back(std::make_tuple(start, source_max-1));
                        start = source_max;
                    }
                }
                if (!pushed)
                    broken.push_back(std::make_tuple(start, end));
            }
            return std::move(broken);
        }

        std::list<interval> operator ()(const std::list<interval>& ints) const
        {
            // map broken intervals
            std::list<interval> mapped;
            for (auto [start, end]: break_intervals(ints))
                mapped.push_back(std::make_tuple((*this)(start), (*this)(end)));
            return std::move(mapped);
        }

        void add_interval(intType source, intType dest, intType range)
        {
            intervals.push_back(std::make_tuple(source, source+range, dest));
            std::sort(intervals.begin(), intervals.end(), [&](auto a, auto b){return std::get<0>(a) < std::get<0>(b); });
        }
};

std::istream& operator>>(std::istream& is, Mapping& m)
{
    is.ignore(1000, '\n');
    intType dest, source, range;
    while (!is.eof() && is.peek() != '\n')
    {
        is >> dest >> source >> range;
        is.ignore(1, '\n');
        m.add_interval(source, dest, range);
    }
    is.ignore(1, '\n');
    return is;
}

void load_input(std::istream& is, std::list<Mapping>& maps, std::list<intType>& seeds)
{
    // get seeds
    is.ignore(100, ':');
    intType seed;
    while (is.peek() != '\n')
    {
        is >> seed;
        seeds.push_back(seed);
    }
    is.ignore(1, '\n');
    is.ignore(1, '\n');

    // get mappings
    while (!is.eof())
    {
        maps.push_back(Mapping());
        is >> maps.back();
    }
}

intType closest_location(const std::list<Mapping>& maps, const std::list<intType>& seeds)
{
    intType res = std::numeric_limits<intType>::max();
    for (intType seed: seeds)
    {
        for (const auto& map: maps)
            seed = map(seed);
        res = std::min(res, seed);
    }
    return res;
}

intType closest_location_2(const std::list<Mapping>& maps, const std::list<intType>& seeds)
{
    intType res = std::numeric_limits<intType>::max();
    auto it_seed = seeds.begin();
    auto it_range = std::next(it_seed, 1);
    for(;it_range != seeds.end() && it_seed != seeds.end(); std::advance(it_seed, 2), std::advance(it_range, 2))
    {
        std::list<interval> input_intervals;
        std::list<interval> output_intervals;
        input_intervals.push_back(std::make_tuple(*it_seed, (*it_seed) + (*it_range) - 1));
        for (const auto& map: maps)
        {
            output_intervals = map(input_intervals);
            input_intervals = output_intervals;
        }
        interval min_interval = *std::min_element(output_intervals.begin(), output_intervals.end(), [&](auto a, auto b){return std::get<0>(a) < std::get<0>(b);});
        res = std::min(res, std::get<0>(min_interval));
    }
    return res;
}


int main()
{
    std::ifstream file("inputs/5.txt");
    std::list<intType> seeds;
    std::list<Mapping> maps;
    load_input(file, maps, seeds);

    intType closest = closest_location(maps, seeds);
    std::cout << closest << std::endl;

    closest = closest_location_2(maps, seeds);
    std::cout << closest << std::endl;
    return 0;
}