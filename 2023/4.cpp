#include <set>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <list>
#include <vector>
#include <cassert>
#include <algorithm>
#include <numeric>

using list_set_int = std::list<std::set<int>>;

void parse_string_set(const std::string& s, std::set<int>& set)
{
    std::stringstream stream(s);
    int num;
    while (!stream.eof())
    {
        stream >> num;
        set.insert(num);
    }
}

void load_input(std::istream& is, list_set_int& winners, list_set_int& cards)
{
    std::string winning_str, cards_str; 
    while (!is.eof())
    {
        is.ignore(50, ':');
        std::getline(is, winning_str, '|');
        std::getline(is, cards_str);
        winners.emplace_back(std::set<int>());
        cards.emplace_back(std::set<int>());
        parse_string_set(winning_str, winners.back());
        parse_string_set(cards_str, cards.back());
    }
    assert(winners.size() == cards.size());
}

int count_intersection(const std::set<int>& s1, const std::set<int>& s2)
{
    return std::count_if(s1.begin(), s1.end(), [&](const auto& num){
            return s2.find(num) != s2.end();
            });
}

int count_points(const list_set_int& winners, const list_set_int& cards)
{
    int sum = 0;
    auto it_winner = winners.begin();
    auto it_cards = cards.begin();
    for(; it_winner!= winners.end() && it_cards != cards.end(); it_winner++, it_cards++)
    {
        int n = count_intersection(*it_cards, *it_winner);
        if (n > 0)
            sum += (1 << (n-1)); // equivalent to 2^(n-1)
    }
    return sum;
}

int count_scratchcards(const list_set_int& winners, const list_set_int& cards)
{
    std::vector<int> matches(winners.size());

    // populate the number of matches for all cards
    auto it_winner = winners.begin();
    auto it_cards = cards.begin();
    auto it_matches = matches.begin();
    for(; it_winner!= winners.end() && it_cards != cards.end() && it_matches != matches.end(); it_winner++, it_cards++, it_matches++)
        *it_matches = count_intersection(*it_cards, *it_winner);

    // populate queue with all scratchcards
    std::list<int> queue(winners.size());
    std::iota(queue.begin(), queue.end(), 0);

    // start counting the number of cards
    int num_scratch_cards = 0;
    while (!queue.empty())
    {
        num_scratch_cards++;
        int cur = queue.front();
        queue.pop_front();

        for (int i=1; i<=matches[cur]; i++)
            if ((cur+i) < matches.size())
                queue.push_back(cur+i);
    }
    return num_scratch_cards;
}

int main()
{
    std::ifstream file("inputs/4.txt");
    list_set_int winners, cards;
    load_input(file, winners, cards);

    int points = count_points(winners, cards);
    std::cout << points << std::endl;

    int scratchcards = count_scratchcards(winners, cards);
    std::cout << scratchcards << std::endl;
}