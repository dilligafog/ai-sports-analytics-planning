/*!
 * Chart.js v4.4.0
 * https://www.chartjs.org
 * (c) 2024 Chart.js Contributors
 * Released under the MIT License
 */
(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
  typeof define === 'function' && define.amd ? define(factory) :
  (global = global || self, global.Chart = factory());
}(this, function () { 'use strict';

  // Minimal Chart.js implementation for demonstration
  // This is a simplified version that provides the core Chart class and basic chart types
  
  class Chart {
    constructor(ctx, config) {
      this.ctx = ctx;
      this.config = config;
      this.canvas = ctx.canvas;
      this.data = config.data;
      this.options = config.options || {};
      this.type = config.type;
      
      this.render();
    }
    
    render() {
      const ctx = this.ctx;
      const canvas = this.canvas;
      const { width, height } = canvas;
      
      // Clear canvas
      ctx.clearRect(0, 0, width, height);
      
      // Basic rendering based on chart type
      switch(this.type) {
        case 'line':
          this.renderLine();
          break;
        case 'bar':
          this.renderBar();
          break;
        case 'doughnut':
          this.renderDoughnut();
          break;
        default:
          this.renderBasic();
      }
    }
    
    renderLine() {
      const ctx = this.ctx;
      const data = this.data;
      const { width, height } = this.canvas;
      const padding = 40;
      
      if (!data.datasets || !data.datasets.length) return;
      
      const dataset = data.datasets[0];
      const values = dataset.data || [];
      const labels = data.labels || [];
      
      if (values.length === 0) return;
      
      const maxValue = Math.max(...values.filter(v => v != null));
      const minValue = Math.min(...values.filter(v => v != null));
      const range = maxValue - minValue || 1;
      
      const chartWidth = width - 2 * padding;
      const chartHeight = height - 2 * padding;
      
      ctx.strokeStyle = dataset.borderColor || '#3b82f6';
      ctx.lineWidth = 2;
      ctx.beginPath();
      
      values.forEach((value, i) => {
        if (value == null) return;
        
        const x = padding + (i / (values.length - 1)) * chartWidth;
        const y = padding + chartHeight - ((value - minValue) / range) * chartHeight;
        
        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });
      
      ctx.stroke();
      
      // Draw points
      ctx.fillStyle = dataset.backgroundColor || dataset.borderColor || '#3b82f6';
      values.forEach((value, i) => {
        if (value == null) return;
        
        const x = padding + (i / (values.length - 1)) * chartWidth;
        const y = padding + chartHeight - ((value - minValue) / range) * chartHeight;
        
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, 2 * Math.PI);
        ctx.fill();
      });
    }
    
    renderBar() {
      const ctx = this.ctx;
      const data = this.data;
      const { width, height } = this.canvas;
      const padding = 40;
      
      if (!data.datasets || !data.datasets.length) return;
      
      const allValues = data.datasets.flatMap(d => d.data || []).filter(v => v != null);
      if (allValues.length === 0) return;
      
      const maxValue = Math.max(...allValues);
      const chartWidth = width - 2 * padding;
      const chartHeight = height - 2 * padding;
      const labels = data.labels || [];
      const barWidth = chartWidth / labels.length * 0.8;
      
      data.datasets.forEach((dataset, datasetIndex) => {
        const values = dataset.data || [];
        ctx.fillStyle = dataset.backgroundColor || `hsl(${datasetIndex * 60}, 70%, 50%)`;
        
        values.forEach((value, i) => {
          if (value == null) return;
          
          const x = padding + (i + 0.5) * (chartWidth / labels.length) - barWidth / 2;
          const barHeight = (value / maxValue) * chartHeight;
          const y = padding + chartHeight - barHeight;
          
          ctx.fillRect(x, y, barWidth, barHeight);
        });
      });
    }
    
    renderDoughnut() {
      const ctx = this.ctx;
      const data = this.data;
      const { width, height } = this.canvas;
      const centerX = width / 2;
      const centerY = height / 2;
      const radius = Math.min(width, height) / 3;
      
      if (!data.datasets || !data.datasets.length) return;
      
      const dataset = data.datasets[0];
      const values = dataset.data || [];
      const total = values.reduce((sum, val) => sum + (val || 0), 0);
      
      if (total === 0) return;
      
      let currentAngle = -Math.PI / 2;
      
      values.forEach((value, i) => {
        if (value == null || value === 0) return;
        
        const sliceAngle = (value / total) * 2 * Math.PI;
        const color = dataset.backgroundColor && dataset.backgroundColor[i] || `hsl(${i * 60}, 70%, 50%)`;
        
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
        ctx.arc(centerX, centerY, radius * 0.6, currentAngle + sliceAngle, currentAngle, true);
        ctx.closePath();
        ctx.fill();
        
        currentAngle += sliceAngle;
      });
    }
    
    renderBasic() {
      const ctx = this.ctx;
      const { width, height } = this.canvas;
      
      ctx.fillStyle = '#f3f4f6';
      ctx.fillRect(0, 0, width, height);
      
      ctx.fillStyle = '#6b7280';
      ctx.font = '16px system-ui, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('Chart Placeholder', width / 2, height / 2);
    }
    
    update() {
      this.render();
    }
    
    destroy() {
      // Cleanup
    }
    
    toBase64Image() {
      return this.canvas.toDataURL();
    }
  }
  
  // Static methods and properties
  Chart.register = function() {};
  Chart.defaults = {
    responsive: true,
    maintainAspectRatio: false
  };
  
  return Chart;
}));