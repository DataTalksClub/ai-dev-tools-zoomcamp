# Cohorts

The current curriculum — every module and its lesson — lives at the
**repository root**, not here. `cohorts/<year>/` holds only what is specific to
one delivery of the course: dates, homework, and (for a past cohort) a frozen
copy of the curriculum as it was taught that year.

**2026 is the current cohort. Fix curriculum at the repository root, not
inside `cohorts/2026/`.** This is recorded once, machine-readably, at the
root: `course.yaml:current_cohort` names it, and it must match the one
`cohorts/<year>/cohort.yaml` that declares `curriculum: current`.

## Layout

```
<repo root>/
├── course.yaml                   # course identity, incl. the description
├── 01-ai-native-workflow/        # the directory name IS the module slug
│   ├── module.yaml                 # module identity and unit list
│   ├── README.md                   # GitHub-facing module index, not published
│   └── lesson.md                   # the module's unit — the stem IS the unit slug
├── ...
└── cohorts/
    ├── README.md                  # this file
    ├── 2026/                      # the directory name IS the cohort identifier
    │   ├── cohort.yaml            # dates, curriculum: current, homework list
    │   ├── README.md              # the human-readable schedule
    │   └── homework/
    │       ├── 01-ai-native-workflow/
    │       │   ├── homework.md    # homework instructions, fixed name
    │       │   └── homework.yaml  # homework identity, due date, form, questions
    │       └── ...
    └── 2025/                      # earlier cohort: frozen, full copy
```

Two rules carry most of the weight:

- **Names are identity.** The module slug is the directory name. Nothing in
  YAML restates it, and renaming one moves a published URL.
- **A module directory is self-contained.** Its lesson lives inside it, and a
  relative link never climbs past the module directory except into a sibling
  module or the repository root. Anything further away is written as an
  absolute GitHub URL.

## Current cohort vs. frozen cohort

A cohort's `cohort.yaml` says which kind it is:

- **`curriculum: current`** — the cohort teaches whatever is currently at the
  repository root. `cohorts/<year>/` carries only dates and homework
  (`cohorts/<year>/homework/<module>/`); there is no module or lesson content
  here to duplicate or drift from the root.
- **`curriculum: github_archive`** — the cohort's curriculum was materially
  different from what root teaches now, so it was frozen: a full, standalone
  copy of every module it taught. It is kept for GitHub readers only and is
  never re-imported as current module or lesson content. `cohorts/2025/` is
  this repository's only archive so far, retrofitted with a minimal
  `cohort.yaml` after the fact — its interior (module directories, README
  files) is untouched v1-era content, not reshaped to match the current
  convention.

## Note on module 5

`05-agent-capabilities/` exists at the repository root with real content, but
has no `module.yaml` and is not part of `cohorts/2026/`'s curriculum yet. This
is deliberate for now, mirroring the same open item in `machine-learning-zoomcamp`
(its `11-kserve/`): a numbered root directory without a `module.yaml` is
simply not discovered as part of the curriculum. Wiring it in (or moving it
out of the numbered-module namespace) is a separate decision.

## Editing

- Fix curriculum content (the lesson) at the **repository root**. That is
  where pull requests for the current cohort are accepted.
- Fix dates or homework for the current cohort under `cohorts/2026/`.
- The frozen `cohorts/2025/` is an archive: the drift is the record of what
  was actually taught. Backport only factual or breaking errors, explicitly.
- A published slug is frozen. Renaming one is a platform decision, not a
  repository pull request.

## The conventions themselves

This repository does not restate them. `DataTalksClub/zoomcamp-ops` is the
authority: `STRUCTURE.md` for the repository layout and
`docs/shared-curriculum-v2.md` for the shared-root schema this repository
follows, plus the curriculum contract documented beside it for the YAML
schemas and the unit page rules.

The website's ingestion parser is the final authority and fails loudly on push.
