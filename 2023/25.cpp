#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <unordered_set>
#include <set>
#include <stack>
#include <queue>
#include <vector>
#include <random>
#include <algorithm>

using Graph = std::unordered_map<std::string, std::unordered_set<std::string>>;
using Hist = std::unordered_map<std::string, size_t>;

Graph load_input(std::istream &is)
{
    Graph g;
    std::string line, first, second;
    while (!is.eof() && !is.bad())
    {
        std::getline(is, line);
        std::stringstream ss(line);

        ss >> first;
        first.pop_back();
        while (ss)
        {
            ss >> second;
            if (!g.contains(first))
                g[first] = {};
            if (!g.contains(second))
                g[second] = {};
            g[first].insert(second);
            g[second].insert(first);
        }
    }
    return g;
}

// finding shortest path between start-end (Dijkstra) and accumulate edges on Hist
void shortest_path_accumulate(const Graph &g, Hist &h, std::string start, std::string end)
{
    if (start == end)
        return;

    std::set<std::string> visited;
    std::unordered_map<std::string, int> min_distance;
    std::unordered_map<std::string, std::string> min_prev;
    auto comp = [](auto &p0, auto &p1)
    { return p0.first < p1.first; };
    std::priority_queue<std::pair<int, std::string>, std::vector<std::pair<int, std::string>>, decltype(comp)> queue;
    queue.emplace(std::make_pair(0, start));
    min_distance[start] = 0;

    // finds minimum distance from start to end
    bool found_path = false;
    while (queue.size())
    {
        auto [dist, cur] = queue.top();
        queue.pop();
        visited.insert(cur);

        if (cur == end)
        {
            found_path = true;
            break;
        }

        for (const auto &neigh : g.at(cur))
        {
            if (!visited.contains(neigh))
                queue.emplace(std::make_pair(dist + 1, neigh));
            if (!min_distance.contains(neigh) || min_distance[neigh] > dist + 1)
            {
                min_distance[neigh] = dist + 1;
                min_prev[neigh] = cur;
            }
        }
    }

    if (!found_path)
        return;

    // add edges to histogram
    for (std::string cur = end; cur != start; cur = min_prev[cur])
    {
        std::string key;
        if (cur > min_prev[cur])
            key = cur + "-" + min_prev[cur];
        else
            key = min_prev[cur] + "-" + cur;
        if (!h.contains(key))
            h[key] = 0;
        h[key]++;
    }
}

// find the likely component edges using random sampling
void cut_component_edges(Graph &g, int trials = 1000)
{
    Hist h;
    std::vector<std::string> nodes;
    for (const auto &[key, map] : g)
        nodes.push_back(key);

    // accumulate edges in shortest path between A-B nodes for random samples of A,B
    std::random_device dev;
    std::mt19937 rng(dev());
    std::uniform_int_distribution<std::mt19937::result_type> dist(0, nodes.size() - 1);
    for (int i = 0; i < trials; i++)
        shortest_path_accumulate(g, h, nodes[dist(rng)], nodes[dist(rng)]);

    // remove the most used edge (likely a bridge)
    auto it = std::min_element(h.begin(), h.end(), [](auto p0, auto p1)
                               { return p0.second > p1.second; });
    std::string edge = it->first;
    size_t pos = edge.find('-');
    std::string node0 = edge.substr(0, pos), node1 = edge.substr(pos + 1);
    g[node0].erase(node1);
    g[node1].erase(node0);
}

int count_components(const Graph &g, int expected_components = 2)
{
    std::unordered_map<std::string, int> component;
    std::stack<std::string> queue;
    std::set<std::string> to_visit;
    for (const auto &[key, map] : g)
        to_visit.insert(key);

    // connected components
    int num_clusters = 0;
    while (to_visit.size())
    {
        queue.push(*to_visit.begin());
        while (queue.size())
        {
            std::string cur = queue.top();
            queue.pop();
            to_visit.erase(cur);
            component[cur] = num_clusters;
            for (const auto &next : g.at(cur))
                if (to_visit.contains(next))
                    queue.push(next);
        }
        num_clusters++;
    }

    // histogram of components
    std::unordered_map<int, int> hist_components;
    for (auto [node, component_idx] : component)
    {
        if (!hist_components.contains(component_idx))
            hist_components[component_idx] = 0;
        hist_components[component_idx]++;
    }

    // check we only have the expected components
    if (hist_components.size() != expected_components)
    {
        std::cerr << "Expected " << expected_components << " but found" << hist_components.size() << std::endl;
        throw std::runtime_error("The number of components found does not match the number of expected components!");
    }

    // return the product of the components
    return hist_components[0] * hist_components[1];
}

int main()
{
    std::ifstream is("inputs/25.txt");
    Graph g = load_input(is);

    for (int i = 0; i < 3; i++)
        cut_component_edges(g);
    std::cout << count_components(g) << std::endl;
    return 0;
}