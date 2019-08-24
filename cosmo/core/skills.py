# Copyright (C) 2019 CosmoHome, LLC
# Unauthorized copying and usage of this file, via any medium is strictly prohibited
# Proprietary and confidential

SKILL_DIR = "skills/"

# Skill Loader Class (Quick Fix from glebs code) (Much better in my opinion)

import os
import sys
import json
import importlib
from ..api import API


# Lets find some skills in the `SKILL_DIR`
def find_skills(cosmo):
    cosmo.logger.debug("Finding Skills")

    skills = []

    # Loop Through Folders/Files in `/skills`
    for file in os.listdir(SKILL_DIR):
        # Get full path
        file_path = os.path.join(SKILL_DIR, file)

        # Check if path is a directory?
        if os.path.isdir(file_path):

            # Check if directory has a manifest
            if os.path.exists(os.path.join(file_path, "skill.json")):
                skills.append(file)
            else:
                # Create Warning because someone made a small boo boo.
                cosmo.logger.warn(f"Directory '{file_path}' found in Skill Directory, but has no 'skill.json'")
        else:
            # Create Warning because someone made a small boo boo that's slightly bigger than the above boo boo.
            cosmo.logger.warn(f"File '{file_path}' found in Skill Directory")

    # Return File Paths
    cosmo.logger.debug(f"Found {len(skills)} Skills")
    return skills


def load_skills(cosmo, skills):
    cosmo.logger.debug("Loading Skills")
    loaded = []

    # Loop through found paths
    for skill in skills:
        # Get Paths of folder files and manifest.
        skill_path = os.path.join(SKILL_DIR, skill)

        # Load Manifest and Objects
        skill_manifest = json.load(open(os.path.join(skill_path, "skill.json"), "r"))
        skill_name = skill_manifest["name"]

        # Find Main Path and Import that MotherLove'in Bitch
        skill_main = skill_manifest["main"].replace(".py", "")
        skill_load = importlib.import_module((skill_path + "/" + skill_main).replace("/", "."))

        # Loop through all Variables in loaded skill module.
        for module_var in dir(skill_load):
            # Check if Var is a user created var
            if not module_var.startswith("__"):
                # Check if the Var is a `API` Object
                if isinstance(eval("skill_load." + module_var), API):
                    # Set the Cosmo Value to give the `API` Object a Cosmso Main Class
                    exec("skill_load." + module_var + "._set_cosmo(cosmo)")
                    # Add module to list
                    loaded.append([skill, skill_manifest])

        cosmo.logger.debug(f"Loaded Skill '{skill_name}' from '{skill_path}'")

    # Set the loaded modules into the cosmo class and return.
    cosmo.modules = loaded
    cosmo.logger.ok(f"Loaded {len(cosmo.modules)} Skills")

    return loaded
