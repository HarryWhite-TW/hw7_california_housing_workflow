const results = window.HW7_RESULTS || { status: "not-run" };

const formatNumber = (value, digits = 2) => {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "Pending";
  return Number(value).toLocaleString(undefined, {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  });
};

const status = document.querySelector("[data-status]");
const metricGrid = document.querySelector("[data-metrics]");
const datasetMeta = document.querySelector("[data-dataset-meta]");

if (results.status === "complete" && results.metrics) {
  status.textContent = "Workflow verified";
  status.dataset.state = "complete";
  datasetMeta.textContent = `${formatNumber(results.rows, 0)} rows · ${results.columns} columns · ${results.features} features`;

  const cards = [
    ["Test R²", formatNumber(results.metrics.r2, 4)],
    ["MAE", formatNumber(results.metrics.mae)],
    ["RMSE", formatNumber(results.metrics.rmse)],
    ["CV R² mean", formatNumber(results.metrics.cv_r2_mean, 4)],
  ];
  metricGrid.innerHTML = cards
    .map(([label, value]) => `<article class="metric-card"><span>${label}</span><strong>${value}</strong></article>`)
    .join("");
} else {
  status.textContent = "Awaiting real California Housing run";
  datasetMeta.textContent = "The repository baseline is ready. Execute the workflow to publish real metrics.";
  metricGrid.innerHTML = `<article class="metric-card pending"><span>Current state</span><strong>Not run</strong></article>`;
}
