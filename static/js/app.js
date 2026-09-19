/* ══════════════════════════════════════════════════════════════
   🌐 AeroSense — app.js
   All dynamic behaviour: fetch, render, animate
   ══════════════════════════════════════════════════════════════ */

'use strict';

// ─────────────────────────────────────────────────────────────
//  Constants & Config
// ─────────────────────────────────────────────────────────────
const GAUGE_CIRCUMFERENCE = 2 * Math.PI * 90; // ≈ 565.49
const AQI_MAX_SCALE       = 500;               // AQI value that = 100% ring fill

const POLLUTANT_META = {
  pm25: { label: 'PM₂.₅', icon: '🫁', unit: 'μg/m³', max: 250,  htmlLabel: 'PM<sub>2.5</sub>' },
  pm10: { label: 'PM₁₀',  icon: '💨', unit: 'μg/m³', max: 350,  htmlLabel: 'PM<sub>10</sub>' },
  co:   { label: 'CO',    icon: '🔥', unit: 'mg/m³', max: 10,   htmlLabel: 'CO' },
  so2:  { label: 'SO₂',   icon: '⚗️', unit: 'μg/m³', max: 80,   htmlLabel: 'SO<sub>2</sub>' },
  no2:  { label: 'NO₂',   icon: '🌫️', unit: 'μg/m³', max: 80,   htmlLabel: 'NO<sub>2</sub>' },
  o3:   { label: 'O₃',    icon: '☀️', unit: 'μg/m³', max: 180,  htmlLabel: 'O<sub>3</sub>' },
};

// AQI band colours for the bar fill
const AQI_COLORS = [
  { max: 50,   color: '#22C55E' },
  { max: 100,  color: '#84CC16' },
  { max: 200,  color: '#F59E0B' },
  { max: 300,  color: '#F97316' },
  { max: 400,  color: '#EF4444' },
  { max: 500,  color: '#991B1B' },
  { max: Infinity, color: '#581C87' },
];

// ─────────────────────────────────────────────────────────────
//  State
// ─────────────────────────────────────────────────────────────
let currentCity    = 'Bangalore';
let activeCounters = [];   // cancel running count-up animations

// ─────────────────────────────────────────────────────────────
//  Utility helpers
// ─────────────────────────────────────────────────────────────

function aqiColor(aqi) {
  const v = parseFloat(aqi) || 0;
  return (AQI_COLORS.find(b => v <= b.max) || AQI_COLORS.at(-1)).color;
}

/** Linear interpolation of AQI (0–500+) → percentage position on scale bar */
function aqiToPercent(aqi) {
  const breakpoints = [0, 50, 100, 200, 300, 400, 500];
  const v = Math.min(parseFloat(aqi) || 0, 520);
  for (let i = 0; i < breakpoints.length - 1; i++) {
    if (v <= breakpoints[i + 1]) {
      const segSize = 100 / (breakpoints.length - 1);
      const frac    = (v - breakpoints[i]) / (breakpoints[i + 1] - breakpoints[i]);
      return Math.min(((i + frac) * segSize), 99);
    }
  }
  return 99;
}

/**
 * Animate a number from `start` to `end`.
 * @param {HTMLElement} el
 * @param {number}      end
 * @param {number}      duration  ms
 * @param {boolean}     integer
 */
function countUp(el, end, duration = 900, integer = true) {
  const start     = 0;
  const startTime = performance.now();
  let   rafId;

  function step(now) {
    const elapsed  = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    // Ease out cubic
    const eased    = 1 - Math.pow(1 - progress, 3);
    const current  = start + (end - start) * eased;
    el.textContent = integer ? Math.round(current) : current.toFixed(1);
    if (progress < 1) rafId = requestAnimationFrame(step);
  }
  rafId = requestAnimationFrame(step);
  activeCounters.push(rafId);
}

function showToast(msg) {
  const toast   = document.getElementById('errorToast');
  const msgSpan = document.getElementById('errorToastMsg');
  msgSpan.textContent = msg;
  toast.classList.add('visible');
  setTimeout(() => toast.classList.remove('visible'), 6000);
}

