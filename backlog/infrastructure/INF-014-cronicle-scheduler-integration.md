# INF-014 - Cronicle Scheduler Integration for NFL Prediction Pipeline

## 🎯 **Story Overview**

**Epic**: Infrastructure  
**Priority**: High  
**Estimate**: 5 story points  
**Type**: Infrastructure Enhancement

### **User Story**
As a system administrator, I want to integrate Cronicle as our job scheduler so that I can manage NFL prediction pipeline jobs through a web interface with real-time monitoring, automated scheduling, and multi-server coordination.

## 🏈 **Business Value**

### **Current Pain Points**
- Manual cron job management across environments
- No visual interface for job status
- Difficult to debug failed pipeline runs
- No real-time monitoring of data pipeline
- Complex coordination between production/development environments

### **Value Delivered**
- **Visual Job Management**: Web UI for all scheduled tasks
- **Real-time Monitoring**: Live status of data pipeline runs
- **Multi-Environment Support**: Separate scheduling for prod/dev
- **Historical Tracking**: Performance trends over NFL seasons
- **Automated Recovery**: Built-in failover and retry mechanisms

## 🔧 **Technical Requirements**

### **Core Integration Features**
1. **Cronicle Server Setup**
   - Install and configure Cronicle on existing infrastructure
   - Set up authentication and API keys
   - Configure categories for NFL prediction jobs

2. **Busta CLI Integration**
   - Create Cronicle plugins that call `busta` commands
   - Environment-aware job execution (dev vs prod)
   - Standardized logging and error handling

3. **Scheduler Configuration**
   - Weekly NFL prediction pipeline schedule
   - Game day specific triggers
   - Season start/end automated workflows

4. **Monitoring & Notifications**
   - Web hooks for Slack/Discord notifications
   - Email alerts for critical failures
   - Dashboard integration with existing web interface

### **Schedule Template (Weekly NFL Pattern)**

```javascript
// Tuesday: Data Pipeline Start
{
  "title": "NFL Data Bronze Normalization",
  "schedule": "0 8 * * 2",  // Tuesdays 8 AM
  "plugin": "busta-pipeline",
  "params": {
    "command": "pipeline data normalize-bronze",
    "environment": "production"
  }
}

// Tuesday: Silver Integration  
{
  "title": "NFL Data Silver Integration",
  "schedule": "0 14 * * 2", // Tuesdays 2 PM
  "plugin": "busta-pipeline", 
  "params": {
    "command": "pipeline data integrate-silver",
    "environment": "production"
  }
}

// Wednesday: Feature Generation
{
  "title": "NFL Feature Generation - All Markets",
  "schedule": "0 9 * * 3",  // Wednesdays 9 AM
  "plugin": "busta-features",
  "params": {
    "markets": ["moneyline", "ats", "ou"],
    "environment": "production"
  }
}

// Thursday: Model Training
{
  "title": "NFL Model Training - All Markets", 
  "schedule": "0 10 * * 4", // Thursdays 10 AM
  "plugin": "busta-training",
  "params": {
    "markets": ["moneyline", "ats", "ou"],
    "environment": "production"
  }
}

// Friday: Predictions Generation
{
  "title": "NFL Weekly Predictions",
  "schedule": "0 11 * * 5", // Fridays 11 AM
  "plugin": "busta-predict",
  "params": {
    "week": "current",
    "environment": "production"
  }
}

// Monday Night: Results Tracking
{
  "title": "NFL Results Tracking",
  "schedule": "0 23 * * 1", // Mondays 11 PM
  "plugin": "busta-results",
  "params": {
    "week": "previous", 
    "environment": "production"
  }
}
```

## 📋 **Implementation Plan**

### **Phase 1: Cronicle Setup (2 SP)**
- [ ] Install Cronicle on existing server
- [ ] Configure authentication and API keys  
- [ ] Set up server groups for production/development
- [ ] Create categories for NFL prediction jobs

### **Phase 2: Plugin Development (2 SP)**
- [ ] Create `busta-pipeline` plugin for data pipeline jobs
- [ ] Create `busta-features` plugin for feature generation
- [ ] Create `busta-training` plugin for model training
- [ ] Create `busta-predict` plugin for predictions
- [ ] Create `busta-results` plugin for results tracking

### **Phase 3: Schedule Configuration (1 SP)**
- [ ] Configure weekly NFL prediction schedule
- [ ] Set up development environment schedules
- [ ] Configure notifications and webhooks
- [ ] Test failover and retry mechanisms

