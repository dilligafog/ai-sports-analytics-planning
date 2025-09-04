/**
 * Daily Dev Story Dashboard
 * GitHub Pages dashboard for visualizing daily GitHub activity
 */

class DashboardApp {
  constructor() {
    this.data = null;
    this.filteredData = null;
    this.charts = {};
    this.debounceTimeout = null;
    
    // Initialize the app
    this.init();
  }
  
  async init() {
    try {
      this.showLoading();
      await this.loadData();
      this.setupEventListeners();
      this.renderInitialUI();
      this.updateDashboard();
      this.hideLoading();
    } catch (error) {
      console.error('Failed to initialize dashboard:', error);
      this.showError('Failed to load dashboard data. Please refresh the page.');
    }
  }
  
  async loadData() {
    try {
      const response = await fetch('./work_review.json');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      this.data = await response.json();
      this.normalizeData();
    } catch (error) {
      console.error('Error loading data:', error);
      throw new Error('Failed to load data from work_review.json');
    }
  }
  
  normalizeData() {
    // Create date->repo map for quick filtering
    this.dateRepoMap = new Map();
    
    if (this.data.daily) {
      this.data.daily.forEach(dayData => {
        this.dateRepoMap.set(dayData.date, dayData.repos || []);
      });
    }
    
    // Extract unique repo names
    this.repoNames = [...new Set(
      this.data.daily?.flatMap(day => day.repos?.map(repo => repo.name) || []) || []
    )];
    
    // Set default filters
    this.filters = {
      repos: new Set(this.repoNames),
      dateRange: {
        start: this.data.metadata?.window?.start_date,
        end: this.data.metadata?.window?.end_date
      }
    };
    
    this.applyFilters();
  }
  
  applyFilters() {
    if (!this.data.daily) {
      this.filteredData = { daily: [], aggregates: this.data.aggregates };
      return;
    }
    
    const filteredDaily = this.data.daily
      .filter(day => {
        const date = new Date(day.date);
        const startDate = new Date(this.filters.dateRange.start);
        const endDate = new Date(this.filters.dateRange.end);
        return date >= startDate && date <= endDate;
      })
      .map(day => ({
        ...day,
        repos: day.repos?.filter(repo => this.filters.repos.has(repo.name)) || []
      }));
    
    this.filteredData = {
      ...this.data,
      daily: filteredDaily
    };
  }
  
