#include <iostream>
#include <fstream>
#include <vector>
#include <queue>
#include <unordered_set>

using vec2i = std::vector<std::vector<int>>;
using Coord = std::pair<int, int>;

struct State
{
    Coord pos;
    char dir;
    int count;
    int cost;
};

template <>
struct std::equal_to<State>
{
    bool operator()(const State &s1, const State &s2) const { return s1.pos == s2.pos && s1.dir == s2.dir && s1.count == s2.count; }
};

template <>
struct std::greater<State>
{
    bool operator()(const State &s1, const State &s2) const { return s1.cost > s2.cost; }
};

template <>
struct std::hash<State>
{
    size_t operator()(const State &s) const { return size_t(s.pos.first << 16) + size_t(s.pos.second) + size_t(s.dir); }
};

std::istream &operator>>(std::istream &is, vec2i &map)
{
    map.push_back(vec2i::value_type());
    char c;
    while (is.get(c))
    {
        if (c == '\n')
            map.push_back(vec2i::value_type());
        else
            map.back().push_back(c - '0');
    }
    return is;
}

std::pair<char, char> turn_directions(char c)
{
    if (c == '>' || c == '<')
        return {'v', '^'};
    else if (c == '^' || c == 'v')
        return {'<', '>'};
    else
        throw std::runtime_error("Unexpected input direction");
}

Coord next_position(const Coord &current, const char direction)
{
    int i = current.first, j = current.second;
    switch (direction)
    {
    case '>':
        j++;
        break;
    case '<':
        j--;
        break;
    case '^':
        i--;
        break;
    case 'v':
        i++;
        break;
    default:
        throw std::runtime_error("Invalid direction");
        break;
    }
    return {i, j};
}

// Dijkstra with conditional neighbours
// priority queue keeps the State with lowest cost on top
int min_cost_path(const vec2i &cost)
{
    const int H = cost.size(), W = cost.front().size();

    std::priority_queue<State, std::vector<State>, std::greater<State>> queue;
    std::unordered_set<State> visited;
    queue.push({{0, 0}, '>', 0});
    queue.push({{0, 0}, 'v', 0});

    while (!queue.empty())
    {
        State s = queue.top();
        const auto &[pos, dir, count, acc_cost] = s;
        queue.pop();

        if (pos.first < 0 || pos.first >= H || pos.second < 0 || pos.second >= W || visited.contains(s))
            continue;

        visited.insert(s);

        const int next_cost = acc_cost + cost[pos.first][pos.second];
        const auto &[dir_left, dir_right] = turn_directions(dir);
        queue.push({next_position(pos, dir_left), dir_left, 1, next_cost});
        queue.push({next_position(pos, dir_right), dir_right, 1, next_cost});
        if (count < 3)
            queue.push({next_position(pos, dir), dir, count + 1, next_cost});

        if (pos.first == H - 1 && pos.second == W - 1)
            return next_cost - cost[0][0];
    }

    throw std::runtime_error("Could not reach target location");
}

int min_cost_path_2(const vec2i &cost)
{
    const int H = cost.size(), W = cost.front().size();

    std::priority_queue<State, std::vector<State>, std::greater<State>> queue;
    std::unordered_set<State> visited;
    queue.push({{0, 0}, '>', 0});
    queue.push({{0, 0}, 'v', 0});

    while (!queue.empty())
    {
        State s = queue.top();
        const auto &[pos, dir, count, acc_cost] = s;
        queue.pop();

        if (pos.first < 0 || pos.first >= H || pos.second < 0 || pos.second >= W || visited.contains(s))
            continue;

        visited.insert(s);

        const int next_cost = acc_cost + cost[pos.first][pos.second];
        if (count < 10)
            queue.push({next_position(pos, dir), dir, count + 1, next_cost});
        if (count >= 4)
        {
            const auto &[dir_left, dir_right] = turn_directions(dir);
            queue.push({next_position(pos, dir_left), dir_left, 1, next_cost});
            queue.push({next_position(pos, dir_right), dir_right, 1, next_cost});
        }

        if (pos.first == H - 1 && pos.second == W - 1 && count >= 4)
            return next_cost - cost[0][0];
    }

    throw std::runtime_error("Could not reach target location");
}

int main()
{
    vec2i cost;
    std::ifstream is("inputs/17.txt");
    is >> cost;

    std::cout << min_cost_path(cost) << std::endl;
    std::cout << min_cost_path_2(cost) << std::endl;
    return 0;
}