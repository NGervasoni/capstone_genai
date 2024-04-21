import re
import subprocess

def compile(compile_command):
    print('checking that harness is compilable')
    print(f"{compile_command=}")
    result = subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        print("Compilation successful.")
        return True, ""
    else:
        print("Compilation failed.")
        print("Errors:", result.stderr)
        # with open('error.log', 'w') as file:
        #     file.write(result.stderr)
        return False, result.stderr

def run_seed(config):
    print('checking that does not crash on seed')
    result = subprocess.run(['./'+config['harness_bin'], config['seeds']+'seed'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        return True, ""
    else:
        print("Errors:", result.stderr)
        return False, result.stderr
        
# def extract_and_save_harness(llm_res, harness):
#     lines = llm_res[0]['generated_text'].split('\n')
#     start_idx = next(i for i, line in enumerate(lines) if '```' in line) + 1
#     end_idx = next(i for i, line in enumerate(lines) if i > start_idx and '```' in line)
#     c_code = '\n'.join(lines[start_idx:end_idx])
#     with open(harness, 'w') as file:
#         file.write(c_code)

def extract_and_save_harness(llm_res, harness):
    """
    Extracts C code enclosed by ```c```...``` or [C]...[/C] from the provided text and saves it to a file.

    Args:
    llm_res (dict): Dictionary containing 'generated_text' as one of its keys with the text to extract from.
    harness (str): File path where the extracted C code should be saved.
    """
    text = llm_res[0]['generated_text']
    c_code = ""

    # Check for ```c or [C] enclosed blocks
    if '```c' in text:
        # Extract code between ```c and ```
        start_marker = '```c'
        end_marker = '```'
    elif '[C]' in text:
        # Extract code between [C] and [/C]
        start_marker = '[C]'
        end_marker = '[/C]'
    elif '```' in text:
        # Extract code between ```c and ```
        start_marker = '```'
        end_marker = '```'
    else:
        print("No C code block found.")
        return

    # Find start and end indices based on identified markers
    start_idx = text.find(start_marker) + len(start_marker)
    end_idx = text.find(end_marker, start_idx)

    if start_idx > len(start_marker) - 1 and end_idx != -1:
        c_code = text[start_idx:end_idx].strip()

    # Save to file
    if c_code:
        with open(harness, 'w') as file:
            file.write(c_code)
        print(f"C code has been extracted and saved to {harness}")
    else:
        print("No C code was extracted.")


def extract_summary_stats(text):
    stats_start = text.find('Summary stats')
    if stats_start == -1:
        return {}  # Return an empty dictionary if the section is not found
    
    # Isolate the section by finding the section title and the next occurrence of '==', or the end of the file
    stats_section = text[stats_start:]
    # stats_end = stats_section.find('\n\n', stats_section.find('\n'))  # Find end by looking for next double newline after first newline
    # if stats_end == -1:
    #     stats_end = len(stats_section)
    # else:
    #     stats_section = stats_section[:stats_end]
    
    # Extract each statistic line
    lines = stats_section.split('\n')[2:]  # Skip the title and any empty line directly after it
    
    # Define a dictionary to hold the stats
    stats_dict = {}
    
    # Regex to capture key and value
    stat_regex = r'^\s*(.*?):\s*(.*)$'
    
    # Process each line
    for line in lines:
        match = re.match(stat_regex, line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
    
            # Normalize the key to a consistent format
            key = ' '.join(key.lower().split())
    
            # Convert numbers if possible
            if value.replace('.', '', 1).isdigit():  # Check if the value is a number
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
    
            # Store in dictionary
            stats_dict[key] = value


    return stats_dict

    return not float(stats['coverage reached'][:-1]) == 0