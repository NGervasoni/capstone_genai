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

def run_seed():
    print('checking that does not crash on seed')
    result = subprocess.run([f'./{HARNESS_BIN}', 'seed/seed'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        return True, ""
    else:
        print("Errors:", result.stderr)
        return False, result.stderr
        
def extract_and_save_harness(llm_res, harness):
    lines = llm_res[0]['generated_text'].split('\n')
    start_idx = next(i for i, line in enumerate(lines) if '```' in line) + 1
    end_idx = next(i for i, line in enumerate(lines) if i > start_idx and '```' in line)
    c_code = '\n'.join(lines[start_idx:end_idx])
    with open(harness, 'w') as file:
        file.write(c_code)

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