import { Runtime, Inspector } from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";
import define from "./bar_chart.js";

const runtime = new Runtime();
runtime.module(define, name => {
  if (name === "chart") return new Inspector(document.querySelector("#chart"));
  if (name === "viewof replay") return new Inspector(document.querySelector("#replay"));
});