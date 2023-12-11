#include <string>
#include <utility> // for std::pair
#include <map>
#include <vector>
#include <iostream>
#include <fstream>

using coordinate = std::pair<int, int>;
using map_uv_string = std::map<coordinate, std::string>;

bool is_symbol(char c)
{
    switch (c)
    {
    case '!':
    case '@':
    case '#':
    case '$':
    case '%':
    case '^':
    case '&':
    case '*':
    case '(':
    case ')':
    case '-':
    case '+':
    case '=':
    case '/':
        return true;

    default:
        return false;
    }
}

/* Load input into maps of (u, v) to string, for numbers and symbols.
   Note: the (u, v) for numbers is the coordinate where the number starts (left-most)
*/
void load_data(std::istream &is, map_uv_string &numbers, map_uv_string &symbols)
{
    std::string current_num;
    std::pair<int, int> current_ij;
    int i = 0, j = 0;
    while (!is.eof())
    {
        char c = is.get();

        if (std::isdigit(c))
        {
            if (current_num.empty())
                current_ij = std::make_pair(i, j);
            current_num.push_back(c);
        }
        else if (!current_num.empty())
        {
            numbers[current_ij] = current_num;
            current_num.clear();
        }

        if (is_symbol(c))
            symbols[std::make_pair(i, j)] = c;
        else if (c == '\n')
        {
            i = 0;
            j++;
            continue;
        }
        i++;
    }
}

std::vector<coordinate> get_neighbours(const coordinate &uv, int number_length)
{
    const auto &[x, y] = uv;
    const size_t num_neighbours = 2 * number_length + 6;
    std::vector<coordinate> neighbours(num_neighbours);

    // left and right-most neighbours
    for (int i = 0; i < 3; i++)
    {
        neighbours[i] = std::make_pair(x - 1, y + 1 - i);
        neighbours[num_neighbours - 1 - i] = std::make_pair(x + number_length, y + 1 - i);
    }

    // up and down neighbours
    for (int i = 0; i < number_length; i++)
    {
        neighbours[2 * i + 3] = std::make_pair(x + i, y + 1);
        neighbours[2 * i + 1 + 3] = std::make_pair(x + i, y - 1);
    }

    return neighbours;
}

int count_part_numbers(const map_uv_string &numbers, const map_uv_string &symbols)
{
    int sum = 0;
    for (const auto &[uv, number] : numbers)
        for (const auto &neighbour : get_neighbours(uv, number.length()))
            if (symbols.find(neighbour) != symbols.end())
            {
                sum += std::stoi(number);
                break;
            }
    return sum;
}

int get_gear_ratio_sum(const map_uv_string &numbers, const map_uv_string &symbols)
{
    std::map<coordinate, coordinate> gears;

    for (const auto &[uv, number] : numbers)
        for (const auto &neighbour : get_neighbours(uv, number.length()))
        {
            auto it = symbols.find(neighbour);
            if (it != symbols.end())
                if (it->second.front() == '*')
                    if (gears.find(it->first) == gears.end())
                        gears[it->first] = std::make_pair(std::stoi(number), 0);
                    else
                        gears[it->first].second = std::stoi(number);
        }

    int sum = 0;
    for (const auto &[uv, gear_values] : gears)
        sum += gear_values.first * gear_values.second;
    return sum;
}

int main()
{
    map_uv_string numbers, symbols;
    std::ifstream file("inputs/3.txt");
    load_data(file, numbers, symbols);

    int sum_part_numbers = count_part_numbers(numbers, symbols);
    std::cout << sum_part_numbers << std::endl;

    int gear_ratio_sum = get_gear_ratio_sum(numbers, symbols);
    std::cout << gear_ratio_sum << std::endl;

    return 0;
}