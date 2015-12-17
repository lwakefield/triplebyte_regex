- grouping
    - set
        - range
            - alpha: [a-z], [A-Z]
            - numeric: [0-9]
        - [asdf09]
    - subqueries
- quantification
    - ?
    - *
    - +
    - {n}
    - {n, }
    - {n, m}
- boolean

- modifiers
    - DOTALL
    - MULTILINE

# What this can do:

## String Searching

For example finding _ipsum_ in _lorem ipsum dolor sit amet_.

## Quantifying of groups.

For example finding _ipsumipsumipsum_ in _lorem ipsumipsumipsum dolor sit amet_
with the regex `(ipsum)+`.

This supports `+*?` quantifiers. However, it does not support mixing quantifiers
such as `ipsum+?` for greedy/non-greedy mode.

No support yet for ranges `{n,m}`

## Set Patterns

For example finding _my name is Lawrence_ with the regex 
`\my name is [A-Z][a-z]+\`.
Sets are able to contain alphanumeric ranges `[a-z]`, `[A-Z]`, `[0-9]`, sections
of ranges `[f-j]`, mixed ranges `[a-zA-Z0-9]` as well as mixed sets `[a-cD-G13579]`.

## No Support For...

... a lot of things

- Modifiers like DOTALL, MULTILINE.
- Start/End line matches `$`, `^`
- Abstracted patterns like `\w`, `\d`, `\W`, `\s`
- Matching not patterns `[^a-z]`
- Handling special characters, such as new line characters or escaped characters
    - Actually it might, but I haven't tested for this yet

