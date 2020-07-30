using JSON
using Plots
plotly()

profiles = JSON.parsefile("raw_results.json")
println(profiles[1])