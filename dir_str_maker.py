
folder = "./"
# exclude all that are present on .gitignore 
excludes = ["__pycache__", ".git", ".gitignore", ".vscode", "venv", ".idea", "node_modules", "build", "dist", 
            "package-lock.json", "package.json", "yarn.lock", "yarn-error.log", "yarn-error.log", 
            "practice", "llm_log_old", "llm_logs", "notes", "downloads", "llm_log.log"
            ]
def make_dir_str(folder, excluded=[]):
    """
    gives structure in this format
    src-|
        |- folder1-|
                    |- file1
                    |- file2
        |- folder2-|
                    |- file1
                    |- file2
    """
    import os
    # for root, dirs, files in os.walk(folder):
    #     level = root.replace(folder, '').count(os.sep)
    #     indent = ' ' * 4 * (level)
    #     print('{}|-{}/'.format(indent, os.path.basename(root)))
    #     subindent = ' ' * 4 * (level + 1)
    #     for f in files:
    #         print('{}|-{}'.format(subindent, f))
    for files in os.listdir(folder):
        for file in files:
            if file in excluded:
                files.remove(file+"/")
        
        print(f"{folder}{files}")
        input("incdd>")
        if os.path.isdir(f"{folder}{files}"):
            make_dir_str(f"{folder}{files}/")
        else:
            print(f"{folder}{files}")

make_dir_str(folder)