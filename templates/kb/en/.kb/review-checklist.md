# Review checklist

The reviewer checks each item and reports the file, the line and the suggested fix.

## Structure

- [ ] The frontmatter has every required field, and the `type` exists in the configuration.
- [ ] The sections follow the type's template, in order.
- [ ] The document is in the right folder: journey in `Journeys/`, standalone rule at the context root, term in `Glossary/`, process part in the parts folder.
- [ ] The document is listed in the folder's `index.md`, with the same description as the frontmatter.

## Content

- [ ] Each fact has a single owner. Nothing repeats another document: link to it.
- [ ] No behavior without a business decision appears as a rule. It is under "To be confirmed".
- [ ] Nothing contradicts another document of the base.
- [ ] Examples are concrete, with values, and show different scenarios.

## Writing

- [ ] Policy comes first. No "If X, the system does Y" sentences.
- [ ] No system, service, queue, endpoint, table or class names.
- [ ] The description does not repeat the content.
- [ ] Name/Description blocks only for values and states. Non-terminal before terminal.
- [ ] No tables, no `#` links, no Citations, no "Where it applies".

## Names

- [ ] The file name is a business name, first letter capitalized, with spaces.
- [ ] A rule's name states the policy.
- [ ] No folder has a system name.

## Journey

- [ ] A person walks the path. A process the business runs on its own is a context, not a journey.
- [ ] Each step has one sentence and at most one link.
- [ ] Every gap is under "Open points".
