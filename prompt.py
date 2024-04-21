import clang.cindex

COMMON_LIBS = """
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
"""

def extract_includes(c_file_path, src_folder_path):

    # Initialize Clang index
    index = clang.cindex.Index.create()
    # Parse the C file
    try:
        translation_unit = index.parse(c_file_path, args=['-x', 'c', '-std=c11'])
    except clang.cindex.TranslationUnitLoadError:
        pass
    else:
        file_paths = [x.include.name for x in translation_unit.get_includes()]
    try:
        tu = index.parse(c_file_path[:-1]+'h', args=['-x', 'c', '-std=c11'])
    except clang.cindex.TranslationUnitLoadError:
        pass
    else:
        file_paths = file_paths + [x.include.name for x in tu.get_includes()]
    final_names = [f"#include <{path.split('/')[-1]}>" 
                   if path.startswith('/usr/include') else path for path in file_paths]
    custom_lib = [path for path in final_names if path.startswith(src_folder_path)]
    # return common + "\n".join([f'#include "{path.split("/")[-1]}"'
                   # if path.startswith(src_folder_path) else path for path in final_names]), custom_lib
    return "\n".join([f'#include "{path[len(src_folder_path):]}"' for path in custom_lib]), custom_lib

def generate_initial_prompt(config):
    role = f"You are a developer. you need to write a libFuzzer target for the {config['function_name']} function of your c library."
    template, custom_lib = extract_includes(config['c_file_path'], config['src_folder_path'])
    fill_c = '''
    <FILL>
    
    int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    '''
    fill_cpp = '''
    <FILL>
    
    extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    '''

    template = template +'''
    // Step 2 include custom and standard headers
    '''+ fill_c if {config['is_c_code']} else fill_c_cp
    template = template +f'''
    
    // Step 3 call to the {config['function_name']} function
    <FILL>;
    
    ''' + '''
      return 0;
    }
    '''
    graph='}'

    lib_for_prompt = ''

    code_md = '```c' if {config['is_c_code']} else '```c++'

    # for l in config['lib_files']:
    #     with open(l, encoding='utf-8', errors='ignore') as file:
    #         content = f"\n{l}\n{code_md}\n{file.read()}\n```\n"
    #     lib_for_prompt = lib_for_prompt + content
    for l in custom_lib:
        with open(l, encoding='utf-8', errors='ignore') as file:
            content = f"\n{l}\n{code_md}\n{file.read()}\n```\n"
        lib_for_prompt = lib_for_prompt + content
        # try:
        #     with open(l[:-1]+'c', encoding='utf-8', errors='ignore') as file: #TODO fix for c++
        #         content = f"\n{l[:-1]+'c'}\n{code_md}\n{file.read()}\n```\n"
        #     lib_for_prompt = lib_for_prompt + content
        # except FileNotFoundError:
        #     pass
    lib_for_prompt = f'''
    ## Library:
    {lib_for_prompt}
    ## End of library
    '''

    initial_prompt = f"""
    {role}
    Work step by step:
    1. Identify and analyze {config['function_name']} in the library source code: which headers and parameters does it need to be properly executed?
    2. Fill the template with necessary headers
    3. fill the template LLVMFuzzerTestOneInput function with a call to {config['function_name']}, such that {config['function_name']} can be properly fuzz
    Answer should be code only, no explanation.
    
    {lib_for_prompt}
    
    ## Start of template:
    {code_md}
    {template}
    ```
    ## End of template:
     """
    initial_prompt = '[INST]' + initial_prompt + '[/INST]'
    return initial_prompt


def generate_initial_prompt_by_example(config):
    role = f"You are a C/C++ developer. You do not know any other programming languages.  Can you write a C/C++ libFuzzer target for the {config['function_name']} function of your c library? You are provided with an example of how the function {config['function_name']} is used."
    template, custom_libs = extract_includes(config['c_file_path'], config['src_folder_path'])
    fill_c = '''
<FILL>

int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
'''
    fill_cpp = '''
<FILL>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
'''

    template = template +'''
// Step 1 include missing custom and standard headers
'''+ fill_c if {config['is_c_code']} else fill_c_cp
    template = template +f'''

// Step 2 insert call to the {config['function_name']} function
<FILL>;

''' + '''
      return 0;
    }
    '''
    # graph = '}'

    lib_for_prompt = ''

    code_md = '[C]' if {config['is_c_code']} else '[C++]'
    # code_md = '```c' if {config['is_c_code']} else '```c++'
    
    # for l in config['lib_files']:
    #     with open(l, encoding='utf-8', errors='ignore') as file:
    #         content = f"\n{l}\n{code_md}\n{file.read()}\n```\n"
    #     lib_for_prompt = lib_for_prompt + content
    # for l in custom_lib:
    #     with open(l, encoding='utf-8', errors='ignore') as file:
    #         content = f"\n{l}\n{code_md}\n{file.read()}\n```\n"
    #     lib_for_prompt = lib_for_prompt + content
        # try:
        #     with open(l[:-1]+'c', encoding='utf-8', errors='ignore') as file: #TODO fix for c++
        #         content = f"\n{l[:-1]+'c'}\n{code_md}\n{file.read()}\n```\n"
        #     lib_for_prompt = lib_for_prompt + content
        # except FileNotFoundError:
        #     pass
    with open(config['example'], encoding='utf-8', errors='ignore') as file:
        # example = f"\n{code_md}\n{file.read()}\n```\n"
        example = f"\n{code_md}\n{file.read()}\n[/\n"
    example = f'''
## Example:
{example}
## End of example
'''
    initial_prompt = f"""
{role}
Fill the provided C/C++ template by working in steps:
Answer should be C/C++ code only, no explanation.

{example}

## Start of template:
{code_md}
{COMMON_LIBS}
{template}
# ```
[/C]
## End of template
"""
    initial_prompt = '[INST]\n' + initial_prompt + '\n[/INST]'
    return initial_prompt
    
def followup_prompt(prev_prompt, prev_respose, new_prompt):
    p = ""
    if not prev_prompt.startswith('<s>'):
        p = '<s>'
    p = p + prev_prompt + '\n' + prev_respose + '</s>'
    p = p + f'<s>[INST]\n{new_prompt}\n[/INST]'
    return p