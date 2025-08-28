# RPT-003 Implementation Plan - Dependency visualization and impact analysis

## Overview
- **Story Reference**: [RPT-003](../refinements/reporting/RPT-003-dependency-visualization-impact-analysis.md)
- **Epic**: reporting
- **Estimated Effort**: 6 story points
- **Timeline**: 2.5 weeks with 3 phases
- **Priority**: Medium

## Technical Approach
- **Architecture**: Graph-based dependency analysis with PostgreSQL recursive queries and network analysis algorithms
- **Technology Stack**:
  - PostgreSQL with recursive CTEs for graph traversal
  - NetworkX Python library for complex graph analysis
  - FastAPI with graph data serialization
  - Graphviz for graph layout algorithms
  - Redis for caching complex dependency calculations
  - D3.js compatible data formats for visualization
- **Integration Points**:
  - Story management API (API-001)
  - PostgreSQL story and dependency tables
  - Export capabilities for visualization tools
- **Data Flow**: Dependency data → Graph analysis → Critical path calculation → Visualization data → API response

## Implementation Phases

### Phase 1: Graph Data Foundation
**Deliverables:**
- Enhanced dependency data model
- Basic graph traversal and analysis
- Dependency cycle detection
- Simple critical path calculation
- Graph data API endpoints

**Story Points**: 2
**Dependencies**: API-001, database with story_dependencies table
**Technical Tasks:**
- Enhance dependency table with relationship types and weights
- Implement PostgreSQL recursive queries for dependency traversal
- Create basic graph representation and traversal algorithms
- Add cycle detection using depth-first search
- Build API endpoints for dependency graph data
- Implement basic critical path analysis

### Phase 2: Advanced Graph Analysis
**Deliverables:**
- Impact analysis algorithms
- Advanced critical path calculation
- Dependency strength analysis
- Risk assessment based on graph metrics
- Performance optimization for large graphs

**Story Points**: 2.5
**Dependencies**: Phase 1 completion
**Technical Tasks:**
- Implement NetworkX integration for advanced graph algorithms
- Build impact analysis for downstream dependency effects
- Add dependency strength calculation (direct vs indirect)
- Create risk scoring based on graph centrality metrics
- Optimize graph calculations with caching strategies
- Add parallel processing for large dependency networks

### Phase 3: Visualization and Export Features
**Deliverables:**
- Multiple graph layout algorithms
- Export capabilities for visualization tools
- Epic-level dependency mapping
- Interactive graph data formats
- Performance monitoring and optimization

**Story Points**: 1.5
**Dependencies**: Phase 2 completion
**Technical Tasks:**
- Implement multiple graph layout algorithms (hierarchical, force-directed)
- Add export capabilities for GraphML, DOT, and JSON formats
- Create epic-level dependency aggregation and visualization
- Build D3.js compatible data structures
- Add graph performance monitoring and metrics
- Optimize memory usage for large dependency networks

## Technical Decisions

### Graph Analysis Library Choice
**Choice**: NetworkX for complex analysis, PostgreSQL for basic traversal
**Rationale**:
- NetworkX provides proven graph algorithms for complex analysis
- PostgreSQL recursive queries efficient for simple traversal
- Hybrid approach balances performance and capability
**Alternatives Considered**: Pure SQL (limited algorithms), Neo4j (overkill for current scale), Custom implementation (reinventing wheel)

### Dependency Model Design
**Choice**: Weighted directed graph with multiple relationship types
**Rationale**:
- Supports different types of dependencies (blocks, depends on, relates to)
- Weights enable sophisticated impact analysis
- Directed graph reflects real dependency relationships
**Alternatives Considered**: Simple binary relationships (less expressive), Undirected graph (loses dependency direction), Complex multi-graph (over-engineering)

### Performance Strategy
**Choice**: Cached graph analysis with selective recalculation
**Rationale**:
- Graph algorithms are computationally expensive
- Dependency graphs change infrequently
- Selective cache invalidation maintains accuracy
**Alternatives Considered**: Real-time calculation (poor performance), Pre-computed views (complex maintenance), No caching (slow response times)

## Risks and Mitigation

### Risk: Graph Calculation Performance
**Impact**: High - Slow analysis affects user experience
**Likelihood**: Medium
**Mitigation**:
- Implement efficient graph algorithms with complexity analysis
- Use caching for expensive calculations
- Provide progress indicators for long-running analysis
- Set reasonable timeouts for complex calculations

### Risk: Circular Dependency Complexity
**Impact**: Medium - Complex cycles difficult to resolve
**Likelihood**: Medium
**Mitigation**:
- Implement robust cycle detection algorithms
- Provide clear visualization of circular dependencies
- Include resolution recommendations in API responses
- Allow manual override for valid circular relationships

### Risk: Memory Usage with Large Graphs
**Impact**: Medium - Memory exhaustion with large dependency networks
**Likelihood**: Low
**Mitigation**:
- Implement streaming analysis for very large graphs
- Use memory-efficient graph representations
- Monitor memory usage and implement limits
- Provide graph simplification options

