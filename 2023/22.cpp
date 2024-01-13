#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <map>
#include <algorithm>

struct Voxel
{
    int x, y, z;

    bool operator==(const Voxel &other) const
    {
        return (x == other.x) && (y == other.y) && (z == other.z);
    }
};

template <>
struct std::hash<Voxel>
{
    size_t operator()(const Voxel &v) const
    {
        return size_t(v.x) << 16 + size_t(v.y) << 8 + size_t(v.z);
    }
};

struct Brick
{
    Voxel p0, p1;

    std::vector<Voxel> voxels() const
    {
        std::vector<Voxel> out;
        for (int z = p0.z; z <= p1.z; z++)
            for (int x = p0.x; x <= p1.x; x++)
                for (int y = p0.y; y <= p1.y; y++)
                    out.push_back({x, y, z});
        return out;
    }

    bool operator<(const Brick &other) const
    {
        return p0.z < other.p0.z;
    }
};

// dependencies denote that the brick with ID "key" is supported by a set of bricks (given by IDs in set)
using Dependencies = std::unordered_map<size_t, std::unordered_set<size_t>>;

void check_dependencies(std::map<size_t, Brick> &bricks, std::unordered_map<size_t, std::unordered_set<size_t>> &dependencies)
{
    // height_map maps a voxel position (only x y used) to the maximum height at that position, and the corresponding brick id
    std::unordered_map<Voxel, std::pair<int, size_t>> height_map;
    auto get_height_and_brick_id = [&](Voxel vox)
    {
        vox.z = 0;
        auto it = height_map.find(vox);
        if (it == height_map.end())
        {
            height_map[vox] = {0, 0};
            return std::make_pair<int, size_t>(0, 0);
        }
        return it->second;
    };

    // update brick heights (fall) and check dependencies
    for (auto &[brick_id, brick] : bricks)
    {
        // checks the heightmap for each voxel that is part of this brick, selecting the height of the highest one
        int min_height = 0;
        std::unordered_set<size_t> supported_by;
        for (const Voxel &vox : brick.voxels())
        {
            auto [occupied_height, occ_brick_id] = get_height_and_brick_id(vox);
            if (occupied_height > min_height)
            {
                min_height = occupied_height;
                supported_by.clear();
                supported_by.insert(occ_brick_id);
            }
            else if (occupied_height == min_height)
                supported_by.insert(occ_brick_id);
        }

        // updates the brick height
        int brick_height = brick.p1.z - brick.p0.z;
        if (brick_height < 0)
            throw std::runtime_error("Expected only positive heights!");
        brick.p0.z = min_height + 1;
        brick.p1.z = brick.p0.z + brick_height;

        // add dependencies
        dependencies[brick_id] = supported_by;

        // update height_map
        for (Voxel vox : brick.voxels())
        {
            int z = vox.z;
            vox.z = 0;
            height_map[vox] = {z, brick_id};
        }
    }
}

int count_destroyable(const Dependencies &dependencies)
{
    // count how many bricks can be removed
    std::unordered_set<size_t> removable;
    for (const auto &[key, deps] : dependencies)
        removable.insert(key);
    for (const auto &[key, deps] : dependencies)
        if (deps.size() == 1)
            removable.erase(*deps.begin());
    return removable.size();
}

// TODO: could be optimised by memoizing the count of fallen bricks from top-to-bottom
// as it is the code runs in < 1s, so not spending time on this now
int count_fallen_given_removal(Dependencies dependencies, size_t key_removed)
{
    int fallen = 0;
    std::unordered_set<size_t> to_remove;
    to_remove.insert(key_removed);

    while (to_remove.size() > 0)
    {
        size_t key = *to_remove.begin();
        for (auto it = dependencies.begin(); it != dependencies.end();)
        {
            const size_t &other_key = it->first;
            std::unordered_set<size_t> &dependent_bricks = it->second;
            dependent_bricks.erase(key);
            if (dependent_bricks.size() == 0)
            {
                to_remove.insert(other_key);
                it = dependencies.erase(it);
            }
            else
                it++;
        }
        to_remove.erase(key);
        fallen++;
    }
    // subtract 1 because the first removed brick doesn't count
    return fallen - 1;
}

int count_chain_reaction(const Dependencies &dependencies)
{
    int count = 0;
    for (const auto &[key, __deps] : dependencies)
        count += count_fallen_given_removal(dependencies, key);
    return count;
}

// loads input into map with unique ids for bricks (sorted in ascending z)
std::map<size_t, Brick> load_input(std::istream &is)
{
    std::vector<Brick> bricks;
    std::vector<int> vals(6);
    int val;
    while (!is.eof() && !is.bad())
    {
        for (int i = 0; i < 6; i++)
        {
            is >> val;
            is.ignore(1);
            vals[i] = val;
        }
        bricks.push_back(Brick{{vals[0], vals[1], vals[2]}, {vals[3], vals[4], vals[5]}});
    }

    // sort bricks by Z value
    std::sort(bricks.begin(), bricks.end(), [](auto &b0, auto &b1)
              { return b0.p0.z < b1.p0.z; });

    // id starts at 1 because id 0 is "ground"
    size_t id = 1;
    std::map<size_t, Brick> brick_map;
    for (const Brick &b : bricks)
        brick_map[id++] = b;
    return brick_map;
}

int main()
{
    std::ifstream is("inputs/22.txt");
    std::map<size_t, Brick> bricks = load_input(is);
    Dependencies deps;
    check_dependencies(bricks, deps);

    std::cout << count_destroyable(deps) << std::endl;
    std::cout << count_chain_reaction(deps) << std::endl;
    return 0;
}