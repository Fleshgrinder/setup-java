<div align="center">
  <h1>
    <img src=".idea/icon.svg" height="64" alt="Java Duke Logo">
    <br>
    Setup Java
  </h1>
  <p><b>Automatic Java Setup</b></p>
</div>

[![GitHub Workflow](https://img.shields.io/github/workflow/status/fleshgrinder/setup-java/Test/main)](https://github.com/fleshgrinder/setup-java/actions)
[![Code Coverage](https://img.shields.io/codecov/c/github/fleshgrinder/setup-java)][CodeCov]

This is [actions/setup-java] with sensible defaults that can be changed globally, `.java-version` file support
(resolving [#113]), and automatic architecture mapping (resolving [#375]). I created this action, because I am not a
fan of copying and pasting things from one project to another, especially not when it comes to workflow automation.

## Usage

The example assumes that you have a `.java-version` file and are fine with the defaults:

```yaml
jobs:
  example:
    runs-on: ubuntu-latest # All OS are supported!
    steps:
    - uses: actions/checkout@main        # replace @main with desired version
    - uses: fleshgrinder/setup-java@main # replace @main with desired version
    - run: java -version                 # 🎉
```

The version that was resolved is **always** exported as `JAVA_VERSION` to the environment. Subsequent steps can use it
to autoconfigure themselves (e.g. Gradle toolchain to use `JAVA_VERSION` if present, with a fallback to the checked in
`.java-version` file).

This action provides the ability to alter the defaults that have been chosen. This is especially useful for all users
of self-hosted runners. Simply include any of the following environment variables in your self-hosted runner to set the
default values for all your workflows:

| Variable                        | Description                                                                                                 |
|---------------------------------|-------------------------------------------------------------------------------------------------------------|
| `JAVA_DEFAULT_VERSION`          | Version to use if nothing else is present                                                                   |
| `JAVA_DEFAULT_VERSION_FILENAME` | Change the `.java-version` default                                                                          |
| `JAVA_DEFAULT_DISTRIBUTION`     | Change the `temurin` default                                                                                |
| `JAVA_DEFAULT_ARCHITECTURE`     | Disable the `$RUNNER_ARCH` mapping, can be used to add support for architectures that are not yet supported |
| `JAVA_DEFAULT_PACKAGE_TYPE`     | Change the `jdk` default                                                                                    |
| `JAVA_DEFAULT_CHECK_LATEST`     | Change the `false` default                                                                                  |

## Project Info

- Contributions are highly appreciated, see [CONTRIBUTING.md] for details.
- We use [semantic versioning] and [keep a changelog], available versions and changes are listed on our [releases] page.
- The [Duke logo](.idea/icon.svg) – the Java mascot – is taken from [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Duke_(Java_mascot)_waving.svg)
  where it is available under a BSDu license. I optimized the logo with [svgo](https://github.com/svg/svgo), that is all, it is not my work, and it is not
  made available under the project’s license.

<!-- @formatter:off -->
[#113]: https://github.com/actions/setup-java/issues/113
[#375]: https://github.com/actions/setup-java/issues/375
[CONTRIBUTING.md]: https://github.com/fleshgrinder/.github/blob/main/CONTRIBUTING.md
[CodeCov]: https://codecov.io/gh/fleshgrinder/setup-java
[actions/setup-java]: https://github.com/actions/setup-java
[keep a changelog]: https://keepachangelog.com/
[releases]: https://github.com/fleshgrinder/setup-java/releases
[semantic versioning]: http://semver.org/
