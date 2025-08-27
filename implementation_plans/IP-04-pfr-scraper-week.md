# ING-004 Implementation Plan - PFR weekly schedule & team stats scraper

## Overview
- **Story Reference**: [ING-004](../backlog/llm/ingestion/04-pfr-scraper-week.md)
- **Epic**: llm_backlog
- **Estimated Effort**: 2 story points
- **Timeline**: 1 week with 2 phases
- **Priority**: Medium

## Technical Approach
- **Architecture**: Respectful web scraping with caching, structured data parsing, and ETL pipeline for feature engineering
- **Technology Stack**:
  - requests + lxml/BeautifulSoup for web scraping
  - pandas for data manipulation and rolling statistics
  - pyarrow/parquet for efficient data storage
  - schedule/APScheduler for automated collection
  - robots.txt compliance checking
- **Integration Points**:
  - Odds data (join via game_id)
  - LLM signals (game context)
  - Model training pipeline (MOD-001, MOD-002)
  - Feature store (silver/gold tables)
- **Data Flow**: PFR website → Scraper → Raw parquet (Bronze) → Transform → Rolling stats (Silver) → Game features (Gold)

## Implementation Phases

### Phase 1: Scraper Implementation & Data Collection
**Deliverables:**
- `python -m src.cli collect pfr-week` command
- Web scraping with robots.txt compliance and polite delays
- Raw data storage in `data/bronze/pfr_week_raw.parquet`
- Basic HTML parsing for schedule and team stats

**Story Points**: 1.5
**Dependencies**: None (foundational data ingestion)
**Technical Tasks:**
- Implement robots.txt checking and polite delay mechanisms (2-3 second delays)
- Build HTML parsers for PFR schedule and team stats tables
- Create data models for schedule (game_id, week, season, teams, kickoff) and team stats
- Implement page caching to disk to avoid re-scraping during development
- Add error handling and retry logic for network failures

### Phase 2: Feature Engineering & Pipeline Integration
**Deliverables:**
- Rolling efficiency stats (last-5 games offense/defense)
- Silver/Gold table transformations
- Integration with odds and LLM signals via game_id
- Unit tests and CI validation

**Story Points**: 0.5
**Dependencies**: Phase 1 completion, basic feature store structure
**Technical Tasks:**
- Calculate rolling statistics: offensive/defensive efficiency, scoring trends
- Implement game_id standardization for joins with other data sources
- Create silver table transformations with team performance metrics
- Build gold table features optimized for model training
- Add comprehensive unit tests for 2 sample weeks of data

## Technical Decisions

### Scraping Ethics Decision
**Choice**: Respectful scraping with robots.txt compliance and delays
**Rationale**:
- Follows web scraping best practices and site policies
- 2-3 second delays prevent server overload
- Caching reduces redundant requests
- Compliance reduces risk of IP blocking
**Alternatives Considered**: Aggressive scraping (unethical), paid API (not available), manual data entry (not scalable)

### Data Storage Decision
**Choice**: Parquet format for efficient analytics workloads
**Rationale**:
- Columnar format optimized for analytics queries
- Good compression and query performance
- Native pandas integration
- Suitable for time-series data
**Alternatives Considered**: CSV (inefficient), database (overkill for this use case), JSON (not optimized)

### Feature Engineering Decision
**Choice**: Rolling window statistics with configurable lookback
**Rationale**:
- Last-5 games captures recent team form
- Rolling statistics smooth out week-to-week variance
- Configurable windows allow experimentation
- Standard approach in sports analytics
**Alternatives Considered**: Season averages (too stable), single game stats (too noisy), weighted averages (more complex)

## Risks and Mitigation

### Risk: Website Structure Changes Breaking Parser
**Impact**: High - Data collection stops
**Likelihood**: Medium
**Mitigation**:
- Robust CSS selector strategies with fallbacks
- Multiple parsing approaches for critical tables
- Automated testing with cached HTML samples
- Monitoring and alerting for parsing failures

### Risk: IP Blocking Due to Scraping
**Impact**: High - Complete data loss from PFR
**Likelihood**: Low (with proper rate limiting)
**Mitigation**:
- Strict adherence to robots.txt and rate limits
- User-Agent rotation and respectful request headers
- Proxy rotation if necessary
- Backup data sources identified

