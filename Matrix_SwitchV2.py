import numpy as np 

import Matrix_Switcher

#Import the reordered bitmasks

matrix_import = Matrix_Switcher.matrix_after

#print("The matrix is: ", matrix_import)

import re

# Read the header file
with open("pin_header_file_filtered.txt", "r") as f:
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
#print("Pin Bitmasks:", pin_bitmasks)

GPIO_6_Vec = [
    pin_bitmasks['CORE_PIN35'], pin_bitmasks['CORE_PIN36'], pin_bitmasks['CORE_PIN37'], pin_bitmasks['CORE_PIN38'],pin_bitmasks['CORE_PIN39'], 
    pin_bitmasks['CORE_PIN40'], pin_bitmasks['CORE_PIN41'], pin_bitmasks['CORE_PIN13'], pin_bitmasks['CORE_PIN14'], pin_bitmasks['CORE_PIN15'],
    pin_bitmasks['CORE_PIN16'], pin_bitmasks['CORE_PIN17'], pin_bitmasks['CORE_PIN18'], pin_bitmasks['CORE_PIN19'], pin_bitmasks['CORE_PIN20'],
    pin_bitmasks['CORE_PIN21'], pin_bitmasks['CORE_PIN22'], pin_bitmasks['CORE_PIN23'], pin_bitmasks['CORE_PIN24'], pin_bitmasks['CORE_PIN25'],
    ]
GPIO_7_Vec = [
    pin_bitmasks['CORE_PIN24'], pin_bitmasks['CORE_PIN31'], pin_bitmasks['CORE_PIN32'], pin_bitmasks['CORE_PIN5'],pin_bitmasks['CORE_PIN6'], 
    pin_bitmasks['CORE_PIN7'], pin_bitmasks['CORE_PIN8'], pin_bitmasks['CORE_PIN9'], pin_bitmasks['CORE_PIN10'], pin_bitmasks['CORE_PIN11'],
    pin_bitmasks['CORE_PIN12']
    ]
GPIO_8_Vec = [
    pin_bitmasks['CORE_PIN27'], pin_bitmasks['CORE_PIN28'], pin_bitmasks['CORE_PIN29'], pin_bitmasks['CORE_PIN30']
]
GPIO_9_Vec = [
    pin_bitmasks['CORE_PIN1'], pin_bitmasks['CORE_PIN3'], pin_bitmasks['CORE_PIN4']
    ]

GPIO_6_Mask = []
GPIO_7_Mask = []
GPIO_8_Mask = []
GPIO_9_Mask = []

def Optimized_Matrix(col):
    # Initialize the masks inside the function
    GPIO_6_Mask = 0
    GPIO_7_Mask = 0
    GPIO_8_Mask = 0
    GPIO_9_Mask = 0
    
    for i in range(len(matrix_import)):  # Loop through rows
        if matrix_import[i][col] == 1:  # Access the specified column
           #print(f"Row {i}, Column {col} -> Masking")

            if 0 <= i <= 19:  # First group (rows 0-19)
                GPIO_6_Mask |= GPIO_6_Vec[i]  # Print intermediate results
                #Print(f"GPIO_6_Mask: {bin(GPIO_6_Mask)}")  # Debug print

            elif 20 <= i <= 23:  # Second group (rows 20-23)
                GPIO_8_Mask |= GPIO_8_Vec[i - 20]# Print intermediate results
                #print(f"GPIO_8_Mask: {bin(GPIO_8_Mask)}") 

            elif 24 <= i <= 26:  # Third group (rows 24-26)
                GPIO_9_Mask |= GPIO_9_Vec[i - 24]# Print intermediate results
                #print(f"GPIO_9_Mask: {bin(GPIO_9_Mask)}")# Debug print

            elif 27 <= i <= 37:  # Fourth group (rows 27-37)
                GPIO_7_Mask |= GPIO_7_Vec[i - 27]# Print intermediate results
                #print(f"GPIO_7_Mask: {bin(GPIO_7_Mask)}")  

    # Return the masks
    return GPIO_6_Mask, GPIO_7_Mask, GPIO_8_Mask, GPIO_9_Mask


def create_mask_matrix():
    # Create a 4x56 result matrix filled with zeros
    result_matrix = np.zeros((4, 56), dtype=int)
    
    # Loop through all columns (0 to 55)
    for col in range(56):  # Iterate through columns
        # Get the GPIO masks for this column
        GPIO_6_Mask, GPIO_7_Mask, GPIO_8_Mask, GPIO_9_Mask = Optimized_Matrix(col)
        
        # Store the masks in the appropriate row of result_matrix
        result_matrix[0, col] = GPIO_6_Mask
        result_matrix[1, col] = GPIO_7_Mask
        result_matrix[2, col] = GPIO_8_Mask
        result_matrix[3, col] = GPIO_9_Mask
    
    return result_matrix

def write_matrix_to_file(matrix, filename="output_matrix.txt", append=False):
    # Open the file in append mode if append is True, else in write mode
    mode = "a" if append else "w"
    with open(filename, mode) as f:  # Open in append mode if specified
        # Loop through each row of the matrix
        for row in matrix:
            # Format each element with a fixed width for proper alignment (e.g., width of 10)
            formatted_row = "   ".join([f"{elem:10}" for elem in row])  # Adjust the width (e.g., 10)
            f.write(formatted_row + "\n")  # Write the formatted row
    print(f"Matrix written to {filename}")

# Get the result matrix
result_matrix = create_mask_matrix()

# Open the file in write mode for the first matrix (this overwrites the file)
write_matrix_to_file(matrix_import, append=False)

# Add a blank line to separate the matrices
write_matrix_to_file([[""]], append=True)  # Writing a row with an empty string to create a blank line

# Write the altered matrix to the file with 3 spaces between elements (appending)
write_matrix_to_file(result_matrix, append=True)  # Write altered matrix

