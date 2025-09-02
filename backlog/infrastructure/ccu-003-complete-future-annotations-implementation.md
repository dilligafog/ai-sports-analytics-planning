---
id: CCU-003
title: Complete Future Annotations Implementation
branch_name: ccu-003-complete-future-annotations-implementation
epic: infrastructure
status: backlog
priority: high
estimate: "1sp"
dependencies: [CCU-002]
labels: [code-cleanup, annotations, simple]
created: "2025-09-01"
author: planning-agent
owner: ""
market: null
layer: null
last_updated: "2025-09-01"
emit_metadata:
  source_id: null
  layer: null
  input_path: null
  notes: null
---

# CCU-003: Complete Future Annotations Implementation

## Background
Following the pattern established in CDR-001 through CDR-004, we need to complete adding `from __future__ import annotations` to any remaining files that don't have it yet. The initial implementation covered test files and some core files, but a comprehensive sweep may be needed.

## Acceptance Criteria

### Functional Requirements
- [ ] **File discovery and analysis**: Comprehensive identification of missing future annotations
  - [ ] Scan all Python files (.py) in the codebase recursively
  - [ ] Identify files missing `from __future__ import annotations`
  - [ ] Exclude files where future annotations would cause issues (Python < 3.7 compatibility files)
  - [ ] Generate report of files requiring modification before making changes

- [ ] **Future annotations implementation**: Standardized import addition
  - [ ] Add `from __future__ import annotations` as the very first import line
  - [ ] Maintain exactly one blank line after future import before other imports
  - [ ] Preserve all existing import structure, order, and spacing
  - [ ] Handle edge cases: files with only docstrings, comments, or encoding declarations