function hideToast() {
  document.getElementById('errorToast').classList.remove('visible');
}

// ─────────────────────────────────────────────────────────────
//  Skeleton / loading states
// ─────────────────────────────────────────────────────────────
function showLoading() {
  // Gauge
  document.getElementById('skeletonGauge').style.display = 'flex';
  document.getElementById('gaugeWrap').style.display     = 'none';
  // Prediction
  document.getElementById('skeletonPred').style.display = 'block';
  document.getElementById('predBody').style.display     = 'none';
  // Reset pollutants to skeleton cards
  const grid = document.getElementById('pollutantsGrid');
  grid.innerHTML = Array(6).fill(
    '<div class="pollutant-card skeleton-card">' +
    '<div class="skel-line"></div>' +
    '<div class="skel-line skel-short"></div></div>'
  ).join('');
}

function hideLoading() {
  document.getElementById('skeletonGauge').style.display = 'none';
  document.getElementById('gaugeWrap').style.display     = 'flex';
  document.getElementById('skeletonPred').style.display  = 'none';
  document.getElementById('predBody').style.display      = 'flex';
}

// ─────────────────────────────────────────────────────────────
//  Gauge animation
// ─────────────────────────────────────────────────────────────
function animateGauge(aqi, color) {
  const progress = document.getElementById('gaugeProgress');
  const ratio    = Math.min(aqi / AQI_MAX_SCALE, 1);
  const offset   = GAUGE_CIRCUMFERENCE * (1 - ratio);

  // Reset first, then animate (triggers CSS transition)
  progress.style.strokeDashoffset = GAUGE_CIRCUMFERENCE;
  progress.style.stroke = color;

  // Glow effect on container
  const container = document.querySelector('.gauge-ring-container');
  container.style.filter = `drop-shadow(0 0 18px ${color}55)`;

  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      progress.style.strokeDashoffset = offset;
    });
  });
}

// ─────────────────────────────────────────────────────────────
//  Render: Current AQI
// ─────────────────────────────────────────────────────────────
function renderCurrentAQI(current) {
  const { aqi, category, color, dominant_pollutant, timestamp } = current;

  // Gauge ring
  animateGauge(aqi, color);

  // AQI number count-up
  const aqiEl = document.getElementById('gaugeAqiValue');
  aqiEl.textContent = '0';
  countUp(aqiEl, aqi, 1000);

  // Category & meta
  document.getElementById('gaugeCategory').textContent    = category;
  document.getElementById('gaugeCategory').style.color    = color;
  document.getElementById('dominantPollutant').textContent = dominant_pollutant.toUpperCase();

  const tsEl = document.querySelector('#lastUpdated span');
  if (tsEl) tsEl.textContent = 'Updated ' + timestamp;
}

// ─────────────────────────────────────────────────────────────
//  Render: Pollutant Cards
// ─────────────────────────────────────────────────────────────
function renderPollutants(pollutants) {
  const grid = document.getElementById('pollutantsGrid');
  grid.innerHTML = '';

  Object.entries(POLLUTANT_META).forEach(([key, meta], i) => {
    const raw   = pollutants[key] ?? 0;
    const value = parseFloat(raw).toFixed(key === 'co' ? 2 : 1);
    const pct   = Math.min((raw / meta.max) * 100, 100);
    const color = aqiColor(raw / meta.max * 200);   // rough colour mapping

    const card = document.createElement('div');
    card.className = 'pollutant-card';
    card.style.animationDelay = `${i * 60}ms`;
    card.innerHTML = `
      <div class="pollutant-header">
        <div class="pollutant-icon">${meta.icon}</div>
        <div class="pollutant-name">${meta.htmlLabel}</div>
      </div>
      <div class="pollutant-value">
        <span class="pval" data-target="${value}">0</span>
        <span class="pollutant-unit">${meta.unit}</span>
      </div>
      <div class="pollutant-bar-wrap">
        <div class="pollutant-bar" data-pct="${pct}" style="background:${color}; width:0%"></div>
      </div>`;

    grid.appendChild(card);

    // Animate value and bar after DOM paint
    requestAnimationFrame(() => {
      const valEl = card.querySelector('.pval');
      countUp(valEl, parseFloat(value), 800, false);
      setTimeout(() => {
        card.querySelector('.pollutant-bar').style.width = pct + '%';
      }, 80 + i * 60);
    });
  });
}

