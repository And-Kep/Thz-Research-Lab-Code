import numpy as np 

import Matrix_Switcher

#Import the reordered bitmasks

matrix_import = Matrix_Switcher.matrix_after

print("The matrix is: ", matrix_import)

import re

# Read the header file
with open("core_pins.txt", "r") as f:
    content = f.readlines()

# Dictionary to store pin bits
pin_bits = {}

# Regular expression to match pin bit definitions
bit_pattern = re.compile(r"#define\s+(CORE_PIN\d+_BIT)\s+(\d+)")

# Extract pin bit values
for line in content:
    match = bit_pattern.match(line)
    if match:
        pin_name, pin_value = match.groups()
        pin_bits[pin_name.replace("_BIT", "")] = int(pin_value)

# Compute bitmasks
pin_bitmasks = {pin: (1 << bit) for pin, bit in pin_bits.items()}

# Print the extracted values
# print("Pin Bits:", pin_bits)
print("Pin Bitmasks:", pin_bitmasks)

GPIO_6_Vec = [
    pin_bitmasks['CORE_PIN35'], pin_bitmasks['CORE_PIN36'], pin_bitmasks['CORE_PIN37'], pin_bitmasks['CORE_PIN38'],pin_bitmasks['CORE_PIN39'], 
    pin_bitmasks['CORE_PIN40'], pin_bitmasks['CORE_PIN41'], pin_bitmasks['CORE_PIN13'], pin_bitmasks['CORE_PIN14'], pin_bitmasks['CORE_PIN15'],
    pin_bitmasks['CORE_PIN16'], pin_bitmasks['CORE_PIN17'], pin_bitmasks['CORE_PIN18'], pin_bitmasks['CORE_PIN19'], pin_bitmasks['CORE_PIN20'],
    pin_bitmasks['CORE_PIN21'], pin_bitmasks['CORE_PIN22'], pin_bitmasks['CORE_PIN23'], pin_bitmasks['CORE_PIN24'], pin_bitmasks['CORE_PIN25'],
    
    ]

GPIO_6-Mask = []

for row in matrix_import:
    if row >= 0 & row<20:
        if matrix_import[row][0] == 1:
            GPIO_6-Mask |= GPIO_6_Vec[row]
            print(GPIO_6-mask)