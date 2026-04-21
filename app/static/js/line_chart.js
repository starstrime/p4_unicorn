//  Unicorn
//  Roster: Ivan Chen, Emaan Asif, Jake Liu, Jalen Chen
//  SoftDev pd4
//  2026

function createBasisSlider(data, onChange) {
  const [min, max] = d3.extent(data, d => d.Close);

  const wrapper = document.createElement("label");
  wrapper.textContent = "Basis: ";

  const input = document.createElement("input");
  input.type  = "range";
  input.min   = min;
  input.max   = max;
  input.value = data[0].Close;
  input.step  = 0.01;

  const display = document.createElement("span");
  display.textContent = data[0].Close.toFixed(2);

  input.addEventListener("input", () => {
    display.textContent = (+input.value).toFixed(2);
    onChange(+input.value);
  });

  wrapper.appendChild(input);
  wrapper.appendChild(display);

  return {
    element:  wrapper,
    getValue: () => +input.value
  };
}

function drawChart(data, basis) {

  const width        = 928;
  const height       = 600;
  const marginTop    = 20;
  const marginRight  = 30;
  const marginBottom = 30;
  const marginLeft   = 50;

  const x = d3.scaleUtc()
      .domain(d3.extent(data, d => d.Date))
      .range([marginLeft, width - marginRight]);

  const y = d3.scaleLog()
      .domain([d3.min(data, d => d.Close / basis * 0.9), d3.max(data, d => d.Close / basis / 0.9)])
      .rangeRound([height - marginBottom, marginTop]);

  const f      = d3.format("+.0%");
  const format = x => x === 1 ? "0%" : f(x - 1);

  const svg = d3.create("svg").attr("viewBox", [0, 0, width, height]);

  svg.append("g")
      .attr("transform", `translate(0,${y(1)})`)
      .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0))
      .call(g => g.select(".domain").remove());

  svg.append("g")
      .attr("transform", `translate(${marginLeft},0)`)
      .call(d3.axisLeft(y)
          .tickValues(d3.ticks(...y.domain(), 10))
          .tickFormat(format))
      .call(g => g.selectAll(".tick line").clone()
          .attr("stroke-opacity", d => d === 1 ? null : 0.2)
          .attr("x2", width - marginLeft - marginRight))
      .call(g => g.select(".domain").remove());

  const line = d3.line()
      .x(d => x(d.Date))
      .y(d => y(d.Close / basis));

  svg.append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 1.5)
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round")
      .attr("d", line);

  return svg.node();
}


async function fetchData() {
  const ticker = document.getElementById("ticker").value;
  const start  = document.getElementById("start").value;
  const end    = document.getElementById("end").value;

  const res = await fetch(`/stock_data?ticker=${ticker}&start=${start}&end=${end}`);
  const raw = await res.json();

  return raw.map(d => ({
    Date:  new Date(d.Date),
    Close: +d.Close
  }));
}


let _data    = [];
let _slider  = null;

function redraw(basis) {
  if (!_data.length) return;
  const chartDiv = document.getElementById("chart");
  chartDiv.innerHTML = "";
  chartDiv.appendChild(drawChart(_data, basis));
}

async function loadChart() {
  _data = await fetchData();

  const controlsDiv = document.getElementById("controls");
  controlsDiv.innerHTML = "";
  _slider = createBasisSlider(_data, basis => redraw(basis));
  controlsDiv.appendChild(_slider.element);

  redraw(_slider.getValue());
}

document.addEventListener("DOMContentLoaded", () => {
  loadChart();
});