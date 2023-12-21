#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <list>
#include <utility>
#include <algorithm>

// Lens = (label, focal)
using Lens = std::pair<std::string, int>;
using Box = std::list<Lens>;

std::istream& operator>>(std::istream& is, std::list<std::string>& seq)
{
    std::string cmd;
    while (!is.eof() && !is.bad())
    {
        std::getline(is, cmd, ',');
        seq.push_back(cmd);
    }
    return is;
}

int hash(const std::string &s)
{
    int h = 0;
    for (const char& c: s)
    {
        h += static_cast<int>(c);
        h *= 17;
        h = h % 256;
    }
    return h;
}

int sum_hashes(const std::list<std::string>& seq)
{
    int sum = 0;
    for (const auto& s: seq)
        sum += hash(s);
    return sum;
}

void initialize(std::vector<Box>& boxes, const std::list<std::string>& seq)
{
    for (const std::string &cmd: seq)
    {
        size_t pos = cmd.find('=');
        if (pos == std::string::npos)
        {
            // It's a remove ('-') cmd
            pos = cmd.find('-');
            if (pos == std::string::npos)
                std::runtime_error("Invalid command");
            std::string label = cmd.substr(0, pos);
            boxes[hash(label)].remove_if([&](Lens &l){return l.first == label;});
        }
        else
        {
            // It's an add ('=') cmd
            int val = std::stoi(cmd.substr(pos+1));
            std::string label = cmd.substr(0, pos);
            Box &b = boxes[hash(label)];
            auto it = std::find_if(b.begin(), b.end(), [&](Lens &l){return l.first == label;});
            if (it != b.end())
                it->second = val;
            else
                b.push_back(std::make_pair(label, val));
        }
    }
}

int focusing_power(const std::vector<Box>& boxes)
{
    int sum = 0;
    int box_pos = 1;
    for (const Box &b: boxes)
    {
        int lens_pos = 1;
        for (auto it = b.cbegin(); it!=b.cend(); ++it, ++lens_pos)
            sum += box_pos * lens_pos * it->second;
        box_pos++;
    }
    return sum;
}

int main()
{
    std::list<std::string> seq;
    std::vector<Box> boxes(256);
    std::ifstream is("inputs/15.txt");
    is >> seq;

    std::cout << sum_hashes(seq) << std::endl;

    initialize(boxes, seq);
    std::cout << focusing_power(boxes) << std::endl;
    return 0;
}
