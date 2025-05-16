from tqdm import tqdm

def clean_newlines(input_file, output_file):
    with open(input_file, 'r', encoding="utf-8") as infile:
        content = infile.read()

    # Replace all occurrences of '\n  \n' with '\n'
    cleaned_content = content.replace('\r\n        \r\n', '\r\n')
    
    with open(output_filename, 'w', encoding="utf-8") as outfile:
        outfile.write(cleaned_content)

    print("Cleanup complete!")

# Get file paths from the user
input_filename = input("Please provide the path to the input file: ")
output_filename = input("Please provide the path for the output file: ")

clean_newlines(input_filename, output_filename)
