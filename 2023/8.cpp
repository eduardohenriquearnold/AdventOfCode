#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <regex>
#include <numeric>

using map_graph = std::map<std::string, std::pair<std::string, std::string>>;

void load_data(std::istream &is, std::string &sequence, map_graph &map)
{
    std::getline(is, sequence);
    is.ignore();

    // R"~()~" removes the need to escape characters
    const std::regex rgx{R"~((\w+) = \((\w+), (\w+)\))~"};
    std::smatch m;
    std::string node;
    while (!is.eof() && !is.fail())
    {
        std::getline(is, node);
        if (!std::regex_match(node, m, rgx))
            throw std::runtime_error("Regex matching failed");
        map[m[1]] = std::make_pair(m[2], m[3]);
    }
}

int count_steps_to_end(const std::string &seq, const map_graph &map)
{
    std::string node("AAA");
    int count = 0;
    while (node != "ZZZ")
    {
        if (seq[count % seq.length()] == 'L')
            node = map.at(node).first;
        else
            node = map.at(node).second;
        count++;
    }
    return count;
}

// Finds the period (iterations required to go from ending Z to ending Z)
int find_period(const std::string &seq, const map_graph &map, const std::string &seed)
{
    std::string node(seed);
    int count = 0, prev_count = 0, period = -1;

    while (period < count - prev_count)
    {
        period = count - prev_count;
        prev_count = count;
        while (node.back() != 'Z')
            if (seq[(count++) % seq.length()] == 'L')
                node = map.at(node).first;
            else
                node = map.at(node).second;
    }

    return period;
}

int count_ghost_steps_to_end(const std::string &seq, const map_graph &map)
{
    std::vector<std::string> nodes;
    for (auto &[name, val] : map)
        if (name.back() == 'A')
            nodes.push_back(name);

    int count = 0;
    while (std::any_of(nodes.begin(), nodes.end(), [&](auto s)
                       { return s.back() != 'Z'; }))
    {
        bool left = seq[count % seq.length()] == 'L';
        for (auto &node : nodes)
            if (left)
                node = map.at(node).first;
            else
                node = map.at(node).second;
        count++;
    }
    return count;
}

// Be smart: use individual periods instead of brute-force
unsigned long smart_count_ghost_steps_to_end(const std::string &seq, const map_graph &map)
{
    unsigned long res = 1;
    for (auto &[name, val] : map)
        if (name.back() == 'A')
            res = std::lcm(res, static_cast<unsigned long>(find_period(seq, map, name)));
    return res;
}

int main()
{
    std::ifstream is("inputs/8.txt");
    std::string seq;
    map_graph map;
    load_data(is, seq, map);

    std::cout << count_steps_to_end(seq, map) << std::endl;
    std::cout << smart_count_ghost_steps_to_end(seq, map) << std::endl;
    return 0;
}