## Success Criteria

### Functional Requirements
- Detect all dependency cycles in story relationships
- Calculate critical path accurately for complex dependency networks
- Impact analysis identifies all downstream affected stories
- Support dependency graphs with 1000+ stories and 5000+ relationships
- Export formats compatible with common visualization tools

### Non-functional Requirements
- Graph analysis completes within 10 seconds for typical story collections
- Memory usage remains under 1GB for large dependency networks
- API responses include performance metrics for monitoring
- Cached results reduce calculation time by 80% for repeated requests

### Testing Strategy
- Unit tests for all graph algorithms with known test cases
- Performance tests with artificially large dependency networks
- Cycle detection tests with complex circular dependency scenarios
- Critical path validation with manual calculation verification
- Memory usage tests with large graph datasets

## Graph Analysis Algorithms

### Critical Path Calculation
```python
def calculate_critical_path(graph, start_story, end_story):
    """
    Calculate critical path using longest path algorithm
    considering story estimates and dependencies
    """
    # Topological sort to ensure acyclic processing
    topo_order = networkx.topological_sort(graph)
    
    # Initialize distances and predecessors
    distances = {node: float('-inf') for node in graph.nodes()}
    distances[start_story] = 0
    predecessors = {}
    
    # Calculate longest path (critical path)
    for node in topo_order:
        for successor in graph.successors(node):
            edge_weight = graph[node][successor]['weight']
            if distances[node] + edge_weight > distances[successor]:
                distances[successor] = distances[node] + edge_weight
                predecessors[successor] = node
    
    # Reconstruct path
    path = []
    current = end_story
    while current in predecessors:
        path.append(current)
        current = predecessors[current]
    path.append(start_story)
    
    return list(reversed(path)), distances[end_story]
```

### Impact Analysis
```python
def analyze_impact(graph, changed_story):
    """
    Analyze downstream impact of changes to a specific story
    """
    # Find all downstream dependencies
    downstream = networkx.descendants(graph, changed_story)
    
    # Calculate impact score based on dependency strength
    impact_scores = {}
    for story in downstream:
        # Consider direct vs indirect dependencies
        shortest_path = networkx.shortest_path_length(
            graph, changed_story, story
        )
        dependency_strength = 1.0 / shortest_path
        
        # Weight by story importance (priority, epic criticality)
        story_weight = get_story_importance(story)
        impact_scores[story] = dependency_strength * story_weight
    
    return sorted(impact_scores.items(), key=lambda x: x[1], reverse=True)
```

## Database Schema Enhancements

```sql
-- Enhanced dependency relationships
ALTER TABLE story_dependencies ADD COLUMN relationship_type VARCHAR(50) DEFAULT 'depends_on';
ALTER TABLE story_dependencies ADD COLUMN weight DECIMAL(3,2) DEFAULT 1.0;
ALTER TABLE story_dependencies ADD COLUMN created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Indexes for graph traversal performance
CREATE INDEX story_deps_source_idx ON story_dependencies(story_id);
CREATE INDEX story_deps_target_idx ON story_dependencies(depends_on);
CREATE INDEX story_deps_type_idx ON story_dependencies(relationship_type);

-- Materialized view for graph analysis
CREATE MATERIALIZED VIEW story_dependency_graph AS
SELECT 
    sd.story_id as source,
    sd.depends_on as target,
    sd.relationship_type,
    sd.weight,
    s1.epic as source_epic,
    s2.epic as target_epic,
    s1.priority as source_priority,
    s2.priority as target_priority
FROM story_dependencies sd
JOIN stories s1 ON sd.story_id = s1.id
JOIN stories s2 ON sd.depends_on = s2.id;

CREATE INDEX story_dep_graph_source_idx ON story_dependency_graph(source);
CREATE INDEX story_dep_graph_target_idx ON story_dependency_graph(target);
```

## API Response Format

```json
{
  "dependency_analysis": {
    "story_id": "INF-014",
    "critical_path": {
      "path": ["INF-012", "INF-013", "INF-014", "API-001"],
      "total_weight": 15.5,
      "estimated_duration": "3 weeks"
    },
    "impact_analysis": {
      "directly_affected": ["API-001", "API-002"],
      "indirectly_affected": ["RPT-001", "INT-002"],
      "total_impact_score": 8.7
    },
    "dependency_cycles": [
      {
        "cycle": ["INF-012", "API-001", "INF-015", "INF-012"],
        "severity": "medium",
        "recommendation": "Consider removing API-001 → INF-015 dependency"
      }
    ],
    "graph_metrics": {
      "total_nodes": 16,
      "total_edges": 23,
      "density": 0.19,
      "longest_path": 4
    }
  },
  "visualization_data": {
    "nodes": [...],
    "edges": [...],
    "layout": "hierarchical"
  }
}
```