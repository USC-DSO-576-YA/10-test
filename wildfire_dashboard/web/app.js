const $ = (id) => document.getElementById(id);
const state = { meta: null, view: "overview", request: 0 };
const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const palette = ["#c66f49", "#397d68", "#6b91a0", "#9e806b", "#aa9e63", "#6d8e6d", "#987f9d", "#cc9761", "#6c9d9c", "#b77778", "#8ba278", "#7f8da8"];
const config = { responsive: true, displayModeBar: false, scrollZoom: false, topojsonURL: `${window.location.origin}/topojson/` };
const fmt = (value, digits = 0) => value == null ? "No observations" : Number(value).toLocaleString("en-US", { maximumFractionDigits: digits, minimumFractionDigits: digits });

function layout(extra = {}) {
  return {
    paper_bgcolor: "rgba(0,0,0,0)", plot_bgcolor: "rgba(0,0,0,0)",
    font: { family: '-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif', size: 11, color: "#718578" },
    margin: { l: 45, r: 17, t: 21, b: 47 }, showlegend: false,
    xaxis: { gridcolor: "#eef1ec", zeroline: false, linecolor: "#e6ece4", tickfont: { size: 10 } },
    yaxis: { gridcolor: "#eef1ec", zeroline: false, linecolor: "#e6ece4", tickfont: { size: 10 }, tickformat: "~s" },
    hoverlabel: { bgcolor: "#1c3d32", bordercolor: "#1c3d32", font: { color: "white" } },
    ...extra,
  };
}

function plot(id, traces, options = {}) {
  Plotly.react(id, traces, layout(options), config);
}

function line(id, rows, field, color, name, suffix = "") {
  plot(id, [{ x: rows.map(r => r.year), y: rows.map(r => r[field]), type: "scatter", mode: "lines+markers", name,
    line: { color, width: 2.5, shape: "linear" }, marker: { color, size: 5 },
    hovertemplate: `%{x}: %{y:,.0f}${suffix}<extra></extra>` }],
    { xaxis: { dtick: Math.max(1, Math.ceil(rows.length / 9)), gridcolor: "#eef1ec", zeroline: false }, yaxis: { gridcolor: "#eef1ec", zeroline: false, tickformat: "~s" } });
}

function drawOverview(data) {
  const m = data.metrics;
  $("stat-fires").textContent = fmt(m.fires);
  $("stat-acres").textContent = fmt(m.acres);
  $("stat-median").textContent = m.median_size == null ? "No observations" : `${fmt(m.median_size, 2)} ac`;
  $("stat-unknown").textContent = m.unknown_pct == null ? "No observations" : `${fmt(m.unknown_pct, 1)}%`;
  const selectedState = state.meta.states.find(s => s.code === $("state").value);
  $("place-name").textContent = `· ${selectedState?.name || ""}`;
  $("selection-caption").textContent = `${$("start-year").value}–${$("end-year").value} · ${$("cause").selectedOptions[0].textContent}`;
  $("empty-overview").classList.toggle("hidden", m.fires !== 0);
  $("overview-charts").classList.toggle("hidden", m.fires === 0);
  drawDrought(data.drought);
  if (m.fires === 0) return;

  line("annual-fires", data.annual, "fires", "#ce6840", "Recorded fires");
  line("annual-acres", data.annual, "acres", "#397d68", "Final reported acres", " acres");
  plot("seasonality", [{ type: "bar", x: months, y: data.seasonality.map(r => r.percent), marker: { color: "#418269", cornerradius: 3 },
    customdata: data.seasonality.map(r => r.fires), hovertemplate: "%{x}: %{y:.1f}%<br>%{customdata:,} fires<extra></extra>" }],
    { yaxis: { gridcolor: "#eef1ec", zeroline: false, ticksuffix: "%" } });

  const causeRows = [...data.causes].reverse();
  plot("causes-chart", [{ type: "bar", orientation: "h", x: causeRows.map(r => r.fires), y: causeRows.map(r => r.reported_cause),
    marker: { color: "#c57650", cornerradius: 2 }, customdata: causeRows.map(r => r.acres),
    hovertemplate: "%{y}<br>%{x:,} fires<br>%{customdata:,.0f} final acres<extra></extra>" }],
    { margin: { l: 172, r: 16, t: 16, b: 41 }, yaxis: { automargin: true, gridcolor: "#eef1ec" }, xaxis: { tickformat: "~s", gridcolor: "#eef1ec", zeroline: false } });

  plot("sizes-chart", [{ type: "bar", x: data.sizes.map(r => r.size_class), y: data.sizes.map(r => r.fires),
    customdata: data.sizes.map(r => [r.label, r.acres]), marker: { color: "#6b91a0", cornerradius: 2 },
    hovertemplate: "%{customdata[0]}<br>%{y:,} fires<br>%{customdata[1]:,.0f} final acres<extra></extra>" }],
    { xaxis: { gridcolor: "#eef1ec", title: { text: "Final fire-size class", font: { size: 10 } } } });

  const causeNames = [...new Set(data.cause_yearly.map(r => r.reported_cause))].sort();
  const annual = data.annual.map(r => r.year);
  const byCauseYear = new Map(data.cause_yearly.map(r => [`${r.reported_cause}|${r.year}`, r]));
  const areaTraces = causeNames.map((cause, i) => ({ type: "scatter", mode: "lines", name: cause, stackgroup: "one", groupnorm: "percent",
    x: annual, y: annual.map(year => byCauseYear.get(`${cause}|${year}`)?.fires || 0),
    line: { width: 0.5, color: palette[i % palette.length] }, hovertemplate: `${cause}<br>%{x}: %{y:,} fires<extra></extra>` }));
  plot("composition-chart", areaTraces,
    { showlegend: true, legend: { orientation: "h", y: -0.27, x: 0, font: { size: 9 }, itemwidth: 30 },
      margin: { l: 43, r: 14, t: 17, b: 77 }, yaxis: { range: [0, 100], ticksuffix: "%", gridcolor: "#eef1ec", zeroline: false } });

  const showMonthly = Array.isArray(data.monthly) && data.monthly.length > 0;
  $("monthly-section").classList.toggle("hidden", !showMonthly);
  if (showMonthly) drawMonthly(data.monthly);
}

