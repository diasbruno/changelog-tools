# changelogtools [![Build Status](https://travis-ci.org/diasbruno/changelogtools.svg?branch=master)](https://travis-ci.org/diasbruno/changelogtools) [![Coverage Status](https://coveralls.io/repos/github/diasbruno/changelogtools/badge.svg?branch=alpha)](https://coveralls.io/github/diasbruno/changelogtools?branch=alpha)

`changelogtools` is a library to help you build a changelog writer.

## Usage

It only knows the pipeline to when collect information, when to execute the formatter
and concatenate the results. You job is to write the rest of it:

- Give an object that knows how to parse the version name (this can be different from project to project)
- Give a function that know how to retrive information between to tags/revisions.
- Give a function to format all the entries collected to produce the final file.

## Documentation

```python
class Version
```

A base class to your version name parser, it should check if a givef version is valid, 
provides comparison between versions and `__str__` protocol. 
[SemVer](http://semver.org) class is provided. 

If you have a different version name system, you'll just need to write your version class.

```python
class Changelog
```

It's just a proxy class that receive a class and 2 functions:

- `version` is a Version class.
- `delta` a function that knows how to get the information between two versions.
- `formatter` process a log entry and return a string.

```python
changelog(versions=[], changelog=None, tip=False)
```

Receives a list of version names, a changelog object and tip if the first version don't exists.

`tip` tags a version that will be replaced by, for example, `HEAD` on a `git` repository.


### Utils

#### git

```python
git_log(args)
```

Simple git log command.

```python
git_log_between_versions(a, b)
```
Given 2 version, return log between `a` and `b`. If `a` is `tip` use `HEAD`.

```python
git_exec(args)
```

Executes a raw git command.

#### hg

Needs implementation.

## Example

See `self_changelog.py`.

## License

Unlicense.

See `license.md`.
