import sys
import os
import re

finalizing = False  # Tracks if the script is in finalization state

def process_file(file_path):
    """Reads and processes a .c64s file, executing supported functions like log()."""
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for line_num, line in enumerate(lines, 1):
            execute_line(line.strip(), file_path, line_num)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def execute_line(line, file_path="REPL", line_num=None):
    """Executes a single line of Chair64 code and handles errors."""
    global finalizing  # Needed to check the exit state

    # Match log("text") or log('text') for string logging
    log_string_match = re.match(r'log\(["\'](.*?)["\']\)', line)

    # Match log(number) where number is an integer or float
    log_number_match = re.match(r'log\((\d+(\.\d+)?)\)', line)

    # Match log(True) or log(False) (booleans)
    log_boolean_match = re.match(r'log\((True|False)\)', line)

    # Match log(void) for JavaScript-like undefined/null
    log_void_match = re.match(r'log\(void\)', line)

    # Match void(0); as a standalone function (does nothing)
    void_0_match = re.match(r'^void\(0\);$', line)

    # Match void(1); – Should return True only if exiting
    void_1_match = re.match(r'^void\(1\);$', line)

    # Match void(); as a standalone function (does nothing)
    void_empty_match = re.match(r'^void\(\);$', line)

    # Handle void() as a no-op function
    if line == "void()":
        return  # Does nothing, just like Python's `pass`

    if log_string_match:
        print(log_string_match.group(1))  # Print extracted string
    elif log_number_match:
        print(log_number_match.group(1))  # Print extracted number
    elif log_boolean_match:
        print(log_boolean_match.group(1))  # Print True or False
    elif log_void_match:
        print("None")  # Print None (like JavaScript's undefined)
    elif void_0_match or void_empty_match:
        return None  # Does nothing, returns None (like void(0); and void();)
    elif void_1_match:
        return finalizing  # Returns True only if finalizing (quitting process)
    elif line:  # If the line isn't empty and isn't recognized
        error_message = f"\033[91mTraceback {file_path}\nFound error at line {line_num if line_num else 'Unknown'}\n{line} is not defined\033[0m"
        print(error_message)

def interactive_mode():
    """Starts an interactive command line where the user can run commands or open a .c64s file."""
    print("Chair64 Interactive Mode (type a .c64s file path to execute it, or enter commands)")
    
    global finalizing

    while True:
        try:
            user_input = input(">>> ").strip()
            
            if user_input.lower() in {"exit", "quit"}:  # Allow user to exit
                finalizing = True  # Set finalizing state before exiting
                print("Exiting Chair64.")
                break
            
            if os.path.isfile(user_input) and user_input.endswith('.c64s'):
                process_file(user_input)  # If it's a valid file, run it
            else:
                execute_line(user_input, "REPL", "1")  # Treat input as a command

        except EOFError:
            finalizing = True  # Set finalizing state when EOF is detected
            print("\nExiting Chair64.")
            break

def main():
    """Main execution logic for Chair64."""
    global finalizing

    if len(sys.argv) > 1:
        file_path = sys.argv[1].strip()
        if file_path.startswith('"') and file_path.endswith('"'):
            file_path = file_path[1:-1]

        if file_path.endswith('.c64s') and os.path.isfile(file_path):
            process_file(file_path)
        else:
            print(f"Error: '{file_path}' is not a valid .c64s file or does not exist.")
            interactive_mode()
    else:
        interactive_mode()

if __name__ == "__main__":
    main()