## 🎯 **Acceptance Criteria**

### **Core Functionality**
- [ ] Cronicle web interface accessible and functional
- [ ] All NFL prediction pipeline jobs scheduled and running
- [ ] Real-time job status visible in Cronicle UI
- [ ] Failed jobs trigger appropriate notifications
- [ ] Environment isolation working (prod/dev separate)

### **Integration Quality**
- [ ] Busta CLI commands execute properly via Cronicle plugins
- [ ] Job logs captured and accessible through web interface
- [ ] Historical job performance data available
- [ ] API endpoints functional for external integration

### **Operational Requirements**
- [ ] Weekly NFL schedule runs automatically
- [ ] Manual job triggers work for ad-hoc runs
- [ ] Backup server failover tested and working
- [ ] Documentation updated with Cronicle workflows

## 🚀 **Benefits**

### **Immediate Value**
- **Visual Monitoring**: See all pipeline jobs in one interface
- **Automated Scheduling**: No more manual cron management
- **Real-time Status**: Know immediately when jobs fail
- **Environment Safety**: Clear separation of prod/dev schedules

### **Long-term Value**
- **Scalability**: Easy to add new jobs and servers
- **Reliability**: Built-in failover and retry mechanisms  
- **Analytics**: Historical performance data for optimization
- **Team Collaboration**: Shared visibility into system operations

## 🔗 **Dependencies**

- **Prerequisites**: Dual repository environment (INF-013) ✅
- **Infrastructure**: Existing server resources (sufficient)
- **Integrations**: Slack/Discord webhook setup (optional)
- **Documentation**: Update operational procedures

## 📊 **Success Metrics**

- **Reliability**: >99% successful job completion rate
- **Visibility**: 100% of pipeline jobs visible in Cronicle
- **Response Time**: <5 minutes to detect and alert on failures
- **User Adoption**: Development team using Cronicle for job management

---

**Story Ready for Implementation** 🚀

## 📝 Implementation Notes

### Current Progress
- ✅ **Cronicle Installation**: v0.9.90 successfully installed at `/opt/cronicle/`
- ✅ **Service Setup**: Running on port 3012 with admin/admin credentials  
- ✅ **Plugin Development**: 5 enhanced NFL prediction plugins created and deployed
- ✅ **Web Interface**: Accessible at http://localhost:3012
- ✅ **API Integration**: Setup script created for automated configuration
- ✅ **Environment Management**: Integrated with bb-env tool for dual repository support
- ✅ **Repository Integration**: bb-env tool added to repository with Makefile support
- ✅ **Plugin Enhancement**: Upgraded to follow official Cronicle best practices
- 🔄 **Event Configuration**: Ready for manual web interface configuration
- ⏳ **Integration Testing**: Ready for complete workflow validation

### Enhanced Plugin Features
- **Performance Metrics**: Real-time tracking of execution time and resource usage
- **Custom Data Tables**: Statistics display in Cronicle web interface
- **Error Handling**: HTTP-style error codes and comprehensive error reporting
- **Environment Variables**: Full integration with Cronicle's job environment system
- **Progress Reporting**: Detailed progress updates with context information
- **Resource Monitoring**: CPU, memory, and system resource tracking
- **bb-env Integration**: Seamless environment switching with fallback support
- **Statistics Collection**: Game tracking, accuracy metrics, ROI analysis
- **Enhanced Logging**: Detailed job logs with structured output

### Environment Management Integration
- **bb-env Tool**: Repository-based environment switcher (`./bb-env` or globally via `make setup-env`)
- **Global Access**: `make setup-env` installs bb-env to `~/.local/bin/` for team use
- **Documentation**: Comprehensive guide in `docs/BB_ENV.md`
- **Cronicle Integration**: Plugins detect environment automatically via bb-env configuration

### API Access
- **Base URL**: http://localhost:3012/api/app/
- **API Key**: cb19aebe9fce8ce6ed51f9e3ea010643
- **Authentication**: Key-based access for programmatic control
- **Setup Script**: `/home/bustabook/nfl-predictions/cronicle-plugins/setup-nfl-events.sh`

### Next Steps
1. **Manual Configuration**: Use web interface to create categories and events
2. **Plugin Refinement**: Fix environment activation for seamless execution
3. **Integration Testing**: Validate complete weekly workflow
4. **Documentation**: Update operational procedures with Cronicle workflows
