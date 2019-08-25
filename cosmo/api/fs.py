# Copyright (C) 2019 CosmoHome, LLC
# Unauthorized copying and usage of this file, via any medium is strictly prohibited
# Proprietary and confidential

import os
import json
import inspect


# File System API

# Get Path from past module
def get_path(depth=3):
    mod = get_invoking_module(depth)
    if mod is None: return None
    file = mod.__file__
    return os.path.dirname(file), file.replace(os.path.dirname(file), "").replace("/", "").replace("\\", "")


# Wrapper for `get_path()`
def get_invoking_module(depth):
    try:
        frm = inspect.stack()[depth]
    except IndexError:
        return None
    mod = inspect.getmodule(frm[0])
    return mod


# Manifest Getter. Returns Name, Authors and Version
def get_manifest(api):
    with open(os.path.join(api.path, "skill.json")) as file:
        data = json.load(file)
        return data["name"], data["authors"], data["version"]

def get_phrases(api,language):
    with open(os.path.join(api.path, f"phrases/{language}.json")) as file:
        return json.load(file)


# File System Class
class FileAPI:
    def __init__(self, session):
        self.session = session

    # Request a path from the local skill directory
    def request_skill_file_path(self, file):
        return os.path.join(self.session.path, file)

    # Request a file from the local skill directory with a CosmoFile Wrapper
    def request_skill_file(self, file):
        return File(self.request_skill_file_path(file))

    # Request a file from the local skill directory with a CosmoJsonFile Wrapper
    def request_skill_file_json(self, file):
        return JsonFile(self.request_skill_file_path(file))

    # Request a path from the skill config/data directory
    def request_data_file_path(self, file):
        return os.path.join("data/skill/", self.session.name.lower().replace(" ", "_"), file)

    # Request a file from the skill config/data directory with a CosmoFile Wrapper
    def request_data_file(self, file):
        return File(self.request_data_file_path(file))

    # Request a file from the skill config/data directory with a CosmoJsonFile Wrapper
    def request_data_file_json(self, file):
        return JsonFile(self.request_data_file_path(file))


# CosmoFile Wrapper
class File:
    def __init__(self, file):
        self.file = file

    # Get Raw Open
    def open(self, perms):
        return open(self.file, perms)

    # Read Wrapper
    def read(self, size=None, b=False):
        with self.open({False: "r", True: "rb"}[b]) as f:
            if size:
                return f.read(size)
            else:
                return f.read()

    # Write Wrapper
    def write(self, value, b=False, a=False):
        perms = {False: "w", True: "a"}[a] + {False: "", True: "b"}[b]
        with self.open(perms) as f:
            f.write(value)

    # Exist Checker
    def exists(self):
        return os.path.exists(self.file)

    # Create File
    def create(self, data=""):
        # Get folders in path
        paths = list(os.path.dirname(self.file).replace("\\", "/").split("/"))
        path = ""
        # Make missing folders
        for folder in paths:
            path += f"{folder}/"
            if not os.path.exists(path):
                os.mkdir(path)
        # Make File
        with self.open("w") as f:
            f.write(self.file)

    # If Does'nt exist create file
    def exist_create(self, data=""):
        if not self.exists():
            self.create(data=data)


class JsonFile(File):
    def __init__(self, file):
        File.__init__(self, file)
        self.data = None

    def create(self, data=None):
        # If data is none, then yeet some empty json
        if data is None:
            data = {}
        # Get folders in path
        paths = list(os.path.dirname(self.file).replace("\\", "/").split("/"))
        path = ""
        # Make missing folders
        for folder in paths:
            path += f"{folder}/"
            if not os.path.exists(path):
                os.mkdir(path)
        # Make File
        with self.open("w") as f:
            f.write(json.dumps(data))

    def read(self, **kwargs):
        with self.open("r") as f:
            self.data = json.loads(f.read())
            return self.data

    def write(self, value=None, **kwargs):
        if value is None:
            value = self.data

        with self.open("w") as f:
            return json.loads(value)

    def get(self, force=False):
        if self.data is None or force is True:
            self.read()
        return self.data

    def set(self, data):
        self.write(data)
        return self.data
