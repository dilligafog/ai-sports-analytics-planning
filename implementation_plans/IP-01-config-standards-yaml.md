# INF-001 Implementation Plan - Configuration standards (YAML + pydantic)

## Overview
- **Story Reference**: [INF-001](../backlog/llm/infra/01-config-standards-yaml.md)
- **Epic**: llm_backlog
- **Estimated Effort**: 2 story points
- **Timeline**: 1 week with 2 phases
- **Priority**: Medium

## Technical Approach
- **Architecture**: Centralized configuration system with pydantic validation, YAML files for human-readable configs, and environment variables for secrets
- **Technology Stack**:
  - `pydantic-settings` for configuration management
  - PyYAML for YAML parsing
  - python-dotenv for environment variable management
  - pre-commit hooks for validation
  - Click for CLI validation commands
- **Integration Points**:
  - All data source configurations
  - Model training parameters
  - LLM pipeline settings
  - Infrastructure deployment configs
- **Data Flow**: YAML configs + env vars → Pydantic validation → Application settings → Runtime configuration

## Implementation Phases

### Phase 1: Core Configuration Framework
**Deliverables:**
- Pydantic settings models for all major components
- YAML configuration structure under `config/`
- Environment variable handling with `.env.example`
- Basic CLI validation command

**Story Points**: 1.5
**Dependencies**: None
**Technical Tasks:**
- Define pydantic models for news sources, teams, models, and infrastructure
- Create hierarchical configuration structure in `config/` directory
- Implement environment variable overrides using pydantic-settings
- Create `.env.example` with all required environment variables
- Implement basic `busta config doctor` CLI command

### Phase 2: Validation, Versioning & Developer Tools
**Deliverables:**
- Schema versioning for critical configurations
- Pre-commit hooks for YAML validation
- Comprehensive error messages and documentation
- Configuration migration tools

**Story Points**: 0.5
**Dependencies**: Phase 1 completion
**Technical Tasks:**
- Add schema versioning for news sources and team configurations
- Set up pre-commit hooks with YAML linting and validation
- Enhance `config doctor` with detailed error reporting
- Create configuration documentation and examples
- Implement configuration migration scripts

## Technical Decisions

### Configuration Format Decision
**Choice**: YAML for human-editable configs, environment variables for secrets
**Rationale**:
- YAML is human-readable and supports comments
- Environment variables prevent secrets in version control
- Pydantic provides type safety and validation
**Alternatives Considered**: TOML (less familiar), JSON (no comments), pure Python (security concerns)

### Settings Management Decision
**Choice**: pydantic-settings with hierarchical configuration
**Rationale**:
- Type safety with automatic validation
- Environment variable override support
- Good integration with FastAPI and other frameworks
- Automatic documentation generation
**Alternatives Considered**: python-decouple (less feature-rich), custom solution (more work)

### Schema Versioning Decision
**Choice**: Version critical configs with migration scripts
**Rationale**:
- Prevents breaking changes during system evolution
- Enables backward compatibility
- Clear upgrade path for configuration changes
**Alternatives Considered**: No versioning (risky), database-style migrations (overkill)

## Risks and Mitigation

### Risk: Configuration Drift Between Environments
**Impact**: Medium - Inconsistent behavior across environments
**Likelihood**: Medium
**Mitigation**:
- Standardized configuration templates
- Environment-specific validation in CI/CD
- Clear documentation of environment differences
- Automated configuration comparison tools

### Risk: Secrets Accidentally Committed to Version Control
**Impact**: High - Security vulnerability
**Likelihood**: Low
**Mitigation**:
- Pre-commit hooks to scan for potential secrets
- Clear separation of config files and secret files
- `.gitignore` rules for sensitive files
- Training and documentation on proper secret handling

### Risk: Configuration Validation Performance Impact
**Impact**: Low - Slower application startup
**Likelihood**: Medium
**Mitigation**:
- Cache validated configurations
- Lazy loading for non-critical settings
- Profile configuration loading times
- Optimize validation rules for performance

## Success Criteria

### Functional Requirements
- All configurations live under `config/` with pydantic validation
- No secrets stored in YAML files (environment variables only)
- `busta config doctor` validates all configurations and reports clear errors
- Pre-commit hooks prevent invalid configurations from being committed

### Non-functional Requirements
- Configuration validation completes in < 1 second
- Clear error messages for all validation failures
- Configuration files are self-documenting with examples
- Zero configuration drift between development and production environments

### Testing Strategy
- Unit tests for all pydantic models (100% coverage)
- Integration tests for environment variable overrides
- Validation tests for all sample configurations
- Pre-commit hook testing in CI/CD pipeline

## Follow-up Work

### Immediate Follow-ups (Next Sprint)
- Configuration hot-reloading for development
- Configuration backup and restore tools
- Environment-specific configuration templates

### Technical Debt Considerations
- Regular review of configuration schema for unused settings
- Performance monitoring for configuration validation
- Documentation updates as system evolves

### Future Enhancements
- Web UI for configuration management
- Configuration audit logging
- Dynamic configuration updates without restart
- Configuration template generation from code

## Implementation Structure

```python
# Example pydantic settings model
class NewsSourceConfig(BaseSettings):
    name: str
    url: str
    enabled: bool = True
    fetch_interval: int = 3600  # seconds
    max_articles: int = 100
    
    class Config:
        env_prefix = "NEWS_"

class DatabaseConfig(BaseSettings):
    host: str
    port: int = 5432
    name: str
    user: str
    password: str = Field(..., env="DB_PASSWORD")
    
    class Config:
        env_file = ".env"

# CLI validation command
@click.command()
def config_doctor():
    """Validate all configuration files"""
    try:
        settings = load_all_settings()
        click.echo("✅ All configurations valid")
    except ValidationError as e:
        click.echo(f"❌ Configuration errors:\n{e}")
        sys.exit(1)
```

## File Structure

```
config/
├── news_sources.yml      # News RSS feed configurations
├── teams.yml            # Team identifiers and mappings
├── models.yml           # Model training parameters
├── infrastructure.yml   # Deployment and runtime settings
└── runtime.yml          # Application runtime configuration

.env.example             # Template for environment variables
.env                     # Local environment (gitignored)
```

## Configuration Examples

```yaml
# config/news_sources.yml
version: "1.0"
sources:
  - name: "espn_nfl"
    url: "https://www.espn.com/espn/rss/nfl/news"
    enabled: true
    fetch_interval: 1800
    max_articles: 50
    
  - name: "nfl_official"
    url: "https://www.nfl.com/feeds/rss/news"
    enabled: true
    fetch_interval: 3600
    max_articles: 25
```