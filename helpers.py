from dataclasses import dataclass
from typing import Union
from __future__ import annotations


def get_func_length(func: binaryninja.function.Function) -> int:
    return func.address_ranges[0].end - func.address_ranges[0].start

def get_function_disassembly(func: binaryninja.function.Function, address: int):
    
    instructions = []
    arch = func.arch
    view = func.view
    func_len = get_func_length(func)
    len = 0
    while len < func_len:
        i_len = view.get_instruction_length(address + len, arch)
        instruction = arch.get_instruction_text(view.read(address + len, i_len), i_len)
        instructions.append(instruction)
        len += i_len
    
    if len != func_len:
        raise("Something went wrong")
    
    return instructions
    