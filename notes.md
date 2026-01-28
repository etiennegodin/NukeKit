

## 

Automated generation of dummy gizmos with params to show worflows 



project_structure/
├── nukekit/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── publisher.py      # Publishing logic
│   │   ├── scanner.py         # Find gizmos in Script/filesystem
│   │   ├── versioning.py      # Version comparison, semver
│   │   └── validator.py       # Gizmo health checks
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py     # PySide2/Qt main interface
│   │   └── widgets.py         # Reusable UI components
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py          # Load settings from JSON/YAML
│   │   ├── logger.py          # Logging setup
│   │   └── paths.py           # Path handling utilities
│   └── data/
│       └── manifest.json      # Published tools registry
├── config/
│   └── settings.yaml          # Repository paths, naming conventions
├── tests/
│   ├── test_versioning.py
│   └── test_scanner.py
├── README.md
├── requirements.txt
└── examples/
    ├── example_gizmo.gizmo
    └── example_usage.py