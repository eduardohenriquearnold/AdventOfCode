#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <list>
#include <map>

using game_set = std::map<std::string, int>;

std::istream& operator>>(std::istream& is, std::list<std::list<game_set>>& record)
{
    while (!is.eof())
    {
        is.ignore(20, ':');
        record.push_back(std::list<game_set>());
        record.back().push_back(game_set());

        while (is.peek() != '\n' && !is.eof())
        {
            int count;
            std::string item;
            bool new_set = false;
            is >> count >> item;

            if (item.back() == ',')
                item.pop_back();
            else if (item.back() == ';')
            {
                item.pop_back();
                new_set = true;
            }
            record.back().back()[item] = count;

            if (new_set)
                record.back().push_back(game_set());
        }
    }
    return is;
}

int get_valid_ids_sum(const std::list<std::list<game_set>>& record)
{
    const game_set max{{"red", 12}, {"green", 13}, {"blue", 14}};

    int sum = 0;
    int id = 0;
    for (const std::list<game_set>& sets: record)
    {
        id++;
        bool invalid = false;
        for (const game_set& set: sets)
            for (auto& item: set)
                if (item.second > max.at(item.first))
                    invalid = true;

        if (!invalid)
            sum += id;
    }
    return sum;
}

int power_minset_cubes(const std::list<std::list<game_set>>& record)
{
    int sum = 0;
    for (const std::list<game_set>& sets: record)
    {
        game_set minset{{"red", 0}, {"green", 0}, {"blue", 0}};
        for (const game_set& set: sets)
            for (auto& item: set)
                minset[item.first] = std::max(minset[item.first], item.second);
        sum += minset["red"] * minset["green"] * minset["blue"];
    }
    return sum;
}

int main()
{
    std::list<std::list<game_set>> record;
    std::ifstream is("inputs/2.txt");
    is >> record;

    int valid_sum = get_valid_ids_sum(record);
    int power_sum = power_minset_cubes(record);
    std::cout << valid_sum << std::endl << power_sum << std::endl;
    return 0;
}