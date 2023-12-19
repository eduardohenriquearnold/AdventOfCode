#include <iostream>
#include <fstream>
#include <sstream>
#include <utility>
#include <list>
#include <vector>
#include <string>
#include <unordered_map>

using intt = unsigned long;
using pair_str_ivec = std::pair<std::string, std::vector<intt>>;

std::istream &operator>>(std::istream &is, std::list<pair_str_ivec> &rows)
{
    std::string line;
    while (std::getline(is, line))
    {
        std::stringstream ss(line);

        std::string pattern;
        ss >> pattern;

        std::vector<intt> groups;
        intt n;
        while (ss >> n)
        {
            groups.push_back(n);
            ss.ignore(); // skip ','
        }

        rows.push_back(std::make_pair(pattern, std::move(groups)));
    }
    return is;
}

// define hash for tuple<int, int, int> - only if C++ core devs could agree on including hashes for tuples
// read more: https://stackoverflow.com/questions/68320024/why-did-the-c-standards-committee-not-include-stdhash-for-pair-and-tuple
// hash fn based on: https://www.quora.com/What-is-a-good-hash-function-for-a-pair-of-integers
struct hash_tuple { 
    template <typename T> 
    size_t operator()( 
        const std::tuple<T, T, T>& x) 
        const
    { 
        size_t h= size_t(std::get<0>(x)<<32) + size_t(std::get<1>(x) << 16) + size_t(std::get<2>(x));
        h*=1231231557ull; // "random" uneven integer 
        h^=(h>>32); 
        return h; 
    } 
};


struct DP
{
    std::string pat;
    std::vector<intt> groups;
    std::unordered_map<std::tuple<intt, intt, intt>, intt, hash_tuple> mem;

    DP(std::string pat_, std::vector<intt> groups_) : pat(pat_), groups(groups_) {}
    intt solve(size_t sidx, size_t gidx, size_t gcount)
    {
        // base case 1: more groups than specified
        if (gidx > groups.size()) return 0;
        // base case 2: end of string - either match the number of groups (two cases, string ends with # or not)
        if (sidx == pat.size())
        {
            if (gidx == groups.size() && gcount==0) return 1;
            else if (gidx == groups.size() - 1 && gcount == groups[gidx]) return 1;
            else return 0;
        } 
        
        // memoization
        auto args = std::make_tuple(sidx, gidx, gcount);
        if (mem.contains(args))
            return mem[args];

        intt ans = 0;
        char c = pat[sidx];
        if (c == '#' || c == '?')
            ans += solve(sidx + 1, gidx, gcount + 1);
        if (c == '.' || c == '?')
        {
            if (gcount == 0)
                ans += solve(sidx + 1, gidx, gcount);
            else if (gcount == groups[gidx])
                ans += solve(sidx + 1, gidx + 1, 0);
        }
        if (c != '#' && c != '.' && c!= '?')
            throw std::runtime_error("Unexpected character");

        mem[args] = ans;
        return ans;
    }
};

bool fit_criteria(const std::string &pattern, const std::vector<intt> &groups)
{
    int count = 0, group = 0;
    for (const char &c : pattern)
    {
        if (c == '#')
            count++;
        else if (count > 0)
        {
            if (group == groups.size() || count != groups[group])
                return false;
            count = 0;
            group++;
        }
    }

    if (count > 0)
    {
        if (group == groups.size() || count != groups[group])
            return false;
        group++;
    }
    return (group == groups.size());
}

// brute force method (just for comparison)
intt bf_count_arrangements(const std::string &pattern, const std::vector<intt> &groups)
{
    size_t pos_unknown = pattern.find('?');
    if (pos_unknown == std::string::npos)
        return int(fit_criteria(pattern, groups));
    else
    {
        std::string pat1(pattern), pat2(pattern);
        pat1[pos_unknown] = '.';
        pat2[pos_unknown] = '#';
        return bf_count_arrangements(pat1, groups) + bf_count_arrangements(pat2, groups);
    }
}

intt sum_counts(const std::list<pair_str_ivec> &rows)
{
    intt sum = 0;
    for (auto &[pattern, groups] : rows)
        // sum += bf_count_arrangements(pattern, groups); // BF solution
        sum += DP(pattern, groups).solve(0, 0, 0);
    return sum;
}

intt sum_counts_folded(const std::list<pair_str_ivec> &rows, int folds=5)
{
    intt sum = 0;
    for (auto& [pattern, groups] : rows)
    {
        std::string fold_pattern(pattern);
        std::vector<intt> fold_groups(groups);
        for (int i=0; i<folds-1; i++)
        {
            fold_pattern += "?" + pattern;
            fold_groups.insert(fold_groups.end(), groups.begin(), groups.end());
        }
        // sum += bf_count_arrangements(fold_pattern, fold_groups); // BF solution
        sum += DP(fold_pattern, fold_groups).solve(0, 0, 0);

    }
    return sum;
}

int main()
{
    std::list<pair_str_ivec> rows;
    std::ifstream is("inputs/12.txt");
    is >> rows;

    std::cout << sum_counts(rows) << std::endl;
    std::cout << sum_counts_folded(rows) << std::endl;
    return 0;
}
