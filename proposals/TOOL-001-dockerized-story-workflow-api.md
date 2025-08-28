# Proposal: TOOL-001 - Dockerized Story Workflow Management API

## Summary
Create a containerized REST API service that provides programmatic access to story lifecycle management, reporting, and file system operations for the AI Sports Analytics planning repository. This tool would complement the existing file-based workflow with web-based automation capabilities.

## Motivation
Currently, story management requires manual file operations and script execution. While the folder-based organization provides excellent visibility, there's a need for:
- **Automated Story Operations**: Programmatic creation, updates, and transitions
- **Advanced Reporting**: Cross-epic analytics, velocity tracking, and dependency visualization  
- **Integration Capabilities**: API endpoints for CI/CD workflows and external tools
- **Data Export/Import**: Bulk operations and backup/restore functionality
- **Real-time Monitoring**: Live status updates and notification systems

This API service would provide these capabilities while preserving the existing file-based structure that stakeholders prefer.

## Proposed Changes

### Core Architecture
- **Containerized FastAPI Service**: Python-based REST API with automatic OpenAPI documentation
- **PostgreSQL Database**: Synchronized with file system for performance and advanced queries
- **File System Sync**: Two-way synchronization between database and markdown files
- **Docker Compose Stack**: Complete development and production environment
- **Authentication Layer**: API key-based access control for operations

### Key Features
- **Story CRUD Operations**: Create, read, update, delete stories via REST endpoints
- **Lifecycle Management**: Automated status transitions with validation rules
- **Advanced Reporting**: Analytics dashboards, velocity metrics, dependency graphs
- **Export/Import Tools**: JSON, CSV, and markdown bulk operations
- **File System Bridge**: Maintain compatibility with existing folder structure
- **Real-time Updates**: WebSocket notifications for status changes

## Acceptance Criteria
- [ ] Docker container runs PostgreSQL database with story schema
- [ ] FastAPI service exposes REST endpoints for all story operations
- [ ] Two-way sync between database and markdown files (max 30 second delay)
- [ ] API endpoints for story creation, updates, status transitions, and queries
- [ ] Advanced reporting endpoints with epic analytics and velocity tracking
- [ ] Bulk export/import functionality for JSON and CSV formats
- [ ] Authentication middleware with API key management
- [ ] OpenAPI documentation with interactive testing interface
- [ ] Docker compose setup for local development and production deployment
- [ ] Existing file-based workflow continues to work unchanged
- [ ] Real-time WebSocket updates for story status changes
- [ ] Comprehensive logging and error handling

## Suggested Stories

### Core Infrastructure (Epic: infrastructure)
- **INF-011**: Docker PostgreSQL database setup with story schema
- **INF-012**: FastAPI service framework with basic CRUD endpoints
- **INF-013**: File system synchronization service
- **INF-014**: Authentication and API key management

### API Development (Epic: api)
- **API-001**: Story management endpoints (CRUD operations)
- **API-002**: Status transition endpoints with validation
- **API-003**: Advanced query endpoints (filtering, searching, aggregation)
- **API-004**: Bulk operations endpoints (import/export)

### Reporting & Analytics (Epic: reporting)
- **RPT-001**: Epic analytics and cross-story reporting
- **RPT-002**: Velocity tracking and sprint metrics
- **RPT-003**: Dependency visualization and impact analysis
- **RPT-004**: Export tools (JSON, CSV, markdown bulk operations)

### Integration & Deployment (Epic: integration)
- **INT-001**: Docker compose production configuration
- **INT-002**: WebSocket real-time update system
- **INT-003**: CI/CD integration endpoints
- **INT-004**: Monitoring and health check endpoints

## Impact

### Areas Affected
- **Database**: New PostgreSQL container with story management schema
- **API Layer**: Complete REST API service for story operations
- **File System**: Enhanced with two-way synchronization capability
- **Documentation**: OpenAPI specs and integration guides
- **Deployment**: Docker compose stack for development and production

### Benefits
- **Automation**: Programmatic story management reduces manual effort
- **Performance**: Database queries enable complex reporting and analytics
- **Integration**: API endpoints enable CI/CD and external tool integration
- **Scalability**: Containerized service supports multiple concurrent users
- **Consistency**: Automated validation ensures data integrity across operations

