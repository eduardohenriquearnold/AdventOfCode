#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <unordered_set>

struct Pos
{
    int u, v;

    bool operator==(const Pos &other) const
    {
        return (u == other.u) && (v == other.v);
    }
};

template <>
struct std::hash<Pos>
{
    size_t operator()(const Pos &s) const
    {
        return ((s.u + 1) << 16) + ((s.v + 1) << 8);
    }
};

struct DP
{
    std::vector<std::string> map;

    Pos initial_pos() const
    {
        for (int u = 0; u < map.size(); u++)
            for (int v = 0; v < map[0].size(); v++)
                if (map[u][v] == 'S')
                    return {u, v};

        throw std::runtime_error("Could not find starting position");
    }

    int reach_count(int steps)
    {
        std::unordered_set<Pos> queue;
        std::unordered_set<Pos> next_queue;
        queue.insert(initial_pos());

        for (; steps >= 0; steps--)
        {
            for (const Pos &pos : queue)
            {
                int u = pos.u % map.size();
                int v = pos.v % map[0].size();
                if (u < 0)
                    u += map.size();
                if (v < 0)
                    v += map[0].size();
                char c = map[u][v];

                if (c == '.' || c == 'S')
                {
                    if (steps > 0)
                    {
                        next_queue.insert({pos.u + 1, pos.v});
                        next_queue.insert({pos.u - 1, pos.v});
                        next_queue.insert({pos.u, pos.v + 1});
                        next_queue.insert({pos.u, pos.v - 1});
                    }
                    else
                        next_queue.insert({pos.u, pos.v});
                }
            }
            queue.clear();
            next_queue.swap(queue);
        }
        return queue.size();
    }
};

std::istream &operator>>(std::istream &is, DP &dp)
{
    std::string line;
    while (!is.eof() && !is.bad())
    {
        std::getline(is, line);
        dp.map.push_back(line);
    }
    return is;
}

int main()
{
    std::ifstream is("inputs/21.txt");
    DP dp;
    is >> dp;

    std::cout << dp.reach_count(6) << std::endl;
    std::cout << dp.reach_count(10) << std::endl;
    std::cout << dp.reach_count(500) << std::endl;
    return 0;
}