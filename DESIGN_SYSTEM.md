# Design system — the rules

Read this before building any page that uses `styles.css`. It is written for
people and for models (Claude, the crew) alike.

**The direction:** warm and chocolatey, with orange. Cream pages, chocolate
text, burnt orange for what you act on, and a 70s stripe of gold, orange,
rust and brown. Cards sit lighter than the page with a thin border, so
everything is clearly separated from its background. If a new choice doesn't
feel warm and chocolatey, it is probably off.

## Ground rules

1. **Tokens only.** Every colour, size, space and radius comes from a token in
   `styles.css`. A raw colour outside the token blocks fails the checks.
2. **Use the components below.** If a page needs one that isn't here, build it
   from tokens and say so in the pull request, so it can be added here.
3. **Both themes, always.** Take colours through `var()`, never per theme.
4. **Text is at least 4.5:1** against what it sits on, in both themes. The
   checks prove it for every pair the components use; a new pair goes in
   `checks/check_tokens.py`.
5. **Status is a label and a tone together**, never colour alone.

## Themes

Light is the cream theme, dark the espresso one. `:root` holds the light
values; `data-theme="dark"` on `<html>` swaps every colour token. Each page
puts this in its `<head>`, before the stylesheet, so it never flashes the
wrong theme:

```html
<script>
(function () {
  var t;
  try { t = localStorage.getItem('theme'); } catch (e) {}
  if (t !== 'light' && t !== 'dark') t = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', t);
})();
</script>
```

A saved choice wins; otherwise the page follows the visitor's system. The
theme toggle (below) saves the choice.

## Colour

| Token | Light | Dark | For |
|---|---|---|---|
| `--color-bg` | cream `#F6EFE3` | espresso `#1C1510` | the page |
| `--color-surface` | `#FFFBF4` | `#261C15` | cards, lighter than the page |
| `--color-surface-raised` | `#EFE2CF` | `#33261C` | active nav, avatars, steps not reached |
| `--color-border` | `#E6D8C3` | `#3D2E22` | every border and rule |
| `--color-text` | chocolate `#2E1F14` | `#F3E9DA` | text |
| `--color-text-dim` | `#6B5646` | `#BCA891` | meta, labels, times |
| `--color-link`, `--color-accent` | burnt orange `#A84A16` | `#E08A4A` | links, the one primary action, focus |
| `--color-accent-hover` | `#7E3510` | `#EDA878` | hover |
| `--color-on-accent` | `#FFFBF4` | `#1C1510` | text on the accent |
| `--color-feature-*` | chocolate panel | deeper brown panel | the feature panel |

**Tones** say what a status means. Each is a background and its text:

| Tone | Colour | Board columns | Replay events |
|---|---|---|---|
| `waiting` | sand | Inbox (Goals), Needs Refinement, Ready, Sprint Backlog | — |
| `active` | teal | In Progress, Reviewing, QAing, Merging | Delivered |
| `held` | harvest gold | a story held for the cards it builds on | Returned |
| `done` | avocado | Done | Approved, Merged |
| `blocked` | rust red | Blocked | Blocked, Refused |

Use the board's own words as labels ("In Progress", "QAing"), not new ones.

**Stages** are the path a story takes, deepening as it goes: `--stage-1`
gold, `--stage-2` orange, `--stage-3` burnt orange, `--stage-4` rust,
`--stage-5` brown. Each has a `-text` token for the label on it. The stripe
under the site header is the same colours.

**Roles** have no colours. An agent is its name and its initials; nine roles
can't have nine colours that stay distinct and accessible.

## Type

- **Fraunces** (`--font-display`) for headings: h1, h2, h3, the wordmark.
- **Public Sans** (`--font-sans`) for everything else, **including large
  numbers**: stat values are Public Sans 700, tightened slightly.
- **Numbers that line up** (times, issue numbers, counts in columns) use
  tabular figures: the `.num` class or `font-variant-numeric: tabular-nums`.
- **Mono** (`--font-mono`) is only for real code and tool output, such as a
  file name or an error the crew quoted. Never for numbers, times or IDs.

Sizes: `--text-xs` 13 (meta), `--text-sm` 14, `--text-md` 16 (body),
`--text-lg` 20, `--text-xl` 24, `--text-2xl` 32.

Load the fonts with:

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Public+Sans:wght@400;500;600;700&display=swap">
```

## Space and shape

Spacing is `--space-1` to `--space-9`: 4, 8, 12, 16, 20, 24, 32, 48, 64 px.
Radius is `--radius-sm` 6px (badges, buttons, quotes) and `--radius-md` 8px
(cards, tiles, avatars). Borders do the separating; there are no shadows.

## Components

| Class | What it is |
|---|---|
| `.page` | the page column, max 1080px |
| `.site-header`, `.brand`, `.mark`, `.nav`, `.theme-toggle` | the header, with the stripe under it. The current page's nav link has `aria-current="page"`. The toggle shows the theme it switches *to* |
| `.card`, `.card__head`, `.card__body`, `.card--padded`, `.cards` | cards; a head holds the title and its meta |
| `.stats`, `.stat`, `.stat__value`, `.stat__label` | numbers in a row, split by quiet rules |
| `.path`, `.path__step[data-stage="1…5"]` | the stages a story went through; a step without `data-stage` is not reached yet |
| `.badge[data-tone]` | a status: label and tone |
| `.events`, `.event`, `.event__time`, `.event__text` | a replay's moments, one per row |
| `.agent`, `.avatar`, `.agent__name`, `.quote` | an agent and what it said |
| `.feature`, `.feature__em` | the one chocolate panel on a page, for the point worth making |
| `.btn`, `.btn--primary` | buttons; one primary per view |
| `.code` | code and tool output |
| `.num`, `.meta` | tabular figures; small dim text |

`index.html` shows every one of them with real crew data.

## Don't

- Don't use a colour for a role, or a tone for anything but status.
- Don't put more than one feature panel or one primary button in a view.
- Don't use mono for numbers, or Fraunces for large numbers.
- Don't nest cards; group inside a card with space or `--color-surface-raised`.
- Don't animate layout. Motion is colour only, and off under
  `prefers-reduced-motion`.

## Accessibility

- Text 4.5:1 in both themes, proven by the checks.
- A visible focus ring (the accent) on everything interactive.
- Real `<button>` and `<a href>` elements; icon-only buttons get an
  `aria-label`. Avatars and the mark are decorative (`aria-hidden`), since the
  name beside them carries the meaning.
- Touch targets at least 40px, 44px on phones.

## Open

- **The site's name**, then the wordmark. `[Site name]` until then.
- **The mark.** The Q in a burnt orange square is a placeholder.
