# Filter script for exercise code

Annotate your code with simple control statements to maintain/extract exercise and solution versions of the same code in/from one file.

## Syntax

> `@EXERCISE`  or  `@==`  
> \<solution code>  
>
> `==>`  
> \<exercise code>  
>
> `== ==`  
> \<test code>  
>
> `===` or `<==`

You don't have to, for the filter script to work, but to be able to still directly run the annotated code you will want to put the control statements (`@EXERCISE` / `@==` / `==>` / `== ==` / `===` / `<==`) in comments.

Lines with control statements are **always removed entirely** in the output.


## Options
(at the beginning of `filter.py`)

`supported` &mdash; File (extensions) that should be processed and the corresponding comment style (for question marks).

`exclude_dirs_that_start_with` &mdash; Exclude sub directories starting with any string from this list.

`exclude_files_that_start_with` &mdash; Exclude files starting with any string from this list.

`_filter_exclude_dirs` and  
`_filter_exclude_files` &mdash; Files to look for in sub directories. If found, they are assumed to contain one string per line that should be added to the corresponding `exclude_*_that_start_with` list for the respective sub directory.


## Running

```
> python filter.py <path/to/source/directory_> [exercise | solution]
```

Depending on the second parameter, the following directories will be generated
(if the parameter is omitted, both are generated):
```
path/to/source/directory            (exercise)
path/to/source/directory_solution   (solution)
```

Note that the source directory name is assumed to end with an **underscore**, e.g. `path/to/code01_/`.


## Code annotation examples (Python)
```
SOURCE                    -> EXERCISE                  -> SOLUTION
```

Remove solution code in exercise files:
```
# @EXERCISE               ->                           -> solution_code()
solution_code()
# ===
```

Replace solution code with dummy code in exercise files:
```
# @EXERCISE               -> dummy_code()              -> solution_code()
solution_code()
''' ==>
dummy_code()
''' # ===
```

Place code in both exercise and solution files:
```
# @EXERCISE ==>           -> non_dev_code()            -> non_dev_code()
'''
non_dev_code()
''' # ===
```

Remove code in both exercise and solution files:
```
# @EXERCISE == ==         ->                           ->
dev_code()
''' # ===
```

Replace dev code with actual code in both exercise and solution files:
```
# @EXERCISE ==>           -> actual_code()             -> actual_code()
actual_code()
# == ==
dev_code()
# ===
```

Append question marks in exercise files with `<==` instead of `===` at the end:
```
# @EXERCISE               -> #                         -> solution_code()
solution_code()              # ???
# <==                        #
```