### Risk: Data Quality Issues in Source
**Impact**: Medium - Incorrect features affect model performance
**Likelihood**: Medium
**Mitigation**:
- Data validation checks for completeness and consistency
- Cross-validation with official NFL data sources
- Outlier detection for statistical anomalies
- Manual review processes for suspicious data

## Success Criteria

### Functional Requirements
- CLI command successfully scrapes and stores weekly schedule data
- Rolling efficiency statistics calculated for all teams
- Game_id standardization enables joins with odds and LLM data
- Data coverage includes 100% of upcoming games for current season

### Non-functional Requirements
- Scraping completes within 30 minutes for full weekly update
- Data quality validation passes for all collected data
- Memory usage < 2GB during processing
- Network requests follow 2-3 second delay policy

### Testing Strategy
- Unit tests for HTML parsing with cached sample pages (90% coverage)
- Integration tests with 2 complete sample weeks
- Data quality tests for statistical validity
- End-to-end tests validating joins with other data sources

## Follow-up Work

### Immediate Follow-ups (Next Sprint)
- Historical data backfill for multiple seasons
- Player-level statistics scraping
- Injury report integration
- Weather data correlation

### Technical Debt Considerations
- Regular monitoring of parsing success rates
- Performance optimization for large historical datasets
- Website change detection and parser maintenance

### Future Enhancements
- Real-time game score scraping during live games
- Advanced team performance metrics (DVOA-style analytics)
- Playoff and championship game special handling
- Integration with advanced football analytics APIs

## Implementation Structure

```python
# PFR scraper implementation
class PFRScraper:
    def __init__(self, config: ScrapingConfig):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': config.user_agent})
        self.delay = config.request_delay
        self.cache_dir = config.cache_dir
        
    def check_robots_txt(self, url: str) -> bool:
        """Check if scraping is allowed by robots.txt"""
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(f"{url}/robots.txt")
        rp.read()
        return rp.can_fetch(self.session.headers['User-Agent'], url)
    
    def scrape_weekly_schedule(self, week: int, season: int) -> pd.DataFrame:
        """Scrape schedule for specific week"""
        if not self.check_robots_txt(PFR_BASE_URL):
            raise PermissionError("Robots.txt disallows scraping")
            
        url = f"{PFR_BASE_URL}/years/{season}/week_{week}.htm"
        html = self._get_cached_or_fetch(url)
        
        # Parse schedule table
        soup = BeautifulSoup(html, 'lxml')
        schedule_table = soup.find('table', {'id': 'games'})
        
        return self._parse_schedule_table(schedule_table, week, season)
    
    def _get_cached_or_fetch(self, url: str) -> str:
        """Get page from cache or fetch with delay"""
        cache_key = hashlib.md5(url.encode()).hexdigest()
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.html")
        
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                return f.read()
        
        time.sleep(self.delay)  # Respectful delay
        response = self.session.get(url)
        response.raise_for_status()
        
        # Cache the response
        os.makedirs(self.cache_dir, exist_ok=True)
        with open(cache_file, 'w') as f:
            f.write(response.text)
            
        return response.text
```

## Data Schema

```python
# Schedule data schema
class GameSchedule(BaseModel):
    game_id: str  # Standardized format: "2024_week_1_home_away"
    week: int
    season: int
    home_team: str  # Standardized team abbreviation
    away_team: str
    kickoff_et: datetime
    completed: bool = False

# Team stats schema  
class TeamStats(BaseModel):
    team: str
    week: int
    season: int
    offensive_efficiency: float  # Rolling 5-game average
    defensive_efficiency: float
    turnover_differential: float
    red_zone_efficiency: float
    third_down_conversion: float
```

## CLI Integration

```bash
# Command usage examples
python -m src.cli collect pfr-week --week 1 --season 2024
python -m src.cli collect pfr-week --current-week  # Automatic current week
python -m src.cli transform pfr-stats --input bronze --output silver
```

## Data Pipeline Flow

```
1. Raw Scraping (Bronze)
   └── data/bronze/pfr_week_raw.parquet
   
2. Team Stats Calculation (Silver)  
   └── data/silver/team_rolling_stats.parquet
   
3. Game Features (Gold)
   └── data/gold/game_features.parquet
   
4. Integration Points
   ├── Join with odds data via game_id
   ├── Context for LLM signals
   └── Features for model training
```