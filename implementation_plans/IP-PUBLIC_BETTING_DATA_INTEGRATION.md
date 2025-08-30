# PUBLIC_BETTING_DATA_INTEGRATION Implementation Plan - Public Betting Data Integration

## Overview
- **Story Reference**: [PUBLIC_BETTING_DATA_INTEGRATION](../backlog/models/PUBLIC_BETTING_DATA_INTEGRATION.md)
- **Epic**: ingestion
- **Estimated Effort**: 5 story points
- **Timeline**: 2-3 weeks with 3 phases
- **Priority**: Medium

## Technical Approach
- **Architecture**: Multi-source data aggregation with real-time line movement tracking, contrarian strategy analysis, and integrated UI visualization
- **Technology Stack**:
  - Python requests/aiohttp for API data collection
  - pandas/numpy for line movement analysis
  - SQLite for historical betting trend storage
  - FastAPI for betting data API endpoints
  - Chart.js/D3.js for line movement visualizations
- **Integration Points**:
  - Data Source Integration Framework (foundation)
  - UI visualization components
  - LLM narrative generation
  - Model training feature pipeline
- **Data Flow**: Sportsbook APIs → Aggregation layer → Line movement analysis → Feature engineering → UI/LLM integration

## Implementation Phases

### Phase 1: Data Collection & Storage Infrastructure
**Deliverables:**
- Multi-sportsbook data collection system
- Standardized betting data schema
- Historical data storage and retrieval
- Basic line movement tracking

**Story Points**: 2
**Dependencies**: Data Source Integration Framework
**Technical Tasks:**
- Research and integrate 3-5 public betting data sources (OddsAPI, Vegas Insider, Action Network)
- Design standardized schema for betting percentages, money distribution, and line movement
- Implement data collection pipelines with appropriate rate limiting
- Create historical data storage with efficient querying for trend analysis
- Build basic line movement detection and storage

### Phase 2: Analysis & Feature Engineering
**Deliverables:**
- Contrarian value identification algorithms
- Public sentiment analysis tools
- Betting trend feature extraction
- Sharp vs. public money detection

**Story Points**: 2
**Dependencies**: Phase 1 completion
**Technical Tasks:**
- Implement contrarian strategy detection (public % vs. line movement divergence)
- Create algorithms to identify "sharp" vs. "public" money indicators
- Build feature engineering pipeline for betting trend integration with ML models
- Develop public sentiment scoring based on betting patterns
- Create betting volume and timing analysis tools

### Phase 3: UI Integration & LLM Enhancement
**Deliverables:**
- Real-time betting data visualization in UI
- LLM integration for betting context in narratives
- Value bet identification dashboard
- Public betting trend reporting

**Story Points**: 1
**Dependencies**: Phase 2 completion, UI framework, LLM pipeline
**Technical Tasks:**
- Create UI components for line movement charts and public betting percentages
- Integrate betting data into LLM prompts for contextual narrative generation
- Build value bet identification dashboard with contrarian indicators
- Implement real-time updates for betting data in UI
- Create betting trend summary reports and alerts

## Technical Decisions

### Data Source Strategy Decision
**Choice**: Multi-source aggregation with consensus validation
**Rationale**:
- Different sportsbooks provide different perspectives on public sentiment
- Consensus approach reduces impact of single-source errors
- Redundancy protects against API outages
- Cross-validation improves data quality
**Alternatives Considered**: Single premium source (expensive, single point of failure), manual data entry (not scalable)

### Line Movement Analysis Decision
**Choice**: Time-series analysis with threshold-based alerts
**Rationale**:
- Captures both gradual line movement and sharp sudden changes
- Threshold-based alerts identify significant movement
- Historical pattern recognition for similar game situations
- Statistical significance testing for movement patterns
**Alternatives Considered**: Simple percentage tracking (insufficient context), complex ML models (overkill for initial implementation)

### Value Bet Identification Decision
**Choice**: Contrarian strategy with multiple validation signals
**Rationale**:
- Public betting % vs. line movement divergence is proven profitable
- Multiple signals reduce false positives
- Considers both money percentage and ticket percentage
- Incorporates timing of betting movement
**Alternatives Considered**: Simple contrarian approach (too basic), complex multi-factor models (premature optimization)

## Risks and Mitigation

### Risk: API Rate Limiting and Access Restrictions
**Impact**: High - Data collection failures
**Likelihood**: Medium
**Mitigation**:
- Implement respectful rate limiting with exponential backoff
- Use multiple data sources to distribute load
- Cache data aggressively to reduce API calls
- Monitor API usage and implement usage-based switching

### Risk: Data Quality and Accuracy Issues
**Impact**: Medium - Incorrect betting insights
**Likelihood**: Medium
**Mitigation**:
- Cross-validate data across multiple sources
- Implement statistical outlier detection
- Create data quality monitoring dashboards
- Manual verification processes for high-impact games

### Risk: Real-time Data Latency
**Impact**: Medium - Stale betting information
**Likelihood**: Low
**Mitigation**:
- Implement efficient data streaming and caching
- Use WebSocket connections where available
- Create latency monitoring and alerting
- Graceful degradation with batch updates

## Success Criteria

### Functional Requirements
- System collects public betting data from 3+ sportsbooks
- Line movement tracking with historical trend analysis
- Contrarian value bet identification with >60% accuracy on historical data
- UI displays real-time betting information with line movement charts
- LLM narratives include relevant public betting context

### Non-functional Requirements
- Data collection latency < 5 minutes for important games
- UI updates betting data every 2-3 minutes during game days
- System handles 100+ concurrent games during peak periods
- Data storage efficiently supports 2+ years of historical analysis

