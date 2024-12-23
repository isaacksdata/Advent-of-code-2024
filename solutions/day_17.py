import logging
import sys
from typing import Callable
from typing import Optional

import fire
import utilities
import z3
from main import main

logging.basicConfig(level=logging.INFO)


class Computer:
    def __init__(self, register_a: int, register_b: int, register_c: int, program: list[int]) -> None:
        self.register_a = register_a
        self.register_b = register_b
        self.register_c = register_c
        self.program = program
        self.instruction_pointer = 0
        self.instructions = []
        self.operands = []
        for i, p in enumerate(program):
            if i % 2 == 0:
                self.instructions.append(p)
            else:
                self.operands.append(p)

        self.instruction_mapping: dict[int, Callable] = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

    def get_combo_operand(self, operand: int) -> int:
        if operand in range(0, 4):
            return operand
        if operand == 4:
            return self.register_a
        if operand == 5:
            return self.register_b
        if operand == 6:
            return self.register_c
        raise ValueError("Unrecognised operand type")

    def _division(self, numerator: int, denominator: int) -> int:
        return numerator // (2**denominator)

    def adv(self, operand: int) -> None:
        self.register_a = self._division(self.register_a, self.get_combo_operand(operand))
        return None

    def bxl(self, operand: int) -> None:
        self.register_b = self.register_b ^ operand
        return None

    def bst(self, operand: int) -> None:
        self.register_b = self.get_combo_operand(operand) % 8
        return None

    def jnz(self, operand: int) -> None:
        # cant check if symbolic value is not 0 so we minus 1 here as we will add it back again during run()
        self.instruction_pointer = operand - 1
        return None

    def bxc(self, operand: int) -> None:
        self.register_b = self.register_b ^ self.register_c
        return None

    def out(self, operand: int) -> int:
        return self.get_combo_operand(operand) % 8

    def bdv(self, operand: int) -> None:
        self.register_b = self._division(self.register_a, self.get_combo_operand(operand))
        return None

    def cdv(self, operand: int) -> None:
        self.register_c = self._division(self.register_a, self.get_combo_operand(operand))
        return None

    def run(self) -> list[int]:
        output = []
        while self.instruction_pointer < len(self.instructions):
            instruction = self.instructions[self.instruction_pointer]
            operand = self.operands[self.instruction_pointer]
            func = self.instruction_mapping[instruction]
            result = func(operand)
            if result is not None:
                output.append(result)
            self.instruction_pointer += 1
        return output


class SymbolicComputer(Computer):
    """
    Key changes compared to the classic Computer class above are:
    1) set registry A to a symbolic value - we only do it for registry A as it can be seen from the program that
        only the A value is important for the output
    2) override the _division() function to use right shift operator in order to work with the z3 BitVec
    """

    def __init__(self, register_a: int, register_b: int, register_c: int, program: list[int]) -> None:
        super().__init__(register_a, register_b, register_c, program)
        self.z3_solver = z3.Optimize()
        # use BitVec instead of Int as ^ means exponent in Z3 when using ints instead of XOR
        self.register_a = z3.BitVec("a", 128)
        self.counter = 0

    def out(self, operand: int) -> int:
        if self.counter == len(self.program):
            # we are trying to recreate program so if we have len(program) worth of constraints then we are done
            raise ValueError()
        # we can add a constraint that the result here must equal the equivalent entry in program
        self.z3_solver.add(self.get_combo_operand(operand) % 8 == self.program[self.counter])
        self.counter += 1
        return self.get_combo_operand(operand) % 8

    def _division(self, numerator: int, denominator: int) -> int:
        return numerator >> denominator

    def run(self) -> list[int]:
        a = self.register_a
        try:
            super().run()
        except ValueError:
            self.z3_solver.minimize(a)
            if self.z3_solver.check() == z3.sat:
                return [self.z3_solver.model()[a]]
        return []


def prepare_data(data: list[str]) -> tuple[int, int, int, list[int]]:
    a = int(data[0].split(": ")[-1])
    b = int(data[1].split(": ")[-1])
    c = int(data[2].split(": ")[-1])
    program = list(map(int, data[4].split(": ")[-1].split(",")))
    return a, b, c, program


def solve_a(data: list[str], example: bool = False) -> str:
    computer = Computer(*prepare_data(data))
    output = computer.run()
    return ",".join([str(i) for i in output])


def solve_b(data: list[str], example: bool = False) -> int:
    # here i use Z3 library to build a system of constraints and then solve for the values which meet those constraints
    # I had not used the Z3 library before saw it mentioned on the reddit solutions thread
    computer = SymbolicComputer(*prepare_data(data))
    output = computer.run()[0]
    return int(str(output))


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    fire.Fire(main)
