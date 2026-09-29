# design-system

Design tokens, CSS and components shared by the projects the crew builds.
Its first user is the presentation site: sprint results and replays on
GitHub Pages (crew Discussion #260).

## What's here

- **Tokens:** the design decisions as data (colour, type, spacing, radius,
  motion), the source everything else is built from.
- **CSS:** the tokens as custom properties, and the base styles built on them.
- **Components:** the shared pieces a page is built from.

## How projects use it

- **Versioned by tag** (`vX.Y.Z`). A project pins a release, so a change here
  never alters a site until that site chooses to upgrade.
- **What a release changes is written down.** A token renamed or removed is a
  breaking change: a major version, and the release notes say what replaces it.
- Each project's design decides how it consumes a release, for example a
  tagged CSS file or the tokens as JSON.

## Who looks after it

- **The Sponsor, to begin with.** The crew reads it, and doesn't change it.
- **Later, the crew's UX role:** proposing changes by pull request, and
  turning design principles into checks that run in CI (contrast, spacing
  scale, token use) rather than guidance nobody enforces.