- [ ] **Code structure preservation**: Maintain existing file formatting
  - [ ] Preserve file encoding declarations (# -*- coding: utf-8 -*-)
  - [ ] Maintain module docstrings in correct position (after future imports)
  - [ ] Keep existing import grouping (standard, third-party, local)
  - [ ] Preserve any existing `# noqa` or type ignore comments

- [ ] **Syntax and compatibility validation**: Ensure all changes are valid
  - [ ] Validate Python syntax for all modified files using `python -m py_compile`
  - [ ] Confirm future annotations import is detected as first import
  - [ ] Verify no duplicate future annotations imports are created
  - [ ] Test that type hints still work correctly after modification

### Technical Requirements
- [ ] **File categorization**: Systematic coverage of all file types
  - [ ] Process test files not covered in CDR-001 (`test_*.py`, `*_test.py`)
  - [ ] Process core package files not covered in CDR-004 (`src/`, `lib/`, main packages)
  - [ ] Process utility and script files (`scripts/`, `bin/`, `tools/`)
  - [ ] Process configuration and setup files (`setup.py`, `conftest.py`)

- [ ] **Implementation consistency**: Follow established patterns
  - [ ] Use exact pattern from CDR-001 implementation
  - [ ] Maintain consistent spacing and formatting across all files
  - [ ] Follow project's existing import ordering standards
  - [ ] Preserve any existing future imports (don't duplicate)

### Quality Assurance
- [ ] **Automated validation**: Comprehensive testing of changes
  - [ ] Run `python -m py_compile` on all modified files
  - [ ] Use AST parsing to validate Python syntax correctness
  - [ ] Verify future annotations import appears on correct line (after encoding/docstring)
  - [ ] Test that existing functionality remains unchanged

- [ ] **Change tracking**: Document all modifications
  - [ ] Generate list of all files modified with line counts
  - [ ] Report any files skipped and reasons why
  - [ ] Confirm no functional code changes beyond import addition
  - [ ] Validate that import order follows project standards (isort/black compatibility)

### Error Handling & Edge Cases
- [ ] **Special file handling**: Manage non-standard Python files
  - [ ] Handle files with existing `__future__` imports (don't duplicate)
  - [ ] Skip files with Python version compatibility requirements
  - [ ] Process files with complex encoding declarations correctly
  - [ ] Handle files with only comments or empty files appropriately

- [ ] **Rollback preparation**: Ensure changes can be undone
  - [ ] Track all files modified for potential rollback
  - [ ] Verify git diff shows only expected import additions
  - [ ] Ensure no unintended whitespace or formatting changes
  - [ ] Test that reverting changes restores original functionality

## Implementation Details

### AI Agent Implementation Notes
**This task is perfect for automated implementation** - it involves simple, repetitive pattern matching and file modification with well-defined rules and validation steps.

### File Discovery Strategy for AI Agent
1. **Python File Identification**: Recursively find all Python files
   ```bash
   find . -name "*.py" -type f | grep -v __pycache__ | grep -v .git
   ```

2. **Future Annotations Detection**: Check for existing import
   ```python
   import ast
   import re
   
   def has_future_annotations(file_content):
       """Check if file already has future annotations import."""
       return "from __future__ import annotations" in file_content
   
   def needs_future_annotations(file_path):
       """Determine if file needs future annotations added."""
       with open(file_path, 'r') as f:
           content = f.read()
       
       # Skip if already has future annotations
       if has_future_annotations(content):
           return False
           
       # Skip if file is empty or only comments
       try:
           tree = ast.parse(content)
           return len(tree.body) > 0  # Has actual code
       except SyntaxError:
           return False  # Skip files with syntax errors
   ```

### Implementation Pattern Templates
```python
# Pattern 1: File with only imports
# Before:
import os
import sys
from typing import Dict

# After:
from __future__ import annotations

import os
import sys
from typing import Dict

# Pattern 2: File with encoding and imports
# Before:
# -*- coding: utf-8 -*-
import os

# After:
# -*- coding: utf-8 -*-
from __future__ import annotations

import os

# Pattern 3: File with docstring
# Before:
"""Module docstring."""
import os

# After:
"""Module docstring."""
from __future__ import annotations

import os

# Pattern 4: File with shebang and encoding
# Before:
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module docstring."""
import os

# After:
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module docstring."""
from __future__ import annotations

import os
```

### Implementation Algorithm for AI Agent
```python
def add_future_annotations(file_path):
    """Add future annotations import to a Python file."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find insertion point
    insert_line = 0
    
    # Skip shebang
    if lines and lines[0].startswith('#!'):
        insert_line = 1
    
    # Skip encoding declaration
    if len(lines) > insert_line and 'coding' in lines[insert_line]:
        insert_line += 1
    
    # Skip module docstring
    if len(lines) > insert_line:
        try:
            first_stmt = ast.parse(''.join(lines[insert_line:])).body[0]
            if isinstance(first_stmt, ast.Expr) and isinstance(first_stmt.value, ast.Str):
                # Find end of docstring
                for i, line in enumerate(lines[insert_line:], insert_line):
                    if '"""' in line or "'''" in line:
                        insert_line = i + 1
                        break
        except:
            pass
    
    # Insert future annotations import
    future_import = "from __future__ import annotations\n"
    if insert_line < len(lines) and lines[insert_line].strip():
        future_import += "\n"  # Add blank line before other imports
    
    lines.insert(insert_line, future_import)
    
    # Write back to file
    with open(file_path, 'w') as f:
        f.writelines(lines)
```

### Implementation Checklist for AI Agent
- [ ] Scan codebase for all Python files (.py extension)
- [ ] Filter out files that already have future annotations import
- [ ] Filter out __pycache__, .git, and other non-source directories
- [ ] For each target file:
  - [ ] Parse file structure to find correct insertion point
  - [ ] Add future annotations import at the proper location
  - [ ] Preserve all existing formatting and structure
  - [ ] Validate syntax with `python -m py_compile`
- [ ] Generate summary report of all files modified

### File Categories to Check
- [ ] Remaining test files not covered in CDR-001
- [ ] Core package files not covered in CDR-004
- [ ] Script files and utilities
- [ ] Any new files added since CDR-001 completion

### Implementation Pattern (from CDR-001)
```python
# Before:
from some_module import something

# After:
from __future__ import annotations

from some_module import something
```

### Validation Steps
- [ ] Syntax validation with `python -m py_compile`
- [ ] AST parsing confirms valid Python syntax
- [ ] Future annotations import detected as first import (line 1)
- [ ] Import order follows project standards

## Technical Details
- Use established pattern from CDR-001 implementation
- Focus on files that don't already have the import
- Maintain existing code structure and formatting
- Batch process for efficiency

### AI Agent Success Criteria
- **File Detection**: Successfully identify all Python files missing future annotations
- **Pattern Recognition**: Correctly handle different file structures (shebang, encoding, docstrings)
- **Syntax Preservation**: No syntax errors introduced in any modified files
- **Consistency**: All modifications follow the exact same pattern

### Validation Commands for AI Agent
```bash
# Validate all modified files compile correctly
find . -name "*.py" -type f -exec python -m py_compile {} \;

# Check that future annotations were added correctly
grep -r "from __future__ import annotations" . --include="*.py" | wc -l

# Verify no duplicate future imports were created
grep -r "from __future__ import annotations" . --include="*.py" | \
  cut -d: -f1 | sort | uniq -d

# Check syntax of all Python files
python -m compileall . -q
```

### Error Prevention Strategies
- **Duplicate Detection**: Skip files that already have future annotations
- **Encoding Handling**: Properly handle files with encoding declarations
- **Syntax Validation**: Test each file after modification
- **Rollback Capability**: Track all changes for potential reversal

## Risk Assessment
- **Very Low Risk**: Simple import addition only
- **No Breaking Changes**: Code functionality unchanged  
- **Standards Compliance**: Follows pattern from existing codebase files
- **AI-Perfect**: Highly repetitive task ideal for automated implementation
- **Easily Validated**: Simple checks confirm successful completion
