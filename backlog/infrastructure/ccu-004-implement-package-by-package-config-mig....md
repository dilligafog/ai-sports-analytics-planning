---
id: CCU-004
title: Implement Package-by-Package Config Migration
branch_name: ccu-004-implement-package-by-package-config-migration
epic: infrastructure
status: backlog
priority: high
estimate: "8sp"
dependencies: [CCU-003]
labels: [code-cleanup, migration, high-risk]
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

# CCU-004: Implement Package-by-Package Config Migration

## Background
Following the human decision in HUM-CDR-015, we need to implement the package-by-package migration strategy from config.py to config_v2.py. The analysis in CDR-005 series identified 26 affected files organized in logical packages.

## Acceptance Criteria

### Package Migration Requirements
- [ ] **Core config package migration**: Foundation layer migration and validation
  - [ ] Migrate `nfl_data_pipeline/config.py` to `nfl_data_pipeline/config_v2.py` pattern
  - [ ] Update all core config imports across the codebase
  - [ ] Validate core config functionality with comprehensive smoke tests
  - [ ] Ensure backward compatibility during transition period

- [ ] **Data pipeline packages migration**: Dependent package migration
  - [ ] Migrate data ingestion config modules following dependency order
  - [ ] Migrate data processing and transformation config modules
  - [ ] Update pipeline orchestration config references
  - [ ] Validate data pipeline functionality with existing datasets

- [ ] **Models packages migration**: ML/Analytics model configuration
  - [ ] Migrate model training configuration modules
  - [ ] Migrate model evaluation and validation config modules
  - [ ] Update model deployment configuration references
  - [ ] Validate model functionality with test datasets

- [ ] **Scripts and utilities migration**: Supporting tools and utilities
  - [ ] Migrate standalone script configurations
  - [ ] Migrate utility and helper script configurations
  - [ ] Update CLI tool configuration references
  - [ ] Validate script functionality with test executions

### Technical Implementation Requirements
- [ ] **Import pattern migration**: Systematic import updates
  - [ ] Replace `from nfl_data_pipeline.config import create_settings` with `from nfl_data_pipeline.config_v2 import create_settings`
  - [ ] Replace `from nfl_data_pipeline.config import CONFIG_INSTANCE` with `from nfl_data_pipeline.config_v2 import CONFIG_INSTANCE`
  - [ ] Update all relative imports within config modules
  - [ ] Maintain import alias compatibility where needed

- [ ] **Variable naming migration**: Consistent naming conventions
  - [ ] Replace variable name `settings` with `config` throughout codebase
  - [ ] Update function parameters from `settings` to `config`
  - [ ] Update class attributes from `self.settings` to `self.config`
  - [ ] Maintain backward compatibility aliases during transition

- [ ] **Dependency order compliance**: Follow CDR-005 analysis sequence
  - [ ] Migrate packages in dependency order to avoid circular import issues
  - [ ] Validate each package migration before proceeding to dependents
  - [ ] Track migration status and rollback capability per package
  - [ ] Document dependency relationships for future reference

### Validation and Testing Requirements
- [ ] **Package-specific smoke tests**: Comprehensive functionality validation
  - [ ] Create smoke test suite for each migrated package
  - [ ] Test core functionality with both old and new config patterns
  - [ ] Validate configuration loading and parsing for each package
  - [ ] Test error handling and edge cases for configuration issues

- [ ] **Integration testing**: Cross-package compatibility validation
  - [ ] Test interactions between migrated and non-migrated packages
  - [ ] Validate data flow between packages during partial migration
  - [ ] Test configuration inheritance and override patterns
  - [ ] Verify environment-specific configuration handling

- [ ] **Dual repo sync validation**: Safety net verification
  - [ ] Ensure changes sync correctly between development and production repos
  - [ ] Validate configuration compatibility across different environments
  - [ ] Test rollback procedures for each package migration
  - [ ] Verify backup and recovery procedures work correctly

### Audit and Logging Requirements
- [ ] **REFACTOR_AUDIT logging**: Comprehensive migration tracking
  - [ ] Log package migration start/completion with timestamps
  - [ ] Log import pattern changes with before/after examples
  - [ ] Log variable naming changes with affected files
  - [ ] Log any migration failures with detailed error context

- [ ] **Migration documentation**: Detailed change tracking
  - [ ] Document all files modified per package migration
  - [ ] Track configuration changes and their impact
  - [ ] Record any compatibility issues discovered and resolved
  - [ ] Maintain rollback procedures documentation per package

