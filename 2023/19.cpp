#include <iostream>
#include <fstream>
#include <unordered_map>
#include <list>
#include <regex>
#include <limits>

int MAX = std::numeric_limits<int>::max();

struct Part
{
    int x, m, a, s;
    std::string pile;

    int operator[](char c) const
    {
        switch (c)
        {
        case 'x':
            return x;
        case 'm':
            return m;
        case 'a':
            return a;
        case 's':
            return s;
        default:
            throw std::runtime_error("Unexpected property");
        }
    }

    int rating() const { return x + m + a + s; }
};

struct Interval
{
    // interval start is inclusive, but end is NOT inclusive
    int xstart, xend;
    int mstart, mend;
    int astart, aend;
    int sstart, send;
    std::string pile;

    long size() const { return long(xend - xstart) * long(mend - mstart) * long(aend - astart) * long(send - sstart); }

    inline std::pair<int, int> axis_intersection(int start0, int end0, int start1, int end1) const
    {
        auto new_start = std::max(start0, start1);
        auto new_end = std::min(end0, end1);
        if (new_start < new_end)
            return {new_start, new_end};
        else
            return {0, 0};
    }

    Interval operator&(const Interval &other) const
    {
        auto [nxstart, nxend] = axis_intersection(xstart, xend, other.xstart, other.xend);
        auto [nmstart, nmend] = axis_intersection(mstart, mend, other.mstart, other.mend);
        auto [nastart, naend] = axis_intersection(astart, aend, other.astart, other.aend);
        auto [nsstart, nsend] = axis_intersection(sstart, send, other.sstart, other.send);
        return Interval{nxstart, nxend, nmstart, nmend, nastart, naend, nsstart, nsend, pile};
    }
};

struct Condition
{
    char variable;
    char comp;
    int threshold;
    std::string destination;

    bool operator()(const Part &p) const
    {
        switch (comp)
        {
        case '>':
            return p[variable] > threshold;
        case '<':
            return p[variable] < threshold;
        case '\0':
            // terminal condition
            return true;
        default:
            throw std::runtime_error("Invalid operator!");
        }
    }

    // if positive, get interval for which condition matches
    // if !positive, get interval for which condition does NOT match
    Interval get_interval(bool positive) const
    {
        int xstart, mstart, astart, sstart, xend, mend, aend, send;
        xstart = mstart = astart = sstart = 0;
        xend = mend = aend = send = MAX;

        if (comp == '\0' && !positive)
            return {0, 0, 0, 0, 0, 0};

        char comp_ = positive ? comp : (comp == '>' ? '<' : '>');

        int *pstart, *pend;
        switch (variable)
        {
        case 'x':
            pstart = &xstart;
            pend = &xend;
            break;
        case 'm':
            pstart = &mstart;
            pend = &mend;
            break;
        case 'a':
            pstart = &astart;
            pend = &aend;
            break;
        case 's':
            pstart = &sstart;
            pend = &send;
            break;
        default:
            break;
        }

        switch (comp_)
        {
        case '>':
            *pstart = threshold + int(positive);
            break;
        case '<':
            *pend = threshold + int(!positive);
            break;
        default:
            break;
        }
        return {xstart, xend, mstart, mend, astart, aend, sstart, send, destination};
    }
};

struct Workflow
{
    std::list<Condition> conditions;

    std::string operator()(const Part &p) const
    {
        for (const Condition &condition : conditions)
            if (condition(p))
                return condition.destination;
        throw std::runtime_error("No condition applies!");
    }

    std::list<Interval> operator()(Interval &i) const
    {
        std::list<Interval> output;
        for (const Condition &condition : conditions)
        {
            output.push_back(condition.get_interval(true) & i);
            i = i & condition.get_interval(false);
        }
        return output;
    }
};

void sort(const std::unordered_map<std::string, Workflow> &workflows, std::list<Part> &parts)
{
    for (Part &p : parts)
        while (p.pile != "A" && p.pile != "R")
            p.pile = workflows.at(p.pile)(p);
}

int rating_accepted(const std::list<Part> &parts)
{
    int sum = 0;
    for (const Part &p : parts)
        if (p.pile == "A")
            sum += p.rating();
    return sum;
}

unsigned long accepted_combinations(const std::unordered_map<std::string, Workflow> &workflows)
{
    const int MIN_VAL = 1, MAX_VAL = 4001;
    std::list<Interval> queue, accepted;
    queue.push_back({MIN_VAL, MAX_VAL, MIN_VAL, MAX_VAL, MIN_VAL, MAX_VAL, MIN_VAL, MAX_VAL, "in"});

    // Get all intervals that are accepted
    while (!queue.empty())
    {
        Interval i = queue.front();
        queue.pop_front();

        if (i.pile == "A")
            accepted.push_back(i);
        else if (i.pile == "R")
            continue;
        else
            queue.splice(queue.begin(), workflows.at(i.pile)(i));
    }

    // Compute the cardinality of the union of accepted intervals
    // assumes no intersection between accepted intervals, otherwise would have to use
    // the expensive Inclusion-Exclusion principle
    unsigned long num = 0;
    for (const Interval &i : accepted)
        num += i.size();
    return num;
}

std::istream &operator>>(std::istream &is, std::unordered_map<std::string, Workflow> &workflows)
{
    const std::regex rx_line("(\\w+)\\{(.*)\\}"), rx_rule("(x|m|a|s)(<|>)(\\d+):(\\w+),|(\\w+)");
    std::smatch matches;

    std::string line;
    while (!is.bad() && !is.eof())
    {
        std::getline(is, line);
        if (line.empty())
            break;

        if (!std::regex_match(line, matches, rx_line))
            throw std::runtime_error("Failed to pass regex!");
        std::string wf_name{matches[1]}, rules{matches[2]};

        workflows[wf_name] = Workflow();
        Workflow &workflow = workflows[wf_name];
        for (std::sregex_iterator it(rules.begin(), rules.end(), rx_rule), end; it != end; it++)
        {
            if ((*it)[1].matched)
                workflow.conditions.push_back(Condition{(*it)[1].str()[0], (*it)[2].str()[0], std::stoi((*it)[3].str()), (*it)[4]});
            else if ((*it)[5].matched)
                // last part of the Workflow (always true)
                workflow.conditions.push_back(Condition{'x', '\0', 0, (*it)[5]});
            else
                throw std::runtime_error("Failed to pass regex!");
        }
    }

    return is;
}

std::istream &operator>>(std::istream &is, std::list<Part> &parts)
{
    const std::regex rx_line("\\{x=(\\d+),m=(\\d+),a=(\\d+),s=(\\d+)}");
    std::smatch m;

    std::string line;
    while (!is.bad() && !is.eof())
    {
        std::getline(is, line);
        if (!std::regex_match(line, m, rx_line))
            throw std::runtime_error("Failed to pass regex!");

        auto mtoi = [](const auto &m)
        { return std::stoi(m.str()); };
        parts.push_back(Part{mtoi(m[1]), mtoi(m[2]), mtoi(m[3]), mtoi(m[4]), "in"});
    }
    return is;
}

int main()
{
    std::unordered_map<std::string, Workflow> workflows;
    std::list<Part> parts;

    std::ifstream is("inputs/19.txt");
    is >> workflows >> parts;

    sort(workflows, parts);
    std::cout << rating_accepted(parts) << std::endl;
    std::cout << accepted_combinations(workflows) << std::endl;
    return 0;
}