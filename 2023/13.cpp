#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <list>
#include <string>
#include <bit>

// Container should be nested container, e.g. vector<vector<int>>
template <typename Container>
class ColumnIterator
{
    using T = Container::value_type::value_type; // Element type inside vector<vector<T>>, i.e. T
private:
    Container &ref;
    size_t row, col;

public:
    ColumnIterator(Container &ref_, size_t col_ = 0) : ref(ref_), col(col_), row(0){};
    ColumnIterator(const Container &ref_, size_t col_ = 0) : ref(ref_), col(col_), row(0){};
    ColumnIterator(ColumnIterator &other) : ref(other.ref), col(other.col), row(other.row){};
    ColumnIterator(const ColumnIterator &other) : ref(other.ref), col(other.col), row(other.row){};

    ColumnIterator begin()
    {
        ColumnIterator res(*this);
        res.row = 0;
        return res;
    }
    ColumnIterator end()
    {
        ColumnIterator res(*this);
        res.row = ref.size();
        return res;
    }
    ColumnIterator &operator++()
    {
        row++;
        return *this;
    }
    ColumnIterator &operator--()
    {
        row--;
        return *this;
    }
    bool operator==(const ColumnIterator &other) const { return &ref == &(other.ref) && row == other.row && col == other.col; }
    T operator*() const { return ref[row][col]; }
};

using PatternColIterator = ColumnIterator<std::vector<std::vector<bool>>>;

class Pattern
{
public:
    std::vector<std::vector<bool>> pat;
    static size_t hash_diff;

    template <typename Iterator>
    size_t hash_array(Iterator it, Iterator end) const
    {
        size_t hash = 0, i = 0;
        for (; it != end; ++it, ++i)
            if (*it)
                hash += 1 << i;
        return hash;
    }

    int summary()
    {
        int res = 0;

        // row symmetry (horizontal lines)
        std::vector<size_t> row_hashes(pat.size());
        for (size_t i = 0; i < row_hashes.size(); i++)
            row_hashes[i] = hash_array(pat[i].cbegin(), pat[i].cend());
        res += 100 * check_symetry(row_hashes);

        // column symmetry (vertical lines)
        std::vector<size_t> col_hashes(pat[0].size());
        for (size_t i = 0; i < col_hashes.size(); i++)
            col_hashes[i] = hash_array(PatternColIterator(pat, i), PatternColIterator(pat, i).end());
        res += check_symetry(col_hashes);

        return res;
    }

    // returns the row/column at which the symetry begins (starting idx 1), 0 if none
    size_t check_symetry(std::vector<size_t> &hashes) const
    {
        for (size_t i = 1; i < hashes.size(); i++)
        {
            int incorrect_bits = 0;
            for (int idx0 = i - 1, idx1 = i; idx0 >= 0 && idx1 < hashes.size(); idx0--, idx1++)
                incorrect_bits += std::popcount(hashes[idx0] ^ hashes[idx1]);
            if (incorrect_bits == Pattern::hash_diff)
                return i;
        }
        return 0;
    }
};
size_t Pattern::hash_diff = 0;

std::istream &operator>>(std::istream &is, Pattern &p)
{
    std::string line;
    while (!is.eof() && !is.bad())
    {
        std::getline(is, line);
        if (!line.length())
            break;

        p.pat.push_back(std::vector<bool>(line.length()));
        int idx = 0;
        for (char &c : line)
            p.pat.back()[idx++] = c == '#';
    }

    // check all rows have the same number of columns
    if (!std::all_of(p.pat.begin(), p.pat.end(), [&](auto row)
                     { return row.size() == p.pat[0].size(); }))
        throw std::runtime_error("Error parsing input stream. All rows should have the same number of columns.");
    return is;
}

std::istream &operator>>(std::istream &is, std::list<Pattern> &ps)
{
    while (!is.eof() && !is.bad())
    {
        ps.push_back(Pattern());
        is >> ps.back();
    }
    return is;
}

int summaries(std::list<Pattern> &ps)
{
    int sum = 0;
    for (auto &p : ps)
        sum += p.summary();
    return sum;
}

int main()
{
    std::list<Pattern> ps;
    std::ifstream("inputs/13.txt") >> ps;

    std::cout << summaries(ps) << std::endl;
    Pattern::hash_diff = 1;
    std::cout << summaries(ps) << std::endl;
    return 0;
}