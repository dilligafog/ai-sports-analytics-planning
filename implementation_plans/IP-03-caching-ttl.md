# INF-003 Implementation Plan - Caching & TTL for time-sensitive signals

## Overview
- **Story Reference**: [INF-003](../backlog/llm/infra/03-caching-ttl.md)
- **Epic**: llm_backlog
- **Estimated Effort**: 2 story points
- **Timeline**: 1 week with 2 phases
- **Priority**: Medium

## Technical Approach
- **Architecture**: Multi-layer caching system with TTL enforcement, disk-based cache with metadata indexing, and monitoring integration
- **Technology Stack**:
  - Redis for high-performance in-memory caching
  - SQLite for metadata indexing and TTL tracking
  - Disk storage for large cached objects (LLM features, news articles)
  - APScheduler for cache cleanup and monitoring
  - Prometheus metrics for cache performance monitoring
- **Integration Points**:
  - LLM feature extraction pipeline
  - News ingestion and retrieval systems
  - Odds/betting data collection
  - Model inference pipeline
- **Data Flow**: Request → Cache check → TTL validation → Fresh data retrieval (if needed) → Cache update → Response

## Implementation Phases

### Phase 1: Core Caching Infrastructure
**Deliverables:**
- Multi-layer cache implementation (memory + disk)
- TTL enforcement for different data types
- Basic cache management and cleanup
- Configuration integration via `config/runtime.yml`

**Story Points**: 1.5
**Dependencies**: INF-001 (configuration system)
**Technical Tasks:**
- Implement cache layer with Redis and disk storage
- Create TTL enforcement mechanisms for different data types
- Build cache key generation strategy (cluster_id for LLM features)
- Implement automatic cache cleanup with configurable schedules
- Create cache configuration in `config/runtime.yml`

### Phase 2: Monitoring & Advanced Features
**Deliverables:**
- Cache performance monitoring and alerting
- ETag/Last-Modified support for news feeds
- Stale data detection during inference
- Cache warming and preloading strategies

**Story Points**: 0.5
**Dependencies**: Phase 1 completion
**Technical Tasks:**
- Add Prometheus metrics for cache hit/miss rates and TTL violations
- Implement ETag/Last-Modified caching for HTTP resources
- Create monitoring alerts for expired signals during inference
- Build cache warming mechanisms for critical data
- Add cache statistics and reporting to CLI tools

## Technical Decisions

### Cache Storage Decision
**Choice**: Redis for hot data + disk storage for large objects
**Rationale**:
- Redis provides fast access for frequently used data
- Disk storage handles large LLM feature vectors efficiently
- Hybrid approach optimizes both performance and storage costs
**Alternatives Considered**: Pure in-memory (memory limitations), pure disk (performance issues), database (overkill)

### TTL Strategy Decision
**Choice**: Data-type specific TTL with configurable overrides
**Rationale**:
- Different data types have different freshness requirements
- LLM features: 24 hours (daily news cycle)
- News articles: 1 hour (breaking news)
- Odds data: 60 seconds (real-time changes)
**Alternatives Considered**: Fixed TTL (inflexible), no TTL (stale data risk), manual expiration (error-prone)

### Cache Key Strategy Decision
**Choice**: Hierarchical cache keys with semantic meaning
**Rationale**:
- `llm:features:{cluster_id}:{date}` for LLM features
- `news:{source}:{article_id}:{etag}` for news articles
- `odds:{game_id}:{timestamp}` for betting odds
- Enables selective cache invalidation and debugging
**Alternatives Considered**: Hash-based keys (no semantic meaning), flat namespace (collision risk)

## Risks and Mitigation

### Risk: Cache Inconsistency Between Layers
**Impact**: Medium - Stale data served to applications
**Likelihood**: Low
**Mitigation**:
- Atomic cache operations with transaction-like behavior
- Cache validation checks during retrieval
- Monitoring for cache layer inconsistencies
- Fallback to fresh data retrieval on cache errors

