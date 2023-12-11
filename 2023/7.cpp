#include <iostream>
#include <fstream>
#include <array>
#include <vector>
#include <string>
#include <map>
#include <algorithm>
#include <cassert>

class Hand
{
public:
    static std::map<char, int> deck;
    static bool jokers;

    std::string cards;
    int bid;

    Hand(int bid_, std::string &cards_) : bid(bid_), cards(cards_)
    {
        assert(cards_.size() == 5);
    }

    int rank() const
    {
        std::vector<int> counter(15, 0);
        for (char c : cards)
            counter[deck.at(c)]++;

        int joker_count = jokers ? counter[deck.at('J')] : 0;
        if (jokers)
            // When jokers are wildcards we remove them from the counting
            counter[deck.at('J')] = 0;

        std::sort(counter.begin(), counter.end(), std::greater<>());

        if (counter[0] == 5 - joker_count)
            return 7;
        else if (counter[0] == 4 - joker_count)
            return 6;
        else if (counter[0] + counter[1] == 5 - joker_count)
            return 5;
        else if (counter[0] == 3 - joker_count)
            return 4;
        else if (counter[0] + counter[1] == 4 - joker_count)
            return 3;
        else if (counter[0] == 2 - joker_count)
            return 2;
        else
            return 1;
    }

    bool operator<(const Hand &other) const
    {
        int this_rank = rank();
        int other_rank = other.rank();
        if (this_rank == other_rank)
        {
            for (size_t i = 0; i < cards.size(); i++)
            {
                int this_v = deck.at(cards[i]);
                int other_v = deck.at(other.cards[i]);
                if (this_v != other_v)
                    return this_v < other_v;
            }
        }
        return this_rank < other_rank;
    }
};

// Default settings
std::map<char, int> Hand::deck = {{'2', 2}, {'3', 3}, {'4', 4}, {'5', 5}, {'6', 6}, {'7', 7}, {'8', 8}, {'9', 9}, {'T', 10}, {'J', 11}, {'Q', 12}, {'K', 13}, {'A', 14}};
bool Hand::jokers = false;

std::istream &operator>>(std::istream &is, std::vector<Hand> &hands)
{
    std::string cards;
    int bid;
    while (!is.eof())
    {
        is >> cards >> bid;
        hands.push_back(Hand(bid, cards));
    }
    return is;
}

int get_total_winnings(std::vector<Hand> &hands)
{
    std::sort(hands.begin(), hands.end());
    int sum = 0;
    for (size_t i = 0; i <= hands.size(); i++)
    {
        sum += (i + 1) * hands[i].bid;
    }
    return sum;
}

int main()
{
    std::vector<Hand> hands;
    std::ifstream is("inputs/7.txt");
    is >> hands;

    int winnings = get_total_winnings(hands);
    std::cout << winnings << std::endl;

    // Part 2
    Hand::deck['J'] = 1;
    Hand::jokers = true;

    winnings = get_total_winnings(hands);
    std::cout << winnings << std::endl;
    return 0;
}