  setupEventListeners() {
    // Repo filter checkboxes
    document.addEventListener('change', (e) => {
      if (e.target.classList.contains('repo-filter')) {
        this.handleRepoFilterChange(e.target);
      }
    });
    
    // Select all button
    const selectAllBtn = document.getElementById('select-all-repos');
    if (selectAllBtn) {
      selectAllBtn.addEventListener('click', () => this.toggleAllRepos());
    }
    
    // Date range controls
    const dateSlider = document.getElementById('date-range-slider');
    if (dateSlider) {
      dateSlider.addEventListener('input', () => this.handleDateRangeChange());
    }
    
    // Quick date buttons
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('date-quick-btn')) {
        this.handleQuickDateSelect(e.target);
      }
    });
    
    // Chart export buttons
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('chart-export-btn')) {
        this.exportChart(e.target.dataset.chartId);
      }
    });
    
    // Repo detail dropdown
    const repoSelect = document.getElementById('repo-detail-select');
    if (repoSelect) {
      repoSelect.addEventListener('change', () => this.updateRepoDetail());
    }
    
    // Info banner close
    const bannerClose = document.getElementById('info-banner-close');
    if (bannerClose) {
      bannerClose.addEventListener('click', () => this.closeBanner());
    }
    
    // Window resize for responsive charts
    window.addEventListener('resize', this.debounce(() => {
      this.resizeCharts();
    }, 250));
  }
  
  renderInitialUI() {
    this.renderHeader();
    this.renderControls();
    this.renderRepoDetail();
    this.showInfoBanner();
  }
  
  renderHeader() {
    const title = document.getElementById('dashboard-title');
    const subtitle = document.getElementById('dashboard-subtitle');
    
    if (title && this.data.metadata) {
      title.textContent = `Daily Dev Story — ${this.data.metadata.owner}`;
    }
    
    if (subtitle && this.data.metadata?.window) {
      const startDate = new Date(this.data.metadata.window.start_date).toLocaleDateString();
      const endDate = new Date(this.data.metadata.window.end_date).toLocaleDateString();
      subtitle.textContent = `${startDate} → ${endDate}`;
    }
  }
  
  renderControls() {
    this.renderRepoFilters();
    this.renderDateControls();
  }
  
  renderRepoFilters() {
    const container = document.getElementById('repo-filters');
    if (!container) return;
    
    container.innerHTML = '';
    
    this.repoNames.forEach(repoName => {
      const checkbox = document.createElement('div');
      checkbox.className = 'repo-checkbox';
      
      const isChecked = this.filters.repos.has(repoName);
      
      checkbox.innerHTML = `
        <input type="checkbox" 
               id="repo-${repoName}" 
               class="repo-filter" 
               data-repo="${repoName}"
               ${isChecked ? 'checked' : ''}>
        <label for="repo-${repoName}">${repoName}</label>
      `;
      
      container.appendChild(checkbox);
    });
  }
  
  renderDateControls() {
    const slider = document.getElementById('date-range-slider');
    if (!slider || !this.data.daily) return;
    
    const dates = this.data.daily.map(d => d.date).sort();
    slider.min = 0;
    slider.max = dates.length - 1;
    slider.value = dates.length - 1; // Default to full range
    
    // Set up quick buttons
    const quickButtons = document.querySelectorAll('.date-quick-btn');
    quickButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.date-quick-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
      });
    });
  }
  
  renderRepoDetail() {
    const select = document.getElementById('repo-detail-select');
    if (!select) return;
    
    select.innerHTML = '<option value="">Select a repository</option>';
    
    this.repoNames.forEach(repoName => {
      const option = document.createElement('option');
      option.value = repoName;
      option.textContent = repoName;
      select.appendChild(option);
    });
    
    if (this.repoNames.length > 0) {
      select.value = this.repoNames[0];
      this.updateRepoDetail();
    }
  }
  
  showInfoBanner() {
    const banner = document.getElementById('info-banner');
    const content = document.getElementById('info-banner-content');
    
    if (banner && content && this.data.metadata?.collection_notes) {
      content.textContent = this.data.metadata.collection_notes;
      banner.classList.remove('hidden');
    }
  }
  
  closeBanner() {
    const banner = document.getElementById('info-banner');
    if (banner) {
      banner.classList.add('hidden');
    }
  }
  
  updateDashboard() {
    this.debouncedUpdate();
  }
  
  debouncedUpdate() {
    clearTimeout(this.debounceTimeout);
    this.debounceTimeout = setTimeout(() => {
      this.applyFilters();
      this.updateKPIs();
      this.updateCharts();
      this.updateRepoDetail();
    }, 150);
  }
  
  updateKPIs() {
    const kpis = this.calculateKPIs();
    
    // Update each KPI card
    Object.entries(kpis).forEach(([key, value]) => {
      const element = document.getElementById(`kpi-${key}`);
      if (element) {
        element.textContent = this.formatKPIValue(key, value);
      }
    });
  }
  
  calculateKPIs() {
    if (!this.filteredData.daily) {
      return this.getEmptyKPIs();
    }
    
    const totals = {
      commits: 0,
      prsOpened: 0,
      prsMerged: 0,
      linesAdded: 0,
      linesDeleted: 0,
      workflowRuns: 0,
      workflowSuccesses: 0,
      prMergeTimes: [],
      issuCloseTimes: [],
      aiCommitMarkers: 0,
      aiPRMarkers: 0,
      botEvents: 0
    };
    
    this.filteredData.daily.forEach(day => {
      day.repos.forEach(repo => {
        totals.commits += repo.commits?.count || 0;
        totals.prsOpened += repo.prs?.opened_count || 0;
        totals.prsMerged += repo.prs?.merged_count || 0;
        totals.linesAdded += repo.commits?.lines_added || 0;
        totals.linesDeleted += repo.commits?.lines_deleted || 0;
        totals.workflowRuns += repo.workflows?.runs_count || 0;
        
        if (repo.workflows?.success_rate != null && repo.workflows?.runs_count > 0) {
          totals.workflowSuccesses += repo.workflows.success_rate * repo.workflows.runs_count;
        }
        
        if (repo.prs?.time_to_merge_seconds_median) {
          totals.prMergeTimes.push(repo.prs.time_to_merge_seconds_median);
        }
        
        if (repo.issues?.time_to_close_seconds_median) {
          totals.issuCloseTimes.push(repo.issues.time_to_close_seconds_median);
        }
        
        totals.aiCommitMarkers += repo.ai_signals?.commit_markers || 0;
        totals.aiPRMarkers += repo.ai_signals?.pr_markers || 0;
        totals.botEvents += repo.ai_signals?.bot_actor_events || 0;
      });
    });
    
    return {
      commits: totals.commits,
      prsOpened: totals.prsOpened,
      prsMerged: totals.prsMerged,
      linesAdded: totals.linesAdded,
      linesDeleted: totals.linesDeleted,
      workflowSuccessRate: totals.workflowRuns > 0 ? (totals.workflowSuccesses / totals.workflowRuns) * 100 : 0,
      medianPRMergeTime: this.calculateMedian(totals.prMergeTimes),
      medianIssueCloseTime: this.calculateMedian(totals.issuCloseTimes),
      aiMarkers: totals.aiCommitMarkers + totals.aiPRMarkers,
      aiSignalScore: totals.aiCommitMarkers * 1 + totals.aiPRMarkers * 2 + totals.botEvents * 1
    };
  }
  
  getEmptyKPIs() {
    return {
      commits: 0,
      prsOpened: 0,
      prsMerged: 0,
      linesAdded: 0,
      linesDeleted: 0,
      workflowSuccessRate: 0,
      medianPRMergeTime: 0,
      medianIssueCloseTime: 0,
      aiMarkers: 0,
      aiSignalScore: 0
    };
  }
  
  formatKPIValue(key, value) {
    if (value == null || value === undefined) return '—';
    
    switch (key) {
      case 'workflowSuccessRate':
        return `${Math.round(value)}%`;
      case 'medianPRMergeTime':
      case 'medianIssueCloseTime':
        return this.formatDuration(value);
      default:
        return value.toLocaleString();
    }
  }
  
  formatDuration(seconds) {
    if (!seconds || seconds === 0) return '—';
    
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    
    if (hours > 0) {
      return `${hours}h ${minutes.toString().padStart(2, '0')}m`;
    } else {
      return `${minutes}m`;
    }
  }
  
  calculateMedian(values) {
    if (!values || values.length === 0) return 0;
    
    const sorted = [...values].sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    
    return sorted.length % 2 === 0
      ? (sorted[mid - 1] + sorted[mid]) / 2
      : sorted[mid];
  }
  
  updateCharts() {
    this.renderCommitsChart();
    this.renderLinesChart();
    this.renderPRVelocityChart();
    this.renderPRSizeChart();
    this.renderAISignalsChart();
    this.renderWorkflowChart();
  }
  
  renderCommitsChart() {
    const canvas = document.getElementById('commits-chart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const data = this.prepareCommitsData();
    
    if (this.charts.commits) {
      this.charts.commits.destroy();
    }
    
    this.charts.commits = new Chart(ctx, {
      type: 'bar',
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { title: { display: true, text: 'Date' } },
          y: { title: { display: true, text: 'Commits' }, beginAtZero: true }
        },
        plugins: {
          title: { display: false },
          legend: { display: true }
        }
      }
    });
  }
  
  renderLinesChart() {
    const canvas = document.getElementById('lines-chart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const data = this.prepareLinesData();
    
    if (this.charts.lines) {
      this.charts.lines.destroy();
    }
    
    this.charts.lines = new Chart(ctx, {
      type: 'bar',
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { title: { display: true, text: 'Date' } },
          y: { title: { display: true, text: 'Lines Changed' } }
        },
        plugins: {
          title: { display: false },
          legend: { display: true }
        }
      }
    });
  }
  
  renderPRVelocityChart() {
    const canvas = document.getElementById('pr-velocity-chart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const data = this.preparePRVelocityData();
    
    if (this.charts.prVelocity) {
      this.charts.prVelocity.destroy();
    }
    
    this.charts.prVelocity = new Chart(ctx, {
      type: 'line',
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { title: { display: true, text: 'Date' } },
          y: { title: { display: true, text: 'Hours' }, beginAtZero: true }
        },
        plugins: {
          title: { display: false },
          legend: { display: false }
        }
      }
    });
  }
  
  renderPRSizeChart() {
    const canvas = document.getElementById('pr-size-chart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const data = this.preparePRSizeData();
    
    if (this.charts.prSize) {
      this.charts.prSize.destroy();
    }
    
    this.charts.prSize = new Chart(ctx, {
      type: 'doughnut',
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: { display: false },
          legend: { display: true, position: 'bottom' }
        }
      }
    });
  }
  
  renderAISignalsChart() {
    const canvas = document.getElementById('ai-signals-chart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const data = this.prepareAISignalsData();
    
    if (this.charts.aiSignals) {
      this.charts.aiSignals.destroy();
    }
    
    this.charts.aiSignals = new Chart(ctx, {
      type: 'line',
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { title: { display: true, text: 'Date' } },
          y: { title: { display: true, text: 'AI Signals' }, beginAtZero: true }
        },
        plugins: {
          title: { display: false },
          legend: { display: true }
        }
      }
    });
  }
  
  renderWorkflowChart() {
    const canvas = document.getElementById('workflow-chart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const data = this.prepareWorkflowData();
    
    if (this.charts.workflow) {
      this.charts.workflow.destroy();
    }
    
    this.charts.workflow = new Chart(ctx, {
      type: 'line',
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { title: { display: true, text: 'Date' } },
          y: { title: { display: true, text: 'Success Rate (%)' }, beginAtZero: true, max: 100 }
        },
        plugins: {
          title: { display: false },
          legend: { display: false }
        }
      }
    });
  }
  
  prepareCommitsData() {
    const labels = this.filteredData.daily.map(day => new Date(day.date).toLocaleDateString());
    const datasets = [];
    
    this.repoNames.forEach((repoName, index) => {
      if (!this.filters.repos.has(repoName)) return;
      
      const data = this.filteredData.daily.map(day => {
        const repo = day.repos.find(r => r.name === repoName);
        return repo?.commits?.count || 0;
      });
      
      datasets.push({
        label: repoName,
        data: data,
        backgroundColor: this.getRepoColor(index, 0.7),
        borderColor: this.getRepoColor(index, 1),
        borderWidth: 1
      });
    });
    
    return { labels, datasets };
  }
  
  prepareLinesData() {
    const labels = this.filteredData.daily.map(day => new Date(day.date).toLocaleDateString());
    
    const addedData = this.filteredData.daily.map(day => {
      return day.repos.reduce((sum, repo) => sum + (repo.commits?.lines_added || 0), 0);
    });
    
    const deletedData = this.filteredData.daily.map(day => {
      return -(day.repos.reduce((sum, repo) => sum + (repo.commits?.lines_deleted || 0), 0));
    });
    
    return {
      labels,
      datasets: [
        {
          label: 'Lines Added',
          data: addedData,
          backgroundColor: 'rgba(34, 197, 94, 0.7)',
          borderColor: 'rgba(34, 197, 94, 1)',
          borderWidth: 1
        },
        {
          label: 'Lines Deleted',
          data: deletedData,
          backgroundColor: 'rgba(239, 68, 68, 0.7)',
          borderColor: 'rgba(239, 68, 68, 1)',
          borderWidth: 1
        }
      ]
    };
  }
  
  preparePRVelocityData() {
    const labels = this.filteredData.daily.map(day => new Date(day.date).toLocaleDateString());
    
    const data = this.filteredData.daily.map(day => {
      const mergeTimes = day.repos
        .filter(repo => repo.prs?.time_to_merge_seconds_median)
        .map(repo => repo.prs.time_to_merge_seconds_median);
      
      if (mergeTimes.length === 0) return null;
      
      const median = this.calculateMedian(mergeTimes);
      return Math.round(median / 3600 * 10) / 10; // Convert to hours with 1 decimal
    });
    
    return {
      labels,
      datasets: [{
        label: 'Median PR Merge Time (hours)',
        data: data,
        borderColor: 'rgba(59, 130, 246, 1)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        borderWidth: 2,
        fill: true
      }]
    };
  }
  
  preparePRSizeData() {
    const sizes = { small: 0, medium: 0, large: 0, xlarge: 0 };
    
    this.filteredData.daily.forEach(day => {
      day.repos.forEach(repo => {
        if (repo.prs?.size_distribution) {
          Object.entries(repo.prs.size_distribution).forEach(([size, count]) => {
            sizes[size] = (sizes[size] || 0) + count;
          });
        }
      });
    });
    
    return {
      labels: ['Small', 'Medium', 'Large', 'X-Large'],
      datasets: [{
        data: [sizes.small, sizes.medium, sizes.large, sizes.xlarge],
        backgroundColor: [
          'rgba(34, 197, 94, 0.7)',
          'rgba(245, 158, 11, 0.7)',
          'rgba(249, 115, 22, 0.7)',
          'rgba(239, 68, 68, 0.7)'
        ],
        borderColor: [
          'rgba(34, 197, 94, 1)',
          'rgba(245, 158, 11, 1)',
          'rgba(249, 115, 22, 1)',
          'rgba(239, 68, 68, 1)'
        ],
        borderWidth: 1
      }]
    };
  }
  
  prepareAISignalsData() {
    const labels = this.filteredData.daily.map(day => new Date(day.date).toLocaleDateString());
    
    const commitMarkers = this.filteredData.daily.map(day => {
      return day.repos.reduce((sum, repo) => sum + (repo.ai_signals?.commit_markers || 0), 0);
    });
    
    const prMarkers = this.filteredData.daily.map(day => {
      return day.repos.reduce((sum, repo) => sum + (repo.ai_signals?.pr_markers || 0), 0);
    });
    
    const botEvents = this.filteredData.daily.map(day => {
      return day.repos.reduce((sum, repo) => sum + (repo.ai_signals?.bot_actor_events || 0), 0);
    });
    
    return {
      labels,
      datasets: [
        {
          label: 'Commit Markers',
          data: commitMarkers,
          borderColor: 'rgba(59, 130, 246, 1)',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          borderWidth: 2
        },
        {
          label: 'PR Markers',
          data: prMarkers,
          borderColor: 'rgba(16, 185, 129, 1)',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          borderWidth: 2
        },
        {
          label: 'Bot Events',
          data: botEvents,
          borderColor: 'rgba(245, 158, 11, 1)',
          backgroundColor: 'rgba(245, 158, 11, 0.1)',
          borderWidth: 2
        }
      ]
    };
  }
  
  prepareWorkflowData() {
    const labels = this.filteredData.daily.map(day => new Date(day.date).toLocaleDateString());
    
    const data = this.filteredData.daily.map(day => {
      const successRates = day.repos
        .filter(repo => repo.workflows?.success_rate != null)
        .map(repo => repo.workflows.success_rate * 100);
      
      if (successRates.length === 0) return null;
      
      return successRates.reduce((sum, rate) => sum + rate, 0) / successRates.length;
    });
    
    return {
      labels,
      datasets: [{
        label: 'Success Rate (%)',
        data: data,
        borderColor: 'rgba(34, 197, 94, 1)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        borderWidth: 2,
        fill: true
      }]
    };
  }
  
  getRepoColor(index, alpha = 1) {
    const colors = [
      `rgba(59, 130, 246, ${alpha})`,   // blue
      `rgba(34, 197, 94, ${alpha})`,    // green
      `rgba(245, 158, 11, ${alpha})`,   // amber
      `rgba(239, 68, 68, ${alpha})`,    // red
      `rgba(139, 92, 246, ${alpha})`,   // violet
      `rgba(236, 72, 153, ${alpha})`,   // pink
      `rgba(14, 165, 233, ${alpha})`,   // sky
      `rgba(16, 185, 129, ${alpha})`    // emerald
    ];
    return colors[index % colors.length];
  }
  
  updateRepoDetail() {
    const select = document.getElementById('repo-detail-select');
    const selectedRepo = select?.value;
    
    if (!selectedRepo) return;
    
    this.updateActiveHours(selectedRepo);
    this.updateRepoTable(selectedRepo);
  }
  
  updateActiveHours(repoName) {
    const container = document.getElementById('active-hours-list');
    if (!container) return;
    
    // Get active hours for the selected repo across all days
    const allHours = [];
    this.filteredData.daily.forEach(day => {
      const repo = day.repos.find(r => r.name === repoName);
      if (repo?.work_patterns?.active_hours) {
        allHours.push(...repo.work_patterns.active_hours);
      }
    });
    
    // Count frequency and get top 3
    const hourCounts = {};
    allHours.forEach(hour => {
      hourCounts[hour] = (hourCounts[hour] || 0) + 1;
    });
    
    const topHours = Object.entries(hourCounts)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 3)
      .map(([hour]) => parseInt(hour));
    
    container.innerHTML = '';
    
    if (topHours.length === 0) {
      container.innerHTML = '<span class="text-muted">No activity data</span>';
      return;
    }
    
    topHours.forEach(hour => {
      const span = document.createElement('span');
      span.className = 'active-hour';
      span.textContent = `${hour}:00`;
      container.appendChild(span);
    });
  }
  
  updateRepoTable(repoName) {
    const tbody = document.getElementById('repo-table-body');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    this.filteredData.daily.forEach(day => {
      const repo = day.repos.find(r => r.name === repoName);
      
      if (!repo) return;
      
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${new Date(day.date).toLocaleDateString()}</td>
        <td>${repo.commits?.count || 0}</td>
        <td>${repo.prs?.opened_count || 0}</td>
        <td>${repo.prs?.merged_count || 0}</td>
        <td>+${repo.commits?.lines_added || 0}</td>
        <td>-${repo.commits?.lines_deleted || 0}</td>
      `;
      
      tbody.appendChild(row);
    });
  }
  
  handleRepoFilterChange(checkbox) {
    const repoName = checkbox.dataset.repo;
    
    if (checkbox.checked) {
      this.filters.repos.add(repoName);
    } else {
      this.filters.repos.delete(repoName);
    }
    
    this.updateDashboard();
  }
  
  toggleAllRepos() {
    const checkboxes = document.querySelectorAll('.repo-filter');
    const allChecked = Array.from(checkboxes).every(cb => cb.checked);
    
    checkboxes.forEach(checkbox => {
      checkbox.checked = !allChecked;
      const repoName = checkbox.dataset.repo;
      
      if (checkbox.checked) {
        this.filters.repos.add(repoName);
      } else {
        this.filters.repos.delete(repoName);
      }
    });
    
    this.updateDashboard();
  }
  
  handleDateRangeChange() {
    // Simple implementation - would need more complex logic for actual date range slider
    this.updateDashboard();
  }
  
  handleQuickDateSelect(button) {
    const days = parseInt(button.dataset.days);
    if (!days || !this.data.daily) return;
    
    const allDates = this.data.daily.map(d => d.date).sort();
    const endDate = allDates[allDates.length - 1];
    const startIndex = Math.max(0, allDates.length - days);
    const startDate = allDates[startIndex];
    
    this.filters.dateRange = { start: startDate, end: endDate };
    this.updateDashboard();
  }
  
  exportChart(chartId) {
    const chart = this.charts[chartId];
    if (!chart) return;
    
    const url = chart.toBase64Image();
    const link = document.createElement('a');
    link.download = `${chartId}-chart.png`;
    link.href = url;
    link.click();
  }
  
  resizeCharts() {
    Object.values(this.charts).forEach(chart => {
      if (chart && chart.resize) {
        chart.resize();
      }
    });
  }
  
  showLoading() {
    document.body.classList.add('loading');
    
    // Show skeleton loaders
    document.querySelectorAll('.skeleton').forEach(el => {
      el.style.display = 'block';
    });
  }
  
  hideLoading() {
    document.body.classList.remove('loading');
    
    // Hide skeleton loaders
    document.querySelectorAll('.skeleton').forEach(el => {
      el.style.display = 'none';
    });
  }
  
  showError(message) {
    const container = document.querySelector('.container');
    if (!container) return;
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    container.insertBefore(errorDiv, container.firstChild);
  }
  
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }
}

// Initialize the dashboard when the page loads
document.addEventListener('DOMContentLoaded', () => {
  new DashboardApp();
});