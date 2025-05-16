# Function to read a trig file and return its contents as a list of lines
def read_trig_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return []

# Function to combine two trig files into a new trig file
def combine_trig_files(file1, file2, output_file):
    trig1 = read_trig_file(file1)
    trig2 = read_trig_file(file2)

    if trig1 and trig2:
        combined_trig = trig1 + trig2

        try:
            with open(output_file, 'w') as file:
                file.writelines(combined_trig)
            print(f"Trig files '{file1}' and '{file2}' have been combined into '{output_file}'.")
        except:
            print(f"Error writing to '{output_file}'.")

# Main program
if __name__ == "__main__":
    file1 = input("Enter the name of the first trig file: ")
    file2 = input("Enter the name of the second trig file: ")
    output_file = input("Enter the name of the new combined trig file: ")

    combine_trig_files(file1, file2, output_file)