function drawMonthly(rows) {
  const x = rows.map(r => r.month.slice(0, 10));
  plot("monthly-trend", [
    { type: "scatter", mode: "lines", name: "Recorded fires", x, y: rows.map(r => r.fires), line: { color: "#ce6840", width: 1.7 }, hovertemplate: "%{x}<br>%{y:,} fires<extra></extra>" },
    { type: "scatter", mode: "lines", name: "Three-month average", x, y: rows.map(r => r.average_3m), line: { color: "#397d68", width: 2.8 }, hovertemplate: "%{x}<br>%{y:,.1f} average<extra></extra>" },
  ], { showlegend: true, legend: { orientation: "h", y: -0.28, x: 0 }, margin: { l: 48, r: 17, t: 17, b: 67 }, xaxis: { type: "date", gridcolor: "#eef1ec" } });
  plot("monthly-change", [{ type: "bar", x, y: rows.map(r => r.change), marker: { color: rows.map(r => r.change >= 0 ? "#c57953" : "#6c9a86") },
    hovertemplate: "%{x}<br>%{y:+,} fires from prior month<extra></extra>" }], { xaxis: { type: "date", gridcolor: "#eef1ec" } });
  plot("monthly-running", [{ type: "scatter", mode: "lines", x, y: rows.map(r => r.running), fill: "tozeroy", fillcolor: "rgba(57,125,104,.13)",
    line: { color: "#397d68", width: 2 }, hovertemplate: "%{x}<br>%{y:,} running fires<extra></extra>" }], { xaxis: { type: "date", gridcolor: "#eef1ec" } });
}

function drawComparison(data) {
  const metric = $("metric").value;
  const label = $("metric").selectedOptions[0].textContent;
  const allRows = data.states;
  const rows = allRows.filter(r => r[metric] != null);
  const ranked = [...rows].sort((a, b) => b[metric] - a[metric]);
  const top = ranked.slice(0, 12).reverse();
  plot("map-chart", [{ type: "choropleth", locationmode: "USA-states", locations: rows.map(r => r.state), z: rows.map(r => r[metric]),
    text: rows.map(r => r.state_name), customdata: rows.map(r => [r.fires, r.acres]),
    colorscale: [[0, "#f4e9cf"], [.35, "#e8b583"], [.7, "#d0794c"], [1, "#a94835"]], marker: { line: { color: "white", width: .8 } },
    colorbar: { title: { text: label, side: "top", font: { size: 10 } }, thickness: 10, len: .52, x: .92, tickfont: { size: 9 } },
    hovertemplate: "%{text}<br>" + label + ": %{z:,.2f}<br>%{customdata[0]:,} recorded fires<br>%{customdata[1]:,.0f} acres burned<extra></extra>" }],
    { geo: { scope: "usa", projection: { type: "albers usa" }, showlakes: false, bgcolor: "rgba(0,0,0,0)" }, margin: { l: 0, r: 0, t: 0, b: 0 } });
  plot("rank-chart", [{ type: "bar", orientation: "h", x: top.map(r => r[metric]), y: top.map(r => r.state_name),
    marker: { color: "#c57650", cornerradius: 2 }, hovertemplate: `%{y}<br>${label}: %{x:,.2f}<extra></extra>` }],
    { margin: { l: 120, r: 16, t: 17, b: 43 }, xaxis: { tickformat: "~s", gridcolor: "#eef1ec", zeroline: false }, yaxis: { automargin: true, gridcolor: "#eef1ec" } });
  $("table-count").textContent = `${allRows.length} jurisdictions (states + DC)`;
  $("states-table").replaceChildren(...[...allRows].sort((a, b) => a.state_name.localeCompare(b.state_name)).map(row => {
    const tr = document.createElement("tr");
    for (const value of [row.state_name, fmt(row.fires), fmt(row.acres), fmt(row.median_size, 2), row.unknown_pct == null ? "—" : `${fmt(row.unknown_pct, 1)}%`]) {
      const td = document.createElement("td"); td.textContent = value; tr.append(td);
    }
    return tr;
  }));
}

