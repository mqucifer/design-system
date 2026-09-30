# design-system

Design tokens, CSS and components shared by the projects the crew builds.
Its first user is the presentation site: sprint results and replays on
GitHub Pages (crew Discussion #260).

## What's here

- **Tokens:** the design decisions as data (colour, type, spacing, radius,
  motion), the source everything else is built from.
- **CSS:** the tokens as custom properties, and the base styles built on them.
- **Components:** the shared pieces a page is built from.

## The files

| File | What it is |
|---|---|
| `styles.css` | The tokens for both themes, and the components built on them. |
| `DESIGN_SYSTEM.md` | The rules: what each token and component is for, and what not to do. Give it to Claude or the crew before UI work. |
| `index.html` | A preview of every component with real crew data, in both themes. |
| `checks/check_tokens.py` | The rules CI enforces: text contrast of at least 4.5:1 in both themes, every colour in both themes, tokens only in components. |

To preview, open `index.html` beside `styles.css` in a browser.

## How projects use it

- **Versioned by tag** (`vX.Y.Z`). A project pins a release, so a change here
  never alters a site until that site chooses to upgrade.
- **What a release changes is written down.** A token renamed or removed is a
  breaking change: a major version, and the release notes say what replaces it.
- Each project's design decides how it consumes a release, for example a
  tagged CSS file or the tokens as JSON.
- A page links the tagged stylesheet, for example
  `https://cdn.jsdelivr.net/gh/mqucifer/design-system@v0.1.0/styles.css`, with
  the fonts and the theme script from `DESIGN_SYSTEM.md` in its `<head>`.

## Who looks after it

- **The Sponsor, to begin with.** The crew reads it, and doesn't change it.
- **Later, the crew's UX role:** proposing changes by pull request, and
  turning design principles into checks that run in CI (contrast, spacing
  scale, token use) rather than guidance nobody enforces.
