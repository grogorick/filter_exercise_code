# Filter script for exercise code

Annotate your code with simple control keywords to maintain/extract exercise and solution versions of the same code in/from one file.

## Syntax

> `@SOLUTION`  
> \<solution code>  
>
> `@EXERCISE`  
> \<exercise code>  
>
> `@DEV`  
> \<development code>  
>
> `@===` or `@===?`

Respective sections (`@SOLUTION`, `@EXERCISE` or `@DEV`) may appear in any order, each starting with any of these control keywords, and must end with a line containing `@===` or `@===?`.

Lines with control keywords are **always removed entirely** in the output.

You don't have to, for the filter script to work, but to be able to still directly run the annotated development code you will want to put the control keywords in comments.  
Also, most of the time, exercise code sections are best placed in (block) comments.


## Options
(at the beginning of `filter.py`)

`supported` &mdash; File (extensions) that should be processed and the corresponding comment style (for question marks).

`exclude_dirs_that_start_with` &mdash; Exclude sub directories starting with any string from this list.

`exclude_files_that_start_with` &mdash; Exclude files starting with any string from this list.

`_filter_exclude_dirs` and  
`_filter_exclude_files` &mdash; Files to look for in sub directories. If found, they are assumed to contain one string per line that should be added to the corresponding `exclude_*_that_start_with` list for the respective sub directory.


## Running

```
> python filter.py <path/to/source/directory> [exercise | solution]
```

Depending on the second parameter, the following directories will be generated
(if the parameter is omitted, both are generated):
```
path/to/source/directory_exercise
path/to/source/directory_solution
```
If the source directory name ends wtih "`_`" (underscore) the exercise output directory will not be suffixed with `_exercise` but the underscore will be removed:
```
path/to/source/directory
```


## Code annotation examples (Python)
```
—————————————————————————————————————————————————————————————————————————
SOURCE                    -> EXERCISE                  -> SOLUTION
—————————————————————————————————————————————————————————————————————————
```

Remove solution code in exercise files:
```python
# @SOLUTION
solution_code()           ->                           -> solution_code()
# @===
```

Replace solution code with dummy code in exercise files:
```python
# @SOLUTION
solution_code()           -> dummy_code()              -> solution_code()
''' @EXERCISE
dummy_code()
@=== '''
```

Place code in both exercise and solution files:
```python
# @SOLUTION @EXERCISE
'''
non_dev_code()
@=== '''                  -> non_dev_code()            -> non_dev_code()
```

Remove development code in both exercise and solution files:
```python
# @DEV
dev_code()                ->                           ->
# @===
```

Replace development code with actual code in both exercise and solution files:
```python
# @SOLUTION @EXERCISE
actual_code()             -> actual_code()             -> actual_code()
# @DEV
dev_code()
# @===
```

End code sections with `@===?` instead of `@===` to insert question marks in exercise files:
```python
# @SOLUTION               -> #                         -> solution_code()
solution_code()              # ???
# @===?                      #
```
