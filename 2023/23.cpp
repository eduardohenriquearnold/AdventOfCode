#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_map>
#include <list>
#include <set>
#include <stack>

using Pos = std::pair<int, int>;
using Graph = std::unordered_map<size_t, std::unordered_map<size_t, int>>;

template <>
struct std::hash<Pos>
{
    size_t operator()(const Pos &p) const
    {
        return size_t(p.first) << 8 + size_t(p.second);
    }
};

struct DP
{
    std::vector<std::string> map;
    Pos start, end;
    Graph graph;
    size_t start_idx, end_idx;

    DP(std::istream &is)
    {
        // Ingest map from input stream
        std::string line;
        while (!is.eof() && !is.bad())
        {
            std::getline(is, line);
            map.push_back(line);
        }

        // Find start and end positions
        for (int v = 0; v < map.front().size(); v++)
        {
            if (map.front()[v] == '.')
                start = {0, v};
            if (map.back()[v] == '.')
                end = {int(map.size() - 1), v};
        }
    }

    void create_graph(bool ignore_slopes = false)
    {
        graph.clear();

        size_t total_nodes = 0;
        std::unordered_map<Pos, size_t> nodes;
        std::list<std::tuple<int, int, char>> queue;

        queue.push_front({start.first, start.second, 'v'});
        nodes[start] = total_nodes++;
        graph[nodes[start]] = {};

        auto in_bounds = [&](Pos p)
        { return (p.first >= 0) && (p.first < map.size()) && (p.second >= 0) && (p.second < map.front().size()); };
        auto next_pos = [&](Pos p, char dir)
        {
            switch (dir)
            {
            case 'v':
                return std::make_pair(p.first + 1, p.second);
            case '^':
                return std::make_pair(p.first - 1, p.second);
            case '>':
                return std::make_pair(p.first, p.second + 1);
            case '<':
                return std::make_pair(p.first, p.second - 1);
            default:
                throw std::runtime_error("Invalid character");
            }
        };
        auto ortho_dir = [](char dir)
        {
            switch (dir)
            {
            case 'v':
            case '^':
                return std::make_pair('<', '>');
            case '<':
            case '>':
                return std::make_pair('^', 'v');
            default:
                throw std::runtime_error("Invalid character");
            }
        };

        // Updates state (u, v, dir). dir becomes \0 if the next position is an intersection and \e if dead-end
        auto get_next_state = [&](int &u, int &v, char &dir)
        {
            Pos cur{u, v}, next;
            auto [dir1, dir2] = ortho_dir(dir);
            bool found = false;
            for (char dir_ : {dir, dir1, dir2})
            {
                next = next_pos(cur, dir_);
                if (in_bounds(next) && !(map[next.first][next.second] == '#'))
                {
                    found = true;
                    cur = next;
                    dir = dir_;
                    u = cur.first;
                    v = cur.second;
                    break;
                }
            }
            if (!found)
            {
                dir = '\e';
                return;
            }
            int next_possibilities = 0;
            for (char dir_ : {'>', '<', '^', 'v'})
            {
                next = next_pos(cur, dir_);
                if (in_bounds(next) && !(map[next.first][next.second] == '#'))
                    next_possibilities++;
            }
            if (next_possibilities > 2 || (!ignore_slopes && map[cur.first][cur.second] != '.'))
                dir = '\0';
            else if (next_possibilities <= 1)
                dir = '\e';
        };

        while (!queue.empty())
        {
            auto [u_start, v_start, dir] = queue.front();
            queue.pop_front();

            // travels until next node and count distance
            int distance{0}, u{u_start}, v{v_start};
            for (; dir != '\0' && dir != '\e'; distance++)
                get_next_state(u, v, dir);

            if (dir == '\e' && (u != end.first && v != end.second))
                continue;

            // update graph and node mapping
            Pos node_start{u_start, v_start}, node{u, v};
            if (!nodes.contains(node))
            {
                nodes[node] = total_nodes++;
                graph[nodes[node]] = {};

                char c = map[u][v];
                if (c == '.')
                    for (char ch : {'>', '<', 'v', '^'})
                        queue.push_back({u, v, ch});
                else
                    queue.push_back({u, v, c});
            }
            graph[nodes[node_start]][nodes[node]] = distance;
        }
        end_idx = nodes[{end.first, end.second}];
    }

    int max_steps() const
    {
        int res = 0;
        std::stack<std::set<size_t>> queue;
        std::stack<size_t> last_node;
        std::stack<int> dist;
        queue.push({start_idx});
        dist.push(0);
        last_node.push(0);

        while (queue.size())
        {
            std::set<size_t> path = queue.top();
            int cur_dist = dist.top();
            size_t last_step = last_node.top();
            queue.pop();
            dist.pop();
            last_node.pop();

            if (last_step == end_idx)
            {
                res = std::max(res, cur_dist);
                continue;
            }

            for (auto [next_node, next_dist] : graph.at(last_step))
                if (!path.contains(next_node))
                {
                    queue.push(path);
                    queue.top().insert(next_node);
                    dist.push(cur_dist + next_dist);
                    last_node.push(next_node);
                }
        }
        return res;
    }
};

int main()
{
    std::ifstream is("inputs/23.txt");
    DP dp(is);

    dp.create_graph();
    std::cout << dp.max_steps() << std::endl;
    dp.create_graph(true);
    std::cout << dp.max_steps() << std::endl;
    return 0;
}