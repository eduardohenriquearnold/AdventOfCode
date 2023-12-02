#include <fstream>
#include <iostream>
#include <list>
#include <array>
#include <string>

template <typename Iter>
int get_first_digit(Iter it, Iter end)
{
    while (it != end)
    {
        if (std::isdigit(*it))
            return (*it) - '0';
        it++;
    }
    throw std::invalid_argument("Could not find digit in string");
}

int get_calibration_value(const std::string code)
{
   int v0 = get_first_digit(code.begin(), code.end());
   int v1 = get_first_digit(code.rbegin(), code.rend());
   return 10* v0 + v1;
}

void convert_spelled_codes(std::list<std::string>& calibration_codes)
{
    const std::array<std::string, 9> numbers{"one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};
    for (std::string& code: calibration_codes)
    {
        size_t pos_beg = code.length(), pos_end=0;
        int num_idx_beg=-1, num_idx_end=-1;
        for (size_t idx=0; idx< numbers.size(); idx++)
        {
            const std::string& number = numbers[idx];
            size_t beg = code.find(number);
            size_t end = code.rfind(number);
            if (beg < pos_beg)
            {
                pos_beg = beg;
                num_idx_beg = idx;
            }
            if (end != std::string::npos && end > pos_end)
            {
                pos_end = end;
                num_idx_end = idx;
            }
 
        }
        if (num_idx_beg >= 0)
        {
            size_t length = numbers[num_idx_beg].length();
            code.insert(pos_beg, std::to_string(num_idx_beg + 1));
            // adjust second replacement idx (we added a new character)
            pos_end += 1;
        }
        if (num_idx_end >= 0 && pos_end != pos_beg)
            code.insert(pos_end, std::to_string(num_idx_end + 1));
    }
}

int main()
{
    // Read calibration codes from file
    std::list<std::string> calibration_codes;
    std::ifstream input_file("inputs/1.txt");
    std::string line;
    while (std::getline(input_file, line))
    {
        calibration_codes.emplace_back(line);
    }

    // Part 1
    int calibration_sum = 0;
    for (std::string code: calibration_codes)
        calibration_sum += get_calibration_value(code);
    std::cout << calibration_sum << std::endl;
    
    // Part 2
    convert_spelled_codes(calibration_codes);
    calibration_sum = 0;
    for (std::string code: calibration_codes)
        calibration_sum += get_calibration_value(code);
    std::cout << calibration_sum << std::endl;
}