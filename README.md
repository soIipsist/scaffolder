# Scaffolder

Command Line Interface (CLI) scaffolding tool designed to create projects using personalized templates. These templates are organized as directories within the designated `templates` folder. To configure project metadata before its creation, users can define specifications in the `src/scaffolder.json` file.

## Installation

It is recommended to use Python version 3.11 or above.

For repository creation, authentication with `gh` is essential. Running `scaffolder.sh` will automatically install all dependencies, unless explicitly declined during the installation process.

### Manual installation (Git)

1. Clone the git repository:

    ```bash
    git clone https://github.com/soIipsis/scaffolder.git
    ```

2. Install all package dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run `scaffolder.sh`

4. If you're on **Linux**, Create an alias in your .bashrc :

      ```bash
      chmod +x /path-to-release/scaffolder/scaffolder.sh
      alias scaffolder="bash /path-to-release/scaffolder/scaffolder.sh"

      ```

### Pip (Linux, Windows)

```bash
pip install git+https://github.com/soIipsis/scaffolder@main
```

## Usage

### Commands

#### scaffold

Creates a new project by utilizing a specified `template_directory` as a baseline. The resulting project will be scaffolded in a `project_directory` of your choice, as specified in the `scaffolder.json` settings file.

Users have the flexibility to customize parameters either by directly modifying the file or by providing new values through the CLI. If `create_repository` is set to true, an initialized GitHub repository will be created automatically, with all the main files included in the original `template_directory`.

**_Note: All words containing the project's name will be renamed in the default template, including files._**

```bash
scaffolder >  scaffold [-h] [-t TEMPLATE_DIRECTORY] [-p PROJECT_DIRECTORY] [-l LICENSE] [-a AUTHOR] [-u GIT_USERNAME] [-r CREATE_REPOSITORY] [-v REPOSITORY_VISIBILITY]

options:
  -h, --help                                                               show this help message and exit
  -t TEMPLATE_DIRECTORY, --template_directory TEMPLATE_DIRECTORY           template directory to copy files from
  -p PROJECT_DIRECTORY, --project_directory PROJECT_DIRECTORY              destination directory of your scaffolded project
  -l LICENSE, --license LICENSE                                            creates license file (mit, afl-3.0, apache-v2.0 etc.)
  -a AUTHOR, --author AUTHOR                                               set name of the author (replaces every instance within the license file)
  -u GIT_USERNAME, --git_username GIT_USERNAME                             set git username (git config username is used by default)
  -r CREATE_REPOSITORY, --create_repository CREATE_REPOSITORY              if set to true, creates a git repository using the git cli tool (gh)
  -v REPOSITORY_VISIBILITY, --repository_visibility REPOSITORY_VISIBILITY  set git repository visibility (0: private, 1: public, 2: internal)

```

#### update

Updates files in an `update_destination_directory` with those from a `update_source_directory`. The extraction of updated functions is governed by `function_patterns`, specified in the `function_patterns.json` file. By default, Python pattern matching is employed.

```bash
scaffolder > update -h
usage: scaffolder update [-h] [--update_source_directory SOURCE_DIRECTORY] [--update_destination_directory UPDATE_DESTINATION_DIRECTORY] [-f FUNCTION_PATTERNS [FUNCTION_PATTERNS ...]]
                         files [files ...]

positional arguments:
  files                                                                                             Template files to update (must be the same name)

options:
  -h, --help                                                                                        show this help message and exit
  --update_source_directory SOURCE_DIRECTORY                                                               project directory to update from
  --update_destination_directory UPDATE_DESTINATION_DIRECTORY                                                               destination project directory for updated files
  -f FUNCTION_PATTERNS [FUNCTION_PATTERNS ...], --function_patterns FUNCTION_PATTERNS [FUNCTION_PATTERNS ...]

```

#### licenses

The `licenses` command can be used to list all supported software license files. If a valid `license` is specified, its content will be printed out.

```bash
scaffolder > licenses [-h] [-l LICENSE]


options:
  -h, --help                     show this help message and exit
  -l LICENSE, --license LICENSE
```

#### settings

View `scaffolder.json` metadata, or manually update a specified parameter.

```bash

scaffolder > settings [-h] {update} ...

positional arguments:
  {update, view}

options:
  -h, --help     show this help message and exit

```

```bash

scaffolder > settings update [-h] [-t TEMPLATE_DIRECTORY] [-p PROJECT_DIRECTORY] [-l LICENSE] [-a AUTHOR] [-u GIT_USERNAME] [-r CREATE_REPOSITORY]
                                 [-v REPOSITORY_VISIBILITY] 

options:
  -h, --help            show this help message and exit
  -t TEMPLATE_DIRECTORY, --template_directory TEMPLATE_DIRECTORY
                        template directory to copy files from
  -p PROJECT_DIRECTORY, --project_directory PROJECT_DIRECTORY
                        destination directory of your scaffolded project
  -l LICENSE, --license LICENSE
                        creates license file (mit, afl-3.0, apache-v2.0)
  -a AUTHOR, --author AUTHOR
                        set name of the author (replaces every instance within the license file)
  -u GIT_USERNAME, --git_username GIT_USERNAME
                        set git username (git config username is used by default)
  -r CREATE_REPOSITORY, --create_repository CREATE_REPOSITORY
                        if set to true, creates a git repository using the git cli tool
  -v REPOSITORY_VISIBILITY, --repository_visibility REPOSITORY_VISIBILITY
                        set git repository visibility (0: private, 1: public, 2: internal)
 
```

```bash
scaffolder > settings view [-h] [-p PARAMETERS]

options:
  -h, --help            show this help message and exit
  -p PARAMETERS, --parameters PARAMETERS
                        
```
