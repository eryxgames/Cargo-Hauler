import os

def create_full_project_file(files, output_file="app_fullproject.txt"):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("You are professional developer and game designer. Here is project code and structure of a python app, rpg space adventure trading game with data science visualization demo stats:\n\n")
        outfile.write("structure: list of files\n\n")
        
        # Write the list of files
        for file in files:
            if os.path.isfile(file) and (file.endswith('.json') or file.endswith('.py') or file.endswith('.txt')):
                outfile.write(f"- {file}\n")
            else:
                print(f"Skipping {file} - not a valid file or unsupported file type.")
        
        outfile.write("\n")
        
        # Write the content of each file
        for file in files:
            if os.path.isfile(file) and (file.endswith('.json') or file.endswith('.py') or file.endswith('.txt')):
                outfile.write(f"File name: {file}\n")
                with open(file, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    outfile.write(f"content of {file}\n")
                    outfile.write(content)
                    outfile.write("\n\n")

def main():
    # List of files to include in the project file
    files = [
        'requirements.txt',
        'src/main.py',
        'src/player.py',
        'src/economy.py',
        'src/events.py',
        'src/technologies.py',
        'src/universe.py',
        'src/visualization.py',
        'data/planets.json',
        'data/quests.json',
        'data/commodities.json'
        # Add more files as needed
    ]
    
    create_full_project_file(files)

if __name__ == "__main__":
    main()