import logging
import sys
from typing import List
from typing import Tuple

import fire
import utilities
from main import main

logging.basicConfig(level=logging.INFO)


def get_rules_and_updates(data: list[str]) -> tuple[list[str], list[str]]:
    separation_idx = [i for i, x in enumerate(data) if x == ""][0]
    rules = data[:separation_idx]
    updates = data[separation_idx + 1 :]
    return rules, updates


def get_dependency_dict(rules: list[str]) -> dict[str, list[str]]:
    dependency_dict: dict[str, list[str]] = {}
    for rule in rules:
        pre, post = rule.split("|")
        if post in dependency_dict:
            dependency_dict[post].append(pre)
        else:
            dependency_dict[post] = [pre]
    return dependency_dict


def classify_updates(
    dependency_dict: dict[str, list[str]], updates: list[str]
) -> tuple[list[list[str]], list[list[str]]]:
    correct_updates = []
    incorrect_updates = []
    for update in updates:
        pages = update.split(",")
        failed = False
        for i, page in enumerate(pages):
            if any(d in pages[i:] for d in dependency_dict.get(page, [])):
                failed = True
                incorrect_updates.append(update.split(","))
                break
        if not failed:
            correct_updates.append(update.split(","))
    return correct_updates, incorrect_updates


def sum_middle_pages(updates: list[list[str]]) -> int:
    total = sum([int(update[len(update) // 2]) for update in updates])
    return total


def solve_a(data: list[str]) -> int:
    rules, updates = get_rules_and_updates(data)
    dependency_dict = get_dependency_dict(rules)
    correct_updates, incorrect_updates = classify_updates(dependency_dict, updates)

    return sum_middle_pages(correct_updates)


def compute_dependency_levels(dependencies: dict[str, list[str]]) -> dict[str, int]:
    levels: dict[str, int] = {}
    visited = set()

    def _dfs(key: str) -> int:
        """
        Use depth first search to find the dependency level of the key - i.e. how many pages it depends on
        """
        if key in levels:
            return levels[key]
        if key in visited:
            raise ValueError(f"Already visited {key}")
        visited.add(key)

        level = 0
        for dep in dependencies.get(key, []):
            level = max(level, _dfs(dep) + 1)
        levels[key] = level
        return level

    # Compute levels for all keys
    for key in dependencies:
        if key not in levels:
            _dfs(key)

    return levels


def correct(update: list[str], dependency_dict: dict[str, list[str]]) -> list[str]:
    sub_dep_dict = {k: v for k, v in dependency_dict.items() if k in update}
    levels = compute_dependency_levels(sub_dep_dict)
    return sorted(update, key=lambda k: levels[k])


def solve_b(data: list[str]) -> int:
    rules, updates = get_rules_and_updates(data)
    dependency_dict = get_dependency_dict(rules)
    correct_updates, incorrect_updates = classify_updates(dependency_dict, updates)
    corrected_updates = [correct(update, dependency_dict) for update in incorrect_updates]
    return sum_middle_pages(corrected_updates)


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    fire.Fire(main)
