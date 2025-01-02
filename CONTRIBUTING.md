# Contributing to baribal

Thank you for your interest in contributing to baribal! This document provides git commit guidelines to ensure consistency in our repository.

## Git Commit Conventions

We follow a modified version of the [Conventional Commits](https://www.conventionalcommits.org/) specification with added emojis for better readability.

### Commit Message Structure
```
<type>(<scope>): <emoji> <description>

[optional body]

[optional footer(s)]
```

### Types and Emojis

| Type     | Emoji | Description                          | Example |
|----------|-------|--------------------------------------|---------|
| feat     | ✨    | New feature                          | `feat(core): ✨ add glimpse() function` |
| fix      | 🐛    | Bug fix                             | `fix(display): 🐛 correct type alignment` |
| refactor | ♻️    | Code change that neither fixes a bug nor adds a feature | `refactor(core): ♻️ optimize type formatting` |
| test     | 🧪    | Adding/updating tests                | `test(core): 🧪 add polars DataFrame tests` |
| docs     | 📚    | Documentation only changes           | `docs: 📚 add usage examples` |
| style    | 💄    | Code style/formatting               | `style: 💄 apply black formatting` |
| chore    | 🔧    | Build, dependencies, config changes  | `chore(deps): ⬆️ upgrade polars` |

### Guidelines

1. **First line (subject)**
   - Maximum 72 characters
   - No period at the end
   - Use present tense ("add" not "added")
   - Use imperative mood ("move cursor" not "moves cursor")

2. **Body (optional)**
   - Separate from subject with a blank line
   - Explain what and why vs. how
   - Can use multiple paragraphs
   - Wrap at 72 characters

3. **Footer (optional)**
   - Reference issues and PRs
   - One issue reference per line
   - Can use multiple lines

### Examples

#### Simple feature
```
feat(core): ✨ add support for polars DataFrame
```

#### Bug fix with description
```
fix(display): 🐛 correct type column alignment

Previous alignment was inconsistent when mixing different 
type lengths (date, int, etc.). Now all types are displayed 
with exactly 3 characters.

Fixes #123
```

#### Documentation update with multiple changes
```
docs: 📚 improve function documentation

- Add more examples for glimpse()
- Update type descriptions
- Include polars usage examples

Related to #456
```

### Initial Commit Structure
The initial commit of a new feature or module should follow:
```
chore(init): 🎉 initial project setup

- Configure project structure with pyproject.toml
- Setup development tools (ruff, pytest)
- Add basic documentation
- Configure GitHub workflows
```

### Pull Requests

1. Create a branch with a descriptive name: `feat/glimpse-function` or `fix/type-alignment`
2. Follow commit guidelines for all commits in the PR
3. Keep commits atomic and focused
4. Rebase on main before requesting review
5. Update documentation if needed

## Questions?

Feel free to open an issue if you have questions about these conventions.