### Testing Strategy
- Unit tests for all data collection and analysis components (90% coverage)
- Integration tests with mock API responses
- Historical backtesting of contrarian strategies
- UI testing for real-time data updates and visualization

## Follow-up Work

### Immediate Follow-ups (Next Sprint)
- Advanced betting pattern recognition (steam moves, reverse line movement)
- Integration with injury/weather data for context
- Automated value bet alert system
- Historical profitability tracking for betting strategies

### Technical Debt Considerations
- Regular API endpoint monitoring and maintenance
- Performance optimization for real-time data processing
- Data storage optimization as historical data grows

### Future Enhancements
- Machine learning models for betting pattern prediction
- Integration with live game events and in-game betting
- Advanced visualization with heat maps and trend analysis
- Social sentiment correlation with betting patterns

## Implementation Structure

```python
# Betting data collector
class BettingDataCollector:
    def __init__(self, config: BettingConfig):
        self.sources = [
            OddsAPISource(config.odds_api_key),
            VegasInsiderSource(),
            ActionNetworkSource(config.action_key)
        ]
        self.storage = BettingDataStorage(config.db_url)
        
    async def collect_game_data(self, game_id: str) -> BettingData:
        """Collect betting data from all sources for a game"""
        tasks = [source.get_game_data(game_id) for source in self.sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Aggregate and validate data
        return self._aggregate_betting_data(results)
    
    def detect_line_movement(self, game_id: str, threshold: float = 0.5) -> List[LineMovement]:
        """Detect significant line movements"""
        historical_lines = self.storage.get_line_history(game_id)
        movements = []
        
        for i in range(1, len(historical_lines)):
            change = abs(historical_lines[i].spread - historical_lines[i-1].spread)
            if change >= threshold:
                movements.append(LineMovement(
                    timestamp=historical_lines[i].timestamp,
                    old_line=historical_lines[i-1].spread,
                    new_line=historical_lines[i].spread,
                    movement=change,
                    direction='up' if historical_lines[i].spread > historical_lines[i-1].spread else 'down'
                ))
        
        return movements

# Contrarian value detector
class ContrarianAnalyzer:
    def identify_value_bets(self, betting_data: BettingData) -> List[ValueBet]:
        """Identify contrarian value opportunities"""
        value_bets = []
        
        # Check for public % vs line movement divergence
        if self._is_contrarian_signal(betting_data):
            confidence = self._calculate_confidence(betting_data)
            value_bets.append(ValueBet(
                game_id=betting_data.game_id,
                bet_type='contrarian',
                recommended_side=self._get_contrarian_side(betting_data),
                confidence=confidence,
                reasoning=self._generate_reasoning(betting_data)
            ))
            
        return value_bets
```

## Data Schema

```python
class BettingData(BaseModel):
    game_id: str
    timestamp: datetime
    sportsbook: str
    
    # Line information
    spread: float
    total: float
    moneyline_home: int
    moneyline_away: int
    
    # Public betting percentages
    spread_public_pct: float  # % betting on favorite
    total_public_pct: float   # % betting on over
    moneyline_public_pct: float
    
    # Money distribution
    spread_money_pct: float
    total_money_pct: float
    moneyline_money_pct: float

class LineMovement(BaseModel):
    game_id: str
    timestamp: datetime
    old_line: float
    new_line: float
    movement: float
    direction: str
    trigger: str  # 'sharp_money', 'public_betting', 'injury_news', etc.

class ValueBet(BaseModel):
    game_id: str
    bet_type: str
    recommended_side: str
    confidence: float
    reasoning: str
    expected_value: Optional[float]
```

## UI Integration Components

```javascript
// Line movement chart component
class LineMovementChart {
    constructor(gameId, containerId) {
        this.gameId = gameId;
        this.container = containerId;
        this.chart = null;
        this.initChart();
        this.startRealtimeUpdates();
    }
    
    initChart() {
        // D3.js implementation for real-time line movement
        this.chart = d3.select(`#${this.container}`)
            .append('svg')
            .attr('width', 600)
            .attr('height', 300);
    }
    
    updateLineData(newData) {
        // Update chart with new betting line data
        // Highlight significant movements
        // Show public betting percentages
    }
}

// Public betting dashboard
class PublicBettingDashboard {
    renderValueBets(valueBets) {
        return valueBets.map(bet => ({
            game: bet.game_id,
            recommendation: bet.recommended_side,
            confidence: bet.confidence,
            reasoning: bet.reasoning,
            publicPercent: bet.public_percentage,
            lineMovement: bet.line_movement
        }));
    }
}
```

## LLM Integration

```python
# Enhanced LLM prompts with betting context
def generate_game_analysis_with_betting_context(game_data, betting_data):
    """Generate LLM analysis including public betting trends"""
    
    betting_context = f"""
    Public Betting Analysis:
    - {betting_data.spread_public_pct:.0f}% of bettors are taking {betting_data.favorite_team}
    - Line movement: {betting_data.line_movement_direction} by {betting_data.line_movement_amount} points
    - Sharp money indicator: {'YES' if betting_data.is_sharp_money else 'NO'}
    - Contrarian value: {'HIGH' if betting_data.contrarian_value > 0.7 else 'LOW'}
    """
    
    prompt = f"""
    Analyze this NFL game with consideration for public betting trends:
    
    {game_data.basic_analysis}
    
    {betting_context}
    
    Consider how public sentiment might be affecting the line and identify any potential value...
    """
    
    return llm_client.generate(prompt)
```