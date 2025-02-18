import os

def execute_file(file_path):
    """ Execute commands in a .c64s file. """
    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} does not exist.")
        return

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line_number, line in enumerate(lines, 1):
        try:
            line = line.strip()
            if line.startswith("log"):
                # Handle log command (e.g., log('text') or log(8))
                print(f"Logging: {line[4:].strip('()').strip()}")
            elif line.startswith("void"):
                # Handle void(0) and void(1) commands
                print(f"Executing: {line.strip()}")
            elif line.strip().lower() == "help":
                print_help()  # Call the help function
            else:
                print(f"Unknown command at line {line_number}: {line}")
        except Exception as e:
            print(f"Error in line {line_number}: {e}")

def print_help():
    """ Display available commands in the interactive mode and file. """
    print("\nAvailable Commands:")
    print("- log: Logs text or numbers to the console. Usage: log('text') or log(8).")
    print("- void(0): Acts like 'pass' in Python. It does nothing but returns nothing.")
    print("- void(1): Checks if the process has finished. Returns a boolean indicating if finalization is running.")
    print("- void({float}): Used for finalization. Returns nothing but performs necessary cleanup when void(0) is called.")
    print("- help: Displays this help message with a list of available commands.")
    print()

def run_interactive_mode():
    """ Handle the interactive mode where the user enters commands. """
    print("Chair64 Interactive Mode (type a .c64s file path to execute it, or enter commands)")
    
    while True:
        # Get user input
        user_input = input(">>> ").strip()

        if user_input.lower() == "help":
            print_help()
        elif user_input.lower().startswith("log"):
            # Handle log command (e.g., log('text') or log(8))
            print(f"Logging: {user_input[4:].strip('()').strip()}")
        elif user_input.lower().startswith("void"):
            # Handle void(0) and void(1) commands
            print(f"Executing: {user_input.strip()}")
        elif user_input.lower() == "exit":
            print("Exiting Chair64 interactive mode...")
            break
        elif user_input:
            print(f"Unknown command: {user_input}")
            print("Type 'help' for a list of available commands.")
        else:
            print("No command entered. Type 'help' for assistance.")

def main():
    # First, check if a file path is provided
    file_path = input("Enter a .c64s file path to execute (or type 'interactive' for interactive mode): ").strip()
    
    if file_path.lower() == "interactive":
        run_interactive_mode()  # Enter the interactive mode
    elif file_path.endswith(".c64s"):
        execute_file(file_path)  # Execute the file commands
    else:
        print("Error: Invalid file or command.")
        print("Exiting program.")

if __name__ == "__main__":
    main()