## Implementation Plan

### AI Agent Implementation Notes
**This task has medium complexity** - it involves systematic code refactoring across multiple packages with dependency management. Suitable for AI implementation with careful validation at each step.

### Migration Sequence (Follow CDR-005 Dependency Order)
1. **Core config package** (foundational dependencies)
   - Target files: `nfl_data_pipeline/config.py`, `nfl_data_pipeline/config_v2.py`
   - Dependencies: None (foundation layer)
   - Validation: Core configuration loading and basic functionality

2. **Data pipeline packages** (dependent on core)
   - Target files: Data ingestion, processing, transformation modules
   - Dependencies: Core config package must be completed first
   - Validation: Data pipeline smoke tests with sample datasets

3. **Models packages** (dependent on pipeline)
   - Target files: Model training, evaluation, deployment modules
   - Dependencies: Core config and data pipeline packages
   - Validation: Model functionality tests with test datasets

4. **Scripts and utilities** (least dependencies)
   - Target files: Standalone scripts, CLI tools, utility modules
   - Dependencies: All above packages
   - Validation: Script execution tests and utility function tests

### File Discovery Strategy for AI Agent
```python
# Core config package files
find . -path "*/nfl_data_pipeline/config*" -name "*.py"
find . -path "*/config/*" -name "*.py"

# Data pipeline package files
find . -path "*/data_pipeline/*" -name "*.py"
find . -path "*/ingestion/*" -name "*.py" 
find . -path "*/processing/*" -name "*.py"

# Models package files
find . -path "*/models/*" -name "*.py"
find . -path "*/ml/*" -name "*.py"
find . -path "*/training/*" -name "*.py"

# Scripts and utilities
find . -path "*/scripts/*" -name "*.py"
find . -path "*/bin/*" -name "*.py"
find . -path "*/utils/*" -name "*.py"
```

### Migration Pattern Templates for AI Agent
```python
# Pattern 1: Import Migration
# Before:
from nfl_data_pipeline.config import create_settings, CONFIG_INSTANCE
settings = create_settings()

# After:
from nfl_data_pipeline.config_v2 import create_settings, CONFIG_INSTANCE
config = create_settings()

# Pattern 2: Variable Name Migration  
# Before:
def process_data(settings):
    database_url = settings.database.url
    return settings.api.timeout

# After:
def process_data(config):
    database_url = config.database.url  
    return config.api.timeout

# Pattern 3: Class Attribute Migration
# Before:
class DataProcessor:
    def __init__(self, settings):
        self.settings = settings
        self.db_url = self.settings.database.url

# After:
class DataProcessor:
    def __init__(self, config):
        self.config = config
        self.db_url = self.config.database.url

# Pattern 4: Configuration Access Migration
# Before:
from nfl_data_pipeline.config import settings
result = some_function(settings.api.endpoint)

# After:
from nfl_data_pipeline.config_v2 import config
result = some_function(config.api.endpoint)
```

### Implementation Algorithm for AI Agent
```python
def migrate_package(package_path, package_name):
    """Migrate a single package following established patterns."""
    
    # Step 1: Discover files in package
    python_files = find_python_files(package_path)
    
    # Step 2: Analyze current imports and usage
    for file_path in python_files:
        imports_to_migrate = analyze_config_imports(file_path)
        variables_to_migrate = analyze_config_variables(file_path)
        
        # Step 3: Apply migration patterns
        if imports_to_migrate or variables_to_migrate:
            migrate_file(file_path, imports_to_migrate, variables_to_migrate)
            
            # Step 4: Add REFACTOR_AUDIT logging
            add_migration_logging(file_path, package_name)
    
    # Step 5: Validate package migration
    validate_package_migration(package_path, package_name)
    
    # Step 6: Run package-specific smoke tests
    run_smoke_tests(package_name)

def migrate_file(file_path, imports_to_migrate, variables_to_migrate):
    """Apply migration patterns to a single file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Apply import migrations
    for old_import, new_import in imports_to_migrate:
        content = content.replace(old_import, new_import)
    
    # Apply variable name migrations
    for old_var, new_var in variables_to_migrate:
        content = re.sub(rf'\b{old_var}\b', new_var, content)
    
    # Add REFACTOR_AUDIT logging
    content = add_refactor_audit_logging(content, file_path)
    
    with open(file_path, 'w') as f:
        f.write(content)
```

