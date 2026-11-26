# Writing style

## Rules

- **Policy first, effect after.** Example: "The delivery time is always at least 1 day. A zero delivery time sent by the supplier is ignored."
  - Never write "If X, the system does Y". That describes the mechanism, not the business decision.
- **Business language.** No system, service, queue, endpoint, table, class or data format names.
  - Test: if the system were rewritten tomorrow in another technology, would the sentence still be true?
  - An external provider may appear as an example, in parentheses.
- **Short sentences, one idea per sentence, active voice.**
- **One name for each thing.** Always use the glossary term.
- **The frontmatter description says what the document is about.** It does not repeat the content.
- **Behavior nobody decided** goes in a "To be confirmed" section or item, never as a rule.
- **No level disclaimers**, such as "high-level overview". The base is always high level.

## Name/Description blocks

- Use them only for **values and states** (e.g. approved, refused, under review).
- Never for behavior, impact, fields or points of attention. Those go in a list or in prose.
- Format, with bold labels:

```
**Name:** Approved
**Description:** The review finished without finding any problem in the order.
```

- **Non-terminal states always come before terminal ones.** The groups are called "Non-terminal statuses" and "Terminal statuses", or "Non-terminal states" and "Terminal states" in terms.

## Format

- **No tables** in terms, rules and process parts.
- **Links always to the file**, never to a heading (`file.md#heading`).
- **Relative markdown links**, with encoded spaces (`%20`).
- **No "Citations" or "Where it applies" sections.** To see where a rule applies, look at the backlinks.
- **Frontmatter:** unquoted text cannot contain ": " (colon followed by space). It breaks the YAML.
