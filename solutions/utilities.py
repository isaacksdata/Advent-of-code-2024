import os
import timeit
from typing import Any
from typing import Callable
from typing import List

from aocd import get_data
from aocd import submit
from dotenv import load_dotenv


load_dotenv()


def get_session() -> str:
    """
    Get the AOC session key from local environment
    :return: AOC session key
    """
    return os.environ["AOC_SESSION"]


def get_puzzle(year: int, day: int) -> str:
    """
    Use the AOC API to get the challenge data
    :param year: year of the challenge
    :param day: day of the challenge
    :return:
    """
    return get_data(session=get_session(), day=day, year=year)


def submit_answer(answer: int, part: str, day: int, year: int) -> None:
    """
    Submit and answer to AOC
    :param answer: Answer to the problem
    :param part: part of the problem e.g. A or B
    :param day: The day of the problem
    :param year: The year of the problem
    :return: void
    """
    submit(answer, part=part, day=day, year=year, session=get_session())


def save_sample_data(data: List[str], path: str) -> None:
    """
    Save some sample data to file
    :param data: data to save to txt file
    :param path: path to save the data to
    :return: void
    """
    with open(path, "w", encoding="utf-8") as file:
        file.writelines("\n".join(data))


def read_sample_data(path: str) -> List[str]:
    """
    Read some sample data for testing with
    :param path: path to sample data
    :return: data from file
    """
    with open(path, "r", encoding="utf-8") as file:
        data = file.readlines()
    data = [x.replace("\n", "") for x in data]
    return data


def format_input_data(data: str) -> List[str]:
    """
    Data is normally returned by API as single string. This function splits into lines
    :param data: input data string
    :return: data separated into lines
    """
    return data.splitlines()


def run_and_measure(func: Callable, args: List[Any], n: int) -> float:
    total_time = timeit.timeit(lambda: func(*args), number=n)
    average_time = total_time / n
    return average_time
