# NukeKit

> Version control system for Nuke Gizmos and Scripts

## Features

- Semantic versioning for Nuke assets
- Publish/install workflow
- Changelog tracking
- Centralized asset repository
- CLI interface


## Installation

```bash
pip install nukekit
```

## Quick start

### Setup repository
```bash
# Configure your repository location
export NUKEKIT_REPO_ROOT="$HOME/nukekit_repo"
```

### Publishing a Gizmo
```bash
# Publish from Nuke directory
nukekit publish

# Or publish from current directory
nukekit publish --local
```
### Installing assets
```bash
nukekit install
```

### Scanning
```bash
# Scan local Nuke directory
nukekit scan 

# Scan remote repository 
nukekit scan remote 
```

```bash
INFO: Starting scan workflow
INFO: Scan found 10 assets
Found 10 assets
                    Assets (remote)                     
┏━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Name     ┃ Type  ┃ Versions                          ┃
┡━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ tool     │ Gizmo │ 0.3.0, 0.2.0, 0.1.0               │
│ my_gizmo │ Gizmo │ 2.0.0, 1.0.0, 0.2.0, 0.1.0, 0.0.0 │
│ my_cool  │ Gizmo │ 0.1.0, 0.0.0                      │
└──────────┴───────┴───────────────────────────────────┘
```

## Configuration
Edit `~/.nukekit/config.yaml`:
```yaml
repository:
  root: "${HOME}/nukekit_repo"
  subfolder:
    - Gizmo
    - Script

user:
  nuke_dir: "~/.nuke"

```