async function getJson(path) {
  const response = await fetch(path);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || `Request failed (${response.status})`);
  return data;
}

async function refresh() {
  if (state.view === "methods" || !state.meta) return;
  const request = ++state.request;
  $("loading").classList.remove("hidden"); $("error").classList.add("hidden");
  try {
    let data;
    const years = new URLSearchParams({ start: $("start-year").value, end: $("end-year").value });
    if (state.view === "overview") {
      years.set("state", $("state").value);
      years.set("cause", $("cause").value);
      data = await getJson(`/api/overview?${years}`);
    } else data = await getJson(`/api/comparison?${years}`);
    if (request !== state.request) return;
    if (state.view === "overview") drawOverview(data); else drawComparison(data);
  } catch (error) {
    if (request === state.request) { $("error").textContent = error.message; $("error").classList.remove("hidden"); }
  } finally {
    if (request === state.request) $("loading").classList.add("hidden");
  }
}

function setView(view) {
  state.view = view;
  state.request++;
  document.querySelectorAll(".nav-button").forEach(button => button.classList.toggle("active", button.dataset.view === view));
  for (const name of ["overview", "comparison", "methods"]) $(`${name}-view`).classList.toggle("hidden", name !== view);
  document.querySelectorAll(".overview-filter").forEach(element => element.classList.toggle("hidden", view !== "overview"));
  document.querySelectorAll(".compare-filter").forEach(element => element.classList.toggle("hidden", view !== "comparison"));
  $("loading").classList.add("hidden"); $("error").classList.add("hidden");
  $("start-year").closest(".filter-bar").classList.toggle("hidden", view === "methods");
  refresh();
}

async function start() {
  try {
    state.meta = await getJson("/api/meta");
    for (const year of Array.from({ length: state.meta.years[1] - state.meta.years[0] + 1 }, (_, i) => state.meta.years[0] + i)) {
      for (const id of ["start-year", "end-year"]) $(id).add(new Option(year, year));
    }
    $("start-year").value = state.meta.years[0]; $("end-year").value = state.meta.years[1];
    for (const item of state.meta.states) $("state").add(new Option(item.name, item.code));
    $("state").value = "CA";
    for (const cause of state.meta.causes) $("cause").add(new Option(cause, cause));
    $("record-count").textContent = fmt(state.meta.records);
    document.querySelectorAll(".nav-button").forEach(button => button.addEventListener("click", () => setView(button.dataset.view)));
    for (const id of ["start-year", "end-year", "state", "cause", "metric"]) $(id).addEventListener("change", () => {
      if (Number($("start-year").value) > Number($("end-year").value)) {
        if (id === "start-year") $("end-year").value = $("start-year").value;
        else $("start-year").value = $("end-year").value;
      }
      refresh();
    });
    refresh();
  } catch (error) { $("error").textContent = error.message; $("error").classList.remove("hidden"); }
}
start();

function drawDrought(rows) {
  const available = rows.some(r => r.drought_pct != null);
  $("drought-message").textContent = available
    ? "Compare monthly fire counts with drought coverage. The two axes use different units."
    : "No drought observations for this selection. Choose California and years from 2000 onward.";
  $("drought-chart").classList.toggle("hidden", !available);
  if (!available) return;
  const x = rows.map(r => r.month.slice(0, 10));
  plot("drought-chart", [
    {type: "bar", name: "Recorded fires", x, y: rows.map(r => r.fires), marker: {color: "#ce6840"}, opacity: .65,
     hovertemplate: "%{x}<br>%{y:,} fires<extra></extra>"},
    {type: "scatter", mode: "lines", name: "Area in drought (D1–D4)", x, y: rows.map(r => r.drought_pct), yaxis: "y2", connectgaps: false,
     line: {color: "#397d68", width: 2}, hovertemplate: "%{x}<br>%{y:.1f}% of state area<extra></extra>"}
  ], {showlegend: true, legend: {orientation: "h", y: -.3}, margin: {l: 60, r: 65, t: 20, b: 85},
      xaxis: {type: "date"}, yaxis: {title: {text: "Recorded fires"}, rangemode: "tozero"},
      yaxis2: {title: {text: "Area in drought (%)"}, overlaying: "y", side: "right", range: [0, 100], showgrid: false}});
}