### Stakeholder Value
- **Planning Agent**: Enhanced automation and reporting capabilities
- **Implementation Agent**: API integration for status updates and queries
- **Stakeholders**: Real-time dashboards and advanced analytics
- **Developers**: Programmatic access for custom tools and integrations

## Technical Architecture

### Database Schema
```sql
-- Core story table
CREATE TABLE stories (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    epic VARCHAR(100),
    status VARCHAR(50) DEFAULT 'backlog',
    priority INTEGER DEFAULT 99,
    estimate VARCHAR(20),
    branch_name VARCHAR(255),
    file_path VARCHAR(500),
    owner VARCHAR(100),
    created_date DATE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Dependencies relationship table  
CREATE TABLE story_dependencies (
    story_id VARCHAR(50) REFERENCES stories(id),
    depends_on VARCHAR(50) REFERENCES stories(id),
    PRIMARY KEY (story_id, depends_on)
);

-- Status history for audit trail
CREATE TABLE status_history (
    id SERIAL PRIMARY KEY,
    story_id VARCHAR(50) REFERENCES stories(id),
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    changed_by VARCHAR(100),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);
```

### REST API Endpoints

#### Story Management
```
GET    /api/v1/stories              # List stories with filtering
POST   /api/v1/stories              # Create new story
GET    /api/v1/stories/{id}         # Get story details
PUT    /api/v1/stories/{id}         # Update story
DELETE /api/v1/stories/{id}         # Delete story
POST   /api/v1/stories/{id}/transition # Change status with validation
```

#### Reporting & Analytics
```
GET    /api/v1/reports/epic-summary      # Stories by epic and status
GET    /api/v1/reports/velocity          # Sprint velocity metrics
GET    /api/v1/reports/dependencies      # Dependency graph data
GET    /api/v1/reports/burndown         # Sprint burndown charts
```

#### Bulk Operations
```
POST   /api/v1/export/stories           # Export stories to JSON/CSV
POST   /api/v1/import/stories           # Import stories from JSON/CSV
GET    /api/v1/export/markdown/{epic}   # Export epic as markdown files
POST   /api/v1/sync/filesystem          # Force filesystem sync
```

### Docker Services
- **api**: FastAPI application server
- **db**: PostgreSQL database
- **sync**: File system synchronization service
- **nginx**: Reverse proxy for production deployment

## Implementation Considerations

### Database Choice Rationale
- **PostgreSQL**: Robust ACID compliance, excellent JSON support for metadata
- **Docker Native**: Official PostgreSQL Docker images with proven reliability
- **JSON Queries**: JSONB support enables flexible metadata querying
- **Performance**: Optimized for complex reporting queries and analytics

### Synchronization Strategy
- **Event-driven Sync**: File system watchers trigger database updates
- **Bi-directional**: Database changes generate markdown file updates
- **Conflict Resolution**: File system takes precedence for manual edits
- **Batch Processing**: Bulk operations processed efficiently

### Security Considerations
- **API Authentication**: JWT tokens or API keys for endpoint access
- **Rate Limiting**: Prevent abuse of bulk operations
- **Input Validation**: Strict validation for all story data
- **Audit Logging**: Complete trail of all story modifications

## Notes
- Maintains backward compatibility with existing file-based workflow
- Database serves as performance layer while files remain source of truth for stakeholder visibility
- Service can be deployed locally for development or in cloud for team access
- WebSocket support enables real-time collaboration features
- Export functionality provides migration path and backup capabilities
- API documentation auto-generated from OpenAPI specification for easy integration

## Dependencies
- Docker and Docker Compose for containerization
- FastAPI framework for REST API development
- PostgreSQL for data storage and analytics
- SQLAlchemy for database ORM and migrations
- Watchdog for file system monitoring
- AsyncIO for real-time WebSocket updates

## Future Enhancements
- **GraphQL Endpoint**: More flexible querying for complex UI needs
- **Story Templates API**: Programmatic template management
- **Workflow Automation**: Trigger external actions on status changes
- **Mobile API**: Optimized endpoints for mobile story management apps
- **Analytics Dashboard**: Web UI for reporting and visualization