// ─────────────────────────────────────────────────────────────
//  Render: Prediction
// ─────────────────────────────────────────────────────────────
function renderPrediction(prediction) {
  const { aqi, category, color, health_advice, recommendations } = prediction;

  // AQI box
  const numEl = document.getElementById('predAqiNumber');
  const box   = document.getElementById('predAqiBox');
  numEl.textContent = '0';
  countUp(numEl, aqi, 1000);
  box.style.borderColor  = color;
  box.style.background   = color + '18';

  // Category badge
  const badge = document.getElementById('predCategoryBadge');
  badge.textContent     = category;
  badge.style.background = color;

  // Health advice
  document.getElementById('predAdvice').textContent = health_advice;

  // Recommendations
  const recContainer = document.getElementById('recommendations');
  if (recommendations && recommendations.length) {
    recContainer.innerHTML = `
      <div class="recommendations-title">Health Recommendations</div>
      <ul class="rec-list">
        ${recommendations.map(r => `<li>${r}</li>`).join('')}
      </ul>`;
  } else {
    recContainer.innerHTML = '';
  }
}

// ─────────────────────────────────────────────────────────────
//  Render: AQI Scale markers
// ─────────────────────────────────────────────────────────────
function renderScaleMarkers(currentAQI, predictedAQI) {
  const currentMarker = document.getElementById('currentMarker');
  const predMarker    = document.getElementById('predMarker');

  if (currentAQI !== null && currentAQI !== undefined) {
    const pct = aqiToPercent(currentAQI);
    currentMarker.style.left    = pct + '%';
    currentMarker.style.display = 'flex';
  }

  if (predictedAQI !== null && predictedAQI !== undefined) {
    const pct = aqiToPercent(predictedAQI);
    predMarker.style.left    = pct + '%';
    predMarker.style.display = 'flex';
  }
}

// ─────────────────────────────────────────────────────────────
//  Main data fetch & render pipeline
// ─────────────────────────────────────────────────────────────
async function fetchAndRender(city) {
  // Cancel any running count-up animations
  activeCounters.forEach(cancelAnimationFrame);
  activeCounters = [];

  showLoading();
  hideToast();

  try {
    const res  = await fetch(`/api/aqi?city=${encodeURIComponent(city)}`);
    const data = await res.json();

    if (!data.success) {
      showToast(data.error || 'Failed to load AQI data for ' + city);
      return;
    }

    hideLoading();

    renderCurrentAQI(data.current);
    renderPollutants(data.current.pollutants);
    renderPrediction(data.prediction);
    renderScaleMarkers(data.current.aqi, data.prediction.aqi);

  } catch (err) {
    showToast('Network error — please check your connection and try again.');
    console.error('[🌐 AeroSense] fetch error:', err);
  }
}

// ─────────────────────────────────────────────────────────────
//  Intersection Observer — staggered section fade-in
// ─────────────────────────────────────────────────────────────
function initFadeObserver() {
  const sections = document.querySelectorAll('.fade-section');
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.08 }
  );
  sections.forEach((s, i) => {
    s.style.transitionDelay = `${i * 80}ms`;
    observer.observe(s);
  });
}

// ─────────────────────────────────────────────────────────────
//  Boot
// ─────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initFadeObserver();

  const select = document.getElementById('citySelect');

  // Read default city set by Flask (via selected attribute or first option)
  currentCity = select.value || 'Bangalore';

  // Initial load
  fetchAndRender(currentCity);

  // City change
  select.addEventListener('change', () => {
    currentCity = select.value;
    fetchAndRender(currentCity);
  });
});
