from typing import NamedTuple

File = NamedTuple("File", (("name", str), ("size", int)))


class FileSystem:
    def __init__(self, cwd: str = "/") -> None:
        self.cwd = cwd
        self.files = {cwd: []}

    def mkdir(self, name: str):
        self.files[self.cwd + name + "/"] = []

    def mkfile(self, file: File):
        self.files[self.cwd].append(file)

    def cd(self, name: str):
        assert len(name) > 0, "folder name must be non-empty"
        assert " " not in name, "folder name must not have spaces"

        if name == "..":
            self.cwd = "/".join(self.cwd.rstrip("/").split("/")[:-1]) + "/"
        elif name == "/":
            self.cwd = name
        else:
            self.cwd += name + "/"

    def folder_size(self, path: str):
        list_subfiles = (v for k, v in self.files.items() if path in k)
        folder_size = sum((file.size for folder_subfiles in list_subfiles for file in folder_subfiles))
        return folder_size

    def all_folders_sizes(self):
        return {path: self.folder_size(path) for path in self.files.keys()}


def create_fs(inputs) -> FileSystem:
    fs = FileSystem()
    for line in inputs:
        match line.strip().split(" "):
            case ["$", "cd", folder_name]:
                fs.cd(name=folder_name)
            case ["dir", folder_name]:
                fs.mkdir(name=folder_name)
            case ["$", "ls"]:
                pass
            case [file_size, file_name]:
                fs.mkfile(File(name=file_name, size=int(file_size)))
            case _:
                raise ValueError(f"Unexpected command: {line}")
    return fs


def part1(fs_size):
    out = sum((v for v in fs_size.values() if v <= 100000))
    print(out)


def part2(fs_size):
    required_space = 30000000
    unused_space = 70000000 - fs_size["/"]
    for folder_size in sorted(fs_size.values()):
        if folder_size + unused_space >= required_space:
            print(folder_size)
            return
    print("could not find big enough folder")


inputs = open("inputs/7.txt", "r").readlines()
fs = create_fs(inputs)
fs_size = fs.all_folders_sizes()
part1(fs_size)
part2(fs_size)
