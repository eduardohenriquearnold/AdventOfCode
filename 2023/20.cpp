#include <iostream>
#include <fstream>
#include <string>
#include <list>
#include <unordered_map>
#include <regex>
#include <algorithm>
#include <numeric>

struct Message
{
    std::string from, to;
    bool pulse;
};

struct Module
{
    std::vector<std::string> destinations;

    Module(const std::vector<std::string> dest_) : destinations(dest_){};
    virtual int output(const Message &m) = 0;
    void process(const Message &m, std::list<Message> &channel)
    {
        int out = output(m);
        if (out != -1)
            for (const std::string &dest : destinations)
                channel.push_back({m.to, dest, out == 1});
    }
    virtual void reset() {}
};

using ModuleMap = std::unordered_map<std::string, std::shared_ptr<Module>>;

struct Broadcaster : public Module
{
    Broadcaster(const std::vector<std::string> dest_) : Module(dest_){};
    int output(const Message &m) { return m.pulse; };
};

struct FlipFlop : public Module
{
    bool state;

    FlipFlop(const std::vector<std::string> dest_) : Module(dest_), state(false){};

    int output(const Message &m)
    {
        if (m.pulse)
            return -1;

        state = !state;
        return state;
    }
    void reset() { state = false; }
};

struct Conjunction : public Module
{
    std::unordered_map<std::string, bool> state;

    Conjunction(const std::vector<std::string> dest_) : Module(dest_){};

    void init(const ModuleMap &mm, std::string my_name)
    {
        for (const auto &[name, mptr] : mm)
            if (std::find(mptr->destinations.begin(), mptr->destinations.end(), my_name) != mptr->destinations.end())
                state[name] = false;
    }

    int output(const Message &m)
    {
        state[m.from] = m.pulse;
        return !std::all_of(state.begin(), state.end(), [&](const auto &m)
                            { return m.second; });
    }

    void reset()
    {
        for (auto &[name, val] : state)
            val = false;
    }
};

std::vector<std::string> split_string(const std::string &input, char sep)
{
    std::stringstream ss(input);
    std::string part;
    std::vector<std::string> output;

    while (getline(ss, part, sep))
    {
        part.erase(0, part.find_first_not_of(" \n\r\t"));
        output.push_back(part);
    }
    return output;
}

ModuleMap load_input(std::istream &is)
{
    const std::regex rx_line("([%|&]?)(\\w+) -> (.*)$");
    std::smatch matches;
    std::string line;
    ModuleMap mm;

    while (!is.eof() && !is.bad())
    {
        std::getline(is, line);
        if (!std::regex_match(line, matches, rx_line))
            throw std::runtime_error("Failed to pass regex!");

        const std::string type{matches[1]}, name{matches[2]};
        std::vector<std::string> dest = split_string(matches[3], ',');

        if (type == "")
            mm[name] = std::make_shared<Broadcaster>(dest);
        else if (type == "%")
            mm[name] = std::make_shared<FlipFlop>(dest);
        else if (type == "&")
            mm[name] = std::make_shared<Conjunction>(dest);
        else
            throw std::runtime_error("Invalid first character");
    }

    // initialize conjunctions
    for (auto &[name, module] : mm)
        if (auto conjunctionModule = std::dynamic_pointer_cast<Conjunction>(module))
            conjunctionModule->init(mm, name);

    return mm;
}

long count_pulses(ModuleMap &mm, int count = 1000)
{
    long low = 0, high = 0;
    std::list<Message> channel;

    for (int i = 0; i < count; i++)
    {
        // adds button message
        channel.push_front({"button", "broadcaster", false});

        // propagates through all modules
        while (!channel.empty())
        {
            try
            {
                mm.at(channel.front().to)->process(channel.front(), channel);
            }
            catch (std::out_of_range &e)
            {
            }
            if (channel.front().pulse)
                high++;
            else
                low++;
            channel.pop_front();
        }
    }
    return low * high;
}

// very strong assumptions which are dependent on input
unsigned long long min_button_taps(ModuleMap &mm)
{
    std::list<Message> channel;
    std::unordered_map<std::string, long> cycles;

    // get all gates that feed to ql (flip-flop before rx)
    for (const auto &[name, mptr] : mm)
        if (std::find(mptr->destinations.begin(), mptr->destinations.end(), "ql") != mptr->destinations.end())
            cycles[name] = 0;

    // find the cycle of each of those gates
    for (long i = 1; !std::all_of(cycles.begin(), cycles.end(), [&](auto a)
                                  { return a.second != 0; });
         i++)
    {
        // adds button message
        channel.push_front({"button", "broadcaster", false});

        // propagates through all modules
        while (!channel.empty())
        {
            try
            {
                mm.at(channel.front().to)->process(channel.front(), channel);
            }
            catch (std::out_of_range &e)
            {
            }
            if (cycles.contains(channel.front().to) && !channel.front().pulse)
                cycles[channel.front().to] = i;
            channel.pop_front();
        }
    }

    // result is the LCM of the multiple cycles (which will result Conjunction output to be 0)
    unsigned long long res = 1;
    for (const auto &[name, count] : cycles)
        res = std::lcm(res, count);
    return res;
}

int main()
{
    std::ifstream is("inputs/20.txt");
    ModuleMap mm = load_input(is);

    std::cout << count_pulses(mm) << std::endl;
    std::for_each(mm.begin(), mm.end(), [](auto m)
                  { m.second->reset(); });
    std::cout << min_button_taps(mm) << std::endl;
    return 0;
}