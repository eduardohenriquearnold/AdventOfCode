#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <list>
#include <unordered_set>
#include <utility>

using Coord = std::pair<unsigned int, unsigned int>;
using State = std::pair<Coord, char>;

// define hash for pair<int, int> - only if C++ core devs could agree on including hashes for all stl types
// hash fn based on: https://www.quora.com/What-is-a-good-hash-function-for-a-pair-of-integers
struct hash_pair{ 
    size_t operator()( 
        const std::pair<std::pair<unsigned int, unsigned int>, char>& x) 
        const
    { 
        size_t h= size_t(x.first.first<<16) + size_t(x.first.second << 8) + size_t(x.second);
        h*=1231231557ull; // "random" uneven integer 
        h^=(h>>32); 
        return h; 
    } 
};

std::istream& operator>>(std::istream& is, std::vector<std::string>& map)
{
    std::string line;
    while (!is.eof() && !is.bad())
    {
        std::getline(is, line);
        map.push_back(line);
    }
    return is;
}

Coord next_position(const Coord& current, const char direction)
{
    int i=current.first, j=current.second;
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

// reflect and return the number of energised cells
int count_energised(const std::vector<std::string>& map, State init)
{
    std::unordered_set<State, hash_pair> states;
    std::list<State> queue{init};

    while (!queue.empty())
    {
        State state = queue.front();
        queue.pop_front();
        
        Coord pos = state.first;
        if (states.contains(state) || pos.first < 0 || pos.first >= map.size() || pos.second < 0 || pos.second >= map[0].size())
            continue;
        states.insert(state);

        char dir = state.second;
        char map_char = map[pos.first][pos.second];
        
        if (map_char=='.' || (map_char=='-' && (dir == '<' || dir == '>') || (map_char=='|' && (dir=='^' || dir=='v'))))
            queue.push_back({next_position(pos, dir), dir});
        else if (map_char == '/' || map_char == '\\')
        {
            if (dir == '>')
                dir = map_char == '/' ? '^' : 'v';
            else if (dir == '<')
                dir = map_char == '/' ? 'v' : '^';
            else if (dir == 'v')
                dir = map_char == '/' ? '<' : '>';
            else if (dir == '^')
                dir = map_char == '/' ? '>' : '<';
            else
                throw std::runtime_error("Invalid");
            queue.push_back({next_position(pos, dir), dir});
        }
        else if (map_char == '|' && (dir == '>' || dir == '<'))
        {
            queue.push_back({next_position(pos, '^'), '^'});
            queue.push_back({next_position(pos, 'v'), 'v'});
        }
        else if (map_char == '-' && (dir == 'v' || dir == '^'))
        {
            queue.push_back({next_position(pos, '<'), '<'});
            queue.push_back({next_position(pos, '>'), '>'});
        }
        else
            throw std::runtime_error("Invalid character");
   }

    // get unique positions (disregard the third State dimension) aka energised tiles
    // sadly the following line doesn't work, probably because of container type
    // std::unique(states.begin(), states.end(), [](const State& s1, const State& s2){return s1.first == s2.first;});
    std::unordered_set<State, hash_pair> states_nondir;
    for (auto& [pos, dir]: states)
        states_nondir.insert({pos, '0'});
    return states_nondir.size();
}

int max_energy(const std::vector<std::string>& map)
{
    int res = 0;
    size_t h = map.size(), w=map[0].size();
    for(int i=0; i < h; i++)
    {
        res = std::max(res, count_energised(map, {{i, 0}, '>'}));
        res = std::max(res, count_energised(map, {{i, w-1}, '<'}));
    }
    for(int j=0; j < w; j++)
    {
        res = std::max(res, count_energised(map, {{0, j}, 'v'}));
        res = std::max(res, count_energised(map, {{h-1, j}, '^'}));
    }
    return res;
}

int main()
{
    std::vector<std::string> map;
    std::ifstream is("inputs/16.txt");
    is >> map;

    std::cout << count_energised(map, {{0, 0}, '>'}) << std::endl;
    std::cout << max_energy(map) << std::endl;
    return 0;
}