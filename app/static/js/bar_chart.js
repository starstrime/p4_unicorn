//  Unicorn
//  Roster: Ivan Chen, Emaan Asif, Jake Liu, Jalen Chen
//  SoftDev pd4
//  2026
const duration   = 250;
const n          = 12;
const k          = 10;
const barSize    = 48;
const marginTop  = 16;
const marginRight  = 6;
const marginBottom = 6;
const marginLeft   = 0;
const width      = 800;

function formatNumber(val) {
  return d3.format("$,.1f")(val) + "B";
}

const formatDate = d3.utcFormat("%b %Y");
const tickFormat = undefined;

function textTween(a, b) {
  const i = d3.interpolateNumber(a, b);
  return function(t) {
    this.textContent = formatNumber(i(t));
  };
}

function color(data) {
  const scale = d3.scaleOrdinal(d3.schemeTableau10);
  if (data.some(d => d.category !== undefined)) {
    const categoryByName = new Map(data.map(d => [d.name, d.category]));
    scale.domain(categoryByName.values());
    return d => scale(categoryByName.get(d.name));
  }
  return d => scale(d.name);
}

function computeAll(data) {
  const names      = new Set(data.map(d => d.name));
  const height     = marginTop + barSize * n + marginBottom;

  const x = d3.scaleLinear([0, 1], [marginLeft, width - marginRight]);
  const y = d3.scaleBand()
      .domain(d3.range(n + 1))
      .rangeRound([marginTop, marginTop + barSize * (n + 1 + 0.1)])
      .padding(0.1);

  const colorFn = color(data);

  const datevalues = Array.from(
    d3.rollup(data, ([d]) => d.value, d => +d.date, d => d.name)
  )
    .map(([date, data]) => [new Date(date), data])
    .sort(([a], [b]) => d3.ascending(a, b));

  function rank(value) {
    const ranked = Array.from(names, name => ({ name, value: value(name) }));
    ranked.sort((a, b) => d3.descending(a.value, b.value));
    for (let i = 0; i < ranked.length; ++i) ranked[i].rank = Math.min(n, i);
    return ranked;
  }

  const keyframes = [];
  let ka, a, kb, b;
  for ([[ka, a], [kb, b]] of d3.pairs(datevalues)) {
    for (let i = 0; i < k; ++i) {
      const t = i / k;
      keyframes.push([
        new Date(ka * (1 - t) + kb * t),
        rank(name => (a.get(name) || 0) * (1 - t) + (b.get(name) || 0) * t)
      ]);
    }
  }
  keyframes.push([new Date(kb), rank(name => b.get(name) || 0)]);

  const nameframes  = d3.groups(keyframes.flatMap(([, data]) => data), d => d.name);
  const prev        = new Map(nameframes.flatMap(([, data]) => d3.pairs(data, (a, b) => [b, a])));
  const next        = new Map(nameframes.flatMap(([, data]) => d3.pairs(data)));

  return { x, y, height, keyframes, prev, next, colorFn };
}

function bars(svg, { n, colorFn, y, x, prev, next }) {
  let bar = svg.append("g")
      .attr("fill-opacity", 0.6)
    .selectAll("rect");

  return ([date, data], transition) => bar = bar
    .data(data.slice(0, n), d => d.name)
    .join(
      enter => enter.append("rect")
        .attr("fill", colorFn)
        .attr("height", y.bandwidth())
        .attr("x", x(0))
        .attr("y", d => y((prev.get(d) || d).rank))
        .attr("width", d => x((prev.get(d) || d).value) - x(0)),
      update => update,
      exit => exit.transition(transition).remove()
        .attr("y", d => y((next.get(d) || d).rank))
        .attr("width", d => x((next.get(d) || d).value) - x(0))
    )
    .call(bar => bar.transition(transition)
      .attr("y", d => y(d.rank))
      .attr("width", d => x(d.value) - x(0)));
}

function labels(svg, { n, x, prev, y, next }) {
  let label = svg.append("g")
      .style("font", "bold 12px sans-serif")
      .style("font-variant-numeric", "tabular-nums")
      .attr("text-anchor", "end")
    .selectAll("text");

  return ([date, data], transition) => label = label
    .data(data.slice(0, n), d => d.name)
    .join(
      enter => enter.append("text")
        .attr("transform", d => `translate(${x((prev.get(d) || d).value)},${y((prev.get(d) || d).rank)})`)
        .attr("y", y.bandwidth() / 2)
        .attr("x", -6)
        .attr("dy", "-0.25em")
        .text(d => d.name)
        .call(text => text.append("tspan")
          .attr("fill-opacity", 0.7)
          .attr("font-weight", "normal")
          .attr("x", -6)
          .attr("dy", "1.15em")),
      update => update,
      exit => exit.transition(transition).remove()
        .attr("transform", d => `translate(${x((next.get(d) || d).value)},${y((next.get(d) || d).rank)})`)
        .call(g => g.select("tspan").tween("text", d => textTween(d.value, (next.get(d) || d).value)))
    )
    .call(bar => bar.transition(transition)
      .attr("transform", d => `translate(${x(d.value)},${y(d.rank)})`)
      .call(g => g.select("tspan").tween("text", d => textTween((prev.get(d) || d).value, d.value))));
}

function axis(svg, { x, y }) {
  const g = svg.append("g")
      .attr("transform", `translate(0,${marginTop})`);

  const axisFn = d3.axisTop(x)
      .ticks(width / 160, tickFormat)
      .tickSizeOuter(0)
      .tickSizeInner(-barSize * (n + y.padding()));

  return (_, transition) => {
    g.transition(transition).call(axisFn);
    g.select(".tick:first-of-type text").remove();
    g.selectAll(".tick:not(:first-of-type) line").attr("stroke", "#d595959");
    g.select(".domain").remove();
  };
}

function ticker(svg, { keyframes }) {
  const now = svg.append("text")
      .style("font", `bold ${barSize}px sans-serif`)
      .style("font-variant-numeric", "tabular-nums")
      .attr("text-anchor", "end")
      .attr("x", width - 6)
      .attr("y", marginTop + barSize * (n - 0.45))
      .attr("dy", "0.32em")
      .attr("fill", "white")
      .text(formatDate(keyframes[0][0]));

  return ([date], transition) => {
    transition.end().then(() => now.text(formatDate(date)));
  };
}

function addTitle(svg) {
  svg.append("text")
      .attr("x", marginLeft)
      .attr("y", marginTop + barSize * 0.5)
      .attr("fill", "#555")
      .style("font", "bold 14px sans-serif")
      .text("Market Cap ($B)");
}

async function drawChart(data) {
  const { x, y, height, keyframes, prev, next, colorFn } = computeAll(data);

  const svg = d3.create("svg")
      .attr("viewBox", [0, 0, width, height])
      .attr("width", width)
      .attr("height", height)
      .attr("style", "max-width: 100%; height: auto;");

  const updateBars   = bars(svg,   { n, colorFn, y, x, prev, next });
  const updateAxis   = axis(svg,   { x, y });
  const updateLabels = labels(svg, { n, x, prev, y, next });
  const updateTicker = ticker(svg, { keyframes });

  const chartDiv = document.getElementById("chart");
  chartDiv.innerHTML = "";
  chartDiv.appendChild(svg.node());

  for (const keyframe of keyframes) {
    const transition = svg.transition()
        .duration(duration)
        .ease(d3.easeLinear);

    x.domain([0, keyframe[1][0].value]);

    updateAxis(keyframe, transition);
    updateBars(keyframe, transition);
    updateLabels(keyframe, transition);
    updateTicker(keyframe, transition);

    await transition.end();
  }
}

async function fetchData() {
  const tickers = document.getElementById("tickers").value;
  const start   = document.getElementById("start").value;
  const end     = document.getElementById("end").value;

  const res = await fetch(`/bar_chart_data?tickers=${tickers}&start=${start}&end=${end}`);
  const raw = await res.json();

  return raw.map(d => ({
    ...d,
    date:  new Date(d.date),
    value: +d.value
  }));
}

function createReplayButton() {
  const btn = document.createElement("button");
  btn.textContent = "Replay";
  btn.onclick = () => fetchData().then(drawChart);
  document.getElementById("replay-btn").appendChild(btn);
}

async function loadChart() {
  const data = await fetchData();
  drawChart(data);
}

document.addEventListener("DOMContentLoaded", () => {
  createReplayButton();
  loadChart();
});
