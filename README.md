# Scaffolder

Command Line Interface (CLI) scaffolding tool designed to automatically generate projects using personalized templates. To configure project metadata before its creation, users can define specifications in the `src/scaffolder.json` file.

## Prerequisites

It is recommended to use Python version 3.11 or above. Running `scaffolder.sh` will automatically install all dependencies, unless explicitly declined during the installation process.

The following dependecies will be installed:

- jq - Used to parse JSON data
- gh - Used for repository creation and git authentication

## Installation

1. Clone the git repository:

    ```bash
    git clone https://github.com/soIipsist/scaffolder.git
    ```

2. Install all package dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run `scaffolder.sh`

4. If you're on **Linux** or **Mac**, Create an alias in your .bashrc :

      ```bash
      chmod +x /path-to-release/scaffolder/scaffolder.sh
      alias scaffolder="bash /path-to-release/scaffolder/scaffolder.sh"

      ```

## Usage

### Commands

#### templates

A `template` is the directory that serves as a reference, from which files are copied during the scaffolding process. A reference name is assigned to all templates upon creation. If not specified, the base name of the `destination_directory` will be used as the default.

You can manage templates by adding or deleting them using the `add` and `delete` subcommands respectively.

```bash
scaffolder > templates add [-h] [-t TEMPLATE]
```

```bash
scaffolder > templates delete [-h] [-t TEMPLATE]
```

#### scaffold

Creates a new project using a specified `template` name or directory as a baseline. The resulting project will be scaffolded in a `destination_directory` of your choice, as specified in the `scaffolder.json` settings file. The generated directory will always adopt the base name of the destination_directory.

Users have the flexibility to customize parameters either by directly modifying the file or by providing new values through the CLI. If `create_repository` is set to true, an initialized GitHub repository will be created automatically, with all the main files included in the original `template` directory.

**_Note: All words containing the project's name will be renamed in the default template, including files._**

```bash
scaffolder >  scaffold [-h] [-t TEMPLATE] [-p PROJECT_DIRECTORY] [-l LICENSE] [-a AUTHOR] [-u AUTHOR] [-r CREATE_REPOSITORY] [-v REPOSITORY_VISIBILITY]

options:
  -h, --help                                                               show this help message and exit
  -t TEMPLATE, --template TEMPLATE                                         template name or directory to copy files from
  -p PROJECT_DIRECTORY, --destination_directory PROJECT_DIRECTORY              destination directory of your scaffolded project
  -n REPOSITORY_NAME --repository_name REPOSITORY_NAME      renames all instances of 'repository_name' in your project
  -l LICENSE, --license LICENSE                                            creates license file (mit, afl-3.0, apache-v2.0 etc.)
  -a AUTHOR, --author AUTHOR                                               set name of the author (replaces every instance within the license file)
  -r CREATE_REPOSITORY, --create_repository CREATE_REPOSITORY              if set to true, creates a git repository using the git cli tool (gh)
  -v REPOSITORY_VISIBILITY, --repository_visibility REPOSITORY_VISIBILITY  set git repository visibility (0: private, 1: public, 2: internal)

```

#### update

Updates files in an `update_destination_directory` with those from a `update_template_directory`. The extraction of updated functions is governed by `function_patterns`, specified in the `languages.json` file. By default, Python pattern matching is employed.

```bash
scaffolder > update -h
usage: scaffolder update [-h] [--update_template_directory SOURCE_DIRECTORY] [--update_destination_directory UPDATE_DESTINATION_DIRECTORY] [-f FUNCTION_PATTERNS [FUNCTION_PATTERNS ...]]
                         files [files ...]

positional arguments:
  files                                                                                             Template files to update (must be the same name)

options:
  -h, --help                                                                                        show this help message and exit
  --update_template_directory SOURCE_DIRECTORY                                                               project directory to update from
  --update_destination_directory UPDATE_DESTINATION_DIRECTORY                                                               destination project directory for updated files
  -f FUNCTION_PATTERNS [FUNCTION_PATTERNS ...], --function_patterns FUNCTION_PATTERNS [FUNCTION_PATTERNS ...]

```

#### licenses

The `licenses` command can be used to list all supported software license files. If a valid `license` is specified, its content and/or path will be printed out.

```bash
scaffolder > licenses [-h] [-l LICENSE] [-c show_content] [-p --show_paths]
```

#### settings

View `scaffolder.json` metadata, or manually update a specified parameter.

```bash

scaffolder > settings update [-h] [-t TEMPLATE] [-p PROJECT_DIRECTORY] [-l LICENSE] [-a AUTHOR] [-u AUTHOR] [-r CREATE_REPOSITORY] [-v REPOSITORY_VISIBILITY] 
```

```bash
scaffolder > settings view [-h] [-p PARAMETERS]
```
