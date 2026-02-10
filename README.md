# NukeKit

> Version control system for Nuke Gizmos and Scripts

## Features

- Semantic versioning for Nuke assets
- Publish/install workflow
- Changelog tracking
- Centralized asset repository
- CLI and _GUI*_ interfaces


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
nukekit scan local

# Scan remote repository
nukekit scan remote
```

## Project Structure
```
NukeKit/
├── src/nukekit/
│   ├── core/          # Business logic
│   ├── ui/            # GUI components  
│   ├── utils/         # Utilities
│   └── cli.py         # CLI entry point
├── test/              # Test suite
├── config/            # Default configs
└── examples/          # Example assets
```