### Package Migration Checklist for AI Agent
- [ ] **Phase 1: Core Config Package**
  - [ ] Identify all files importing from `nfl_data_pipeline.config`
  - [ ] Update imports to use `nfl_data_pipeline.config_v2`
  - [ ] Replace `settings` variables with `config`
  - [ ] Add REFACTOR_AUDIT logging for core config changes
  - [ ] Validate core config functionality
  - [ ] Run core config smoke tests

- [ ] **Phase 2: Data Pipeline Packages** (depends on Phase 1)
  - [ ] Identify data pipeline files using old config patterns
  - [ ] Apply migration patterns to data ingestion modules
  - [ ] Apply migration patterns to data processing modules
  - [ ] Update pipeline orchestration config references
  - [ ] Validate data pipeline functionality
  - [ ] Run data pipeline smoke tests

- [ ] **Phase 3: Models Packages** (depends on Phase 1,2)
  - [ ] Identify model-related files using old config patterns
  - [ ] Apply migration patterns to model training modules
  - [ ] Apply migration patterns to model evaluation modules
  - [ ] Update model deployment configurations
  - [ ] Validate model functionality
  - [ ] Run model smoke tests

- [ ] **Phase 4: Scripts and Utilities** (depends on Phase 1,2,3)
  - [ ] Identify script and utility files using old config patterns
  - [ ] Apply migration patterns to standalone scripts
  - [ ] Apply migration patterns to CLI tools
  - [ ] Update utility function configurations
  - [ ] Validate script functionality
  - [ ] Run script execution tests

## Technical Details
- Follow the migration pattern established in CDR-008 (backtesting pilot)
- Update imports: `from nfl_data_pipeline.config import create_settings` → `from nfl_data_pipeline.config_v2 import create_settings`
- Update variable naming: `settings` → `config`
- Preserve compatibility patterns for gradual migration
- Add REFACTOR_AUDIT logging as per HUM-CDR-016

### AI Agent Success Criteria
- **Package Isolation**: Successfully migrate one package at a time without breaking others
- **Import Accuracy**: All config imports updated correctly with no missing references
- **Variable Consistency**: All `settings` variables renamed to `config` consistently
- **Dependency Respect**: Migration order follows CDR-005 dependency analysis exactly
- **Validation Passing**: All smoke tests pass for each migrated package

### Validation Commands for AI Agent
```bash
# Check for remaining old import patterns
grep -r "from nfl_data_pipeline.config import" . --include="*.py" | grep -v config_v2

# Check for remaining settings variables (excluding legitimate uses)
grep -r "\bsettings\b" . --include="*.py" | grep -v "django.conf.settings" | grep -v "test_settings"

# Validate Python syntax for all modified files
find . -name "*.py" -type f -exec python -m py_compile {} \;

# Run package-specific smoke tests
python -m pytest tests/smoke/ -k "config_migration" -v

# Check REFACTOR_AUDIT logging was added
grep -r "REFACTOR_AUDIT.*migration" . --include="*.py" | wc -l
```

### Risk Mitigation Strategies for AI Agent
- **Incremental Validation**: Test each package migration before proceeding
- **Rollback Capability**: Track all changes per package for easy rollback
- **Compatibility Preservation**: Maintain backward compatibility during transition
- **Dependency Awareness**: Respect package dependency order strictly

### Error Handling Patterns
```python
# Safe migration with validation
def safe_package_migration(package_name):
    try:
        # Backup current state
        backup_package_state(package_name)
        
        # Perform migration
        migrate_package(package_name)
        
        # Validate migration
        if not validate_package_migration(package_name):
            rollback_package_migration(package_name)
            return False
            
        # Run smoke tests
        if not run_package_smoke_tests(package_name):
            rollback_package_migration(package_name)
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"REFACTOR_AUDIT: Migration failed for {package_name}: {e}")
        rollback_package_migration(package_name)
        return False
```

## Risk Assessment
- **Medium Risk**: Affects multiple packages but isolated by package boundaries
- **Mitigation**: Package-by-package approach allows rollback per package
- **Validation**: Dual repo safety net and smoke tests per package
- **AI-Suitable**: Systematic pattern-based refactoring with clear validation steps
- **Rollback-Safe**: Each package can be independently rolled back if issues arise
