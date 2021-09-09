using JSON
using DataStructures
using Plots
plotlyjs()

profiles = JSON.parsefile("raw_results.json")

function topping_popularity(profiles)
    toppings = DefaultDict(0)
    for profile in profiles, topping in profile["order"]
        toppings[topping] += 1
    end
    toppings
end

topping_dict = topping_popularity(profiles)
display(histogram(keys(topping_dict), values(topping_dict)))

# x = rand(10)
# y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# println(x)
# println(y)
# plt = plot(x, y)
# display(plt), gui()
