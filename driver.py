#!/usr/bin/env python3
from base import*

if __name__ == "__main__":
    print("Executing driver code")
    print('----------------------')
    box = Structure("input.txt")
    print(f'Loading input script: {box.input_file}')
    print(f'Number of types: {box.types}')
    print(f'Shapes: {box.shapes}')
    print(f'Shape areas:')
    for t,s,a in zip(range(box.types),box.shapes,box.type_areas):
        print(f'Type: {t}, shape: {s}, area: {a}.')
    print(box.AREA(1))