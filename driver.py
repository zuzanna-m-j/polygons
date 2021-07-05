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

    for i,s in enumerate(box.shapes):
        v = np.array(box.vertices[i])
        st = 0
        for n in range(s):
            x, y = v[st:st+2]
            st += 2
            plt.plot(x,y,'o',label = n)
        plt.legend()
        plt.show()