### Risk: TTL Violations During High Load
**Impact**: High - Stale signals affect prediction accuracy
**Likelihood**: Medium
**Mitigation**:
- Circuit breaker pattern for cache failures
- Graceful degradation with fresh data retrieval
- Load balancing and cache partitioning
- Emergency cache flush procedures

### Risk: Disk Space Exhaustion
**Impact**: Medium - Cache failures and system instability
**Likelihood**: Medium
**Mitigation**:
- Automated cache size monitoring and cleanup
- Configurable cache size limits with LRU eviction
- Disk space alerts and emergency cleanup procedures
- Cache compression for large objects

## Success Criteria

### Functional Requirements
- LLM features cached with 24-hour TTL (configurable)
- News articles cached with ETag/Last-Modified support
- Odds data cached with 60-second TTL
- No inference run uses signals older than configured TTL
- Automatic cache cleanup prevents disk space issues

### Non-functional Requirements
- Cache hit ratio > 80% for frequently accessed data
- Cache lookup time < 10ms for in-memory data
- TTL violation rate < 1% during normal operations
- Cache cleanup completes within maintenance windows

### Testing Strategy
- Unit tests for cache operations and TTL enforcement (95% coverage)
- Integration tests for different data types and TTL scenarios
- Performance tests for cache throughput and latency
- Stress tests for cache cleanup and TTL violation handling

## Follow-up Work

### Immediate Follow-ups (Next Sprint)
- Cache warming strategies for critical game predictions
- Advanced cache statistics and analytics dashboard
- Cache replication for high availability

### Technical Debt Considerations
- Regular cache performance tuning based on usage patterns
- Cache size optimization as data volume grows
- TTL configuration review based on data freshness requirements

### Future Enhancements
- Intelligent cache prefetching based on usage patterns
- Distributed caching for multi-instance deployments
- Machine learning-based TTL optimization
- Real-time cache invalidation for breaking news

## Implementation Structure

```python
# Cache manager with TTL enforcement
class CacheManager:
    def __init__(self, config: CacheConfig):
        self.redis = Redis(config.redis_url)
        self.disk_cache = DiskCache(config.cache_dir)
        self.metadata_db = SQLiteMetadata(config.metadata_path)
        
    def get(self, key: str, ttl_hours: Optional[int] = None) -> Optional[Any]:
        # Check TTL first
        if self.is_expired(key, ttl_hours):
            self.invalidate(key)
            return None
            
        # Try memory cache first
        data = self.redis.get(key)
        if data:
            return pickle.loads(data)
            
        # Fall back to disk cache
        return self.disk_cache.get(key)
    
    def set(self, key: str, value: Any, ttl_hours: int):
        timestamp = datetime.utcnow()
        
        # Store in memory for hot data
        if self.is_hot_data(key):
            self.redis.setex(key, ttl_hours * 3600, pickle.dumps(value))
        
        # Always store on disk with metadata
        self.disk_cache.set(key, value)
        self.metadata_db.record_cache_entry(key, timestamp, ttl_hours)
```

## Configuration Example

```yaml
# config/runtime.yml
cache:
  redis_url: "redis://localhost:6379"
  cache_dir: "data/cache"
  metadata_path: "data/cache/metadata.db"
  
  # TTL configurations (hours)
  ttl:
    llm_features: 24
    news_articles: 1
    odds_data: 0.017  # 1 minute
    
  # Cleanup schedule
  cleanup:
    interval: "0 2 * * *"  # Daily at 2 AM
    max_size_gb: 10
    
  # Monitoring
  monitoring:
    ttl_violation_threshold: 0.01  # 1%
    cache_hit_ratio_threshold: 0.8  # 80%
```

## Monitoring Metrics

```python
# Prometheus metrics
cache_hit_total = Counter('cache_hit_total', 'Cache hits', ['cache_type'])
cache_miss_total = Counter('cache_miss_total', 'Cache misses', ['cache_type'])
ttl_violation_total = Counter('ttl_violation_total', 'TTL violations', ['data_type'])
cache_size_bytes = Gauge('cache_size_bytes', 'Cache size in bytes', ['cache_type'])
```