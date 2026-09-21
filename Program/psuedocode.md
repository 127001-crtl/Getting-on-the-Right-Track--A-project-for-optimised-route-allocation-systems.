## Pseudocode for the Development of the Solution
Design-section pseudocode, feeding directly into Technical Solution later.

### Data Structures
Here is an example pseudocode that showcases the possible data structures I will be using in my technical solution. These abstract data structures map directly onto the ones shown at section 3.3.2 [here](../main.pdf#page=25).  
```py
class Delivery:
    #stores all relevant information for deliveries
    id, demand, time_window_start, time_window_end, 
    service_duration, location #(lat, lon)

class Vehicle:
    #stores all relevant information for vehicles
    id, capacity, depot_location, 
    shift_start, shift_end, max_route_duration #(optional)

class Route:
    vehicle, total_load, total_distance, 
    total_duration, stops #(ordered list of Delivery)
```
The use of classes here helps me 
- Keep my code DRY (Don't Repeat Yourself).
- Makes code easier to maintain, reuse, and debug.
- Provides a clear structure to my solution.
- Allows me to build reusable structures to my code 

OOP is an example of object-oriented decomposition. While functional or procedural paradigms break a system down by what it does (actions and functions), OOP breaks a system down by what things exist (entities and objects). This should help to critically reduce chaotic dependencies across the entire codebase.

---
### Phase 1: Construct Routes
this can be seen here (process 4 at [here](../main.pdf#page=26) at page 26.)
```py
function construct_routes(deliveries, vehicles, distance_matrix, depot):
    unallocated = copy(deliveries)
    routes = []

    for vehicle in vehicles:
        if unallocated is empty: break
        route = new Route(vehicle)
        location, time, load = depot, vehicle.shift_start, 0

        while True:
            candidates = [d for d in unallocated if
                load + d.demand <= vehicle.capacity
                and time + travel_time(location, d.location) <= d.time_window_end]

            if candidates is empty: break

            next_stop = closest(candidates, location, distance_matrix)
            arrival = time + travel_time(location, next_stop.location)
            start_service = max(arrival, next_stop.time_window_start)  # wait if early

            route.add(next_stop, start_service)
            time = start_service + next_stop.service_duration
            load += next_stop.demand
            location = next_stop.location
            unallocated.remove(next_stop)

        routes.append(route)

    return routes, unallocated
```
a delivery that would break capacity or arrive too late is simply never in `candidates` — it can't get added, so there's nothing to reject later. ![validate](../Images/D2/validate%20orders.svg)


---

### Phase 2 — Check constraints 
This selection will aim to match process 5 in [here](../main.pdf#page=26) at page 26.

Now this only has to check things that genuinely can't be known per stop during construction:
```py
function check_constraints(routes, unallocated):
    violations = []
    if unallocated is not empty:
        violations.append("Unallocated deliveries", unallocated)
    for route in routes:
        if route.total_duration > route.vehicle.max_route_duration:
            violations.append(route, "Shift limit exceeded")
    return violations
```

Per-stop capacity/time-window feasibility never appears here — it can't be violated, by construction.

### Phase 3 — Improve routes
plain 2-opt only checks distance, but your problem has time windows. Reversing a segment can shorten total distance while pushing a later stop's arrival past its window — reordering changes arrival times, even though it doesn't change total load. So every candidate swap needs a feasibility re-check and not just a distance comparison. 

```py
function improve_route(route, distance_matrix):
    improved = true
    while improved:
        improved = false
        for i, j in segment_pairs(route.stops):
            candidate = reverse_segment(route.stops, i, j)
            if distance(candidate) < distance(route.stops)
               and time_windows_feasible(candidate, route.vehicle):
                route.stops = candidate
                improved = true
    return route
```

Capacity doesn't need re-checking here (reordering doesn't change total load as $\alpha + \beta = \beta + \alpha $), but time windows do. 

---
## CVRPTW System — Function IPO Diagrams (D2)

One diagram per process from the system DFD. Each is a self-contained
D2 file — inputs enter the highlighted box from the left, outputs leave
from the right (`direction: right` drives this layout). Plain-text nodes
(no border) represent the external entity, process, or data store on the
other end of each flow — they exist to label *where data comes from /
goes to*, not as part of the function itself.

**To render:** paste any block into https://play.d2lang.com, or run
`d2 diagram.d2 diagram.svg` locally, then `\includegraphics` the SVG
into your LaTeX report.

Dashed edges (`style.stroke-dash`) mark feedback/exception flows.

---

## 1. Validate orders and vehicles

```d2
direction: right

Delivery_coordinator: "Delivery\ncoordinator" { shape: text }

fn: "1. Validate orders\nand vehicles" {
  shape: rectangle
  style.fill: "#4C8BF5"
  style.font-color: white
}

Geocode: "Geocode and\nconfirm address" { shape: text }
Vehicle_store: "Driver and\nvehicle records" { shape: text }

Delivery_coordinator -> fn: "Orders, vehicles\nand depot"
fn -> Geocode: "Validated orders &\nvehicle records"
fn -> Vehicle_store: "Vehicle records"
```
![validate](../Images/D2/validate%20orders.svg)

## 2. Geocode and confirm address

```d2
direction: right

Validate: "Validate orders\nand vehicles" { shape: text }
Google_Maps: "Google Maps API" { shape: text }

fn: "2. Geocode and\nconfirm address" {
  shape: rectangle
  style.fill: "#4C8BF5"
  style.font-color: white
}

Delivery_coordinator: "Delivery\ncoordinator" { shape: text }
Order_store: "Order records" { shape: text }

Validate -> fn: "Validated orders &\nvehicle records"
Google_Maps -> fn: "Candidates"

fn -> Google_Maps: "Geocode request"
fn -> Delivery_coordinator: "Confirm address" {
  style.stroke-dash: 3
}
fn -> Order_store: "Confirmed coordinates"
```
![validate](../Images/D2/Geocode%20confirm.svg)

## 3. Build distance-time matrix

```d2
direction: right

Order_store: "Order records" { shape: text }

fn: "3. Build distance-\ntime matrix" {
  shape: rectangle
  style.fill: "#4C8BF5"
  style.font-color: white
}

Construct: "Construct routes" { shape: text }
Cache: "Cache" { shape: text }

Order_store -> fn: "Geocoded stops"

fn -> Construct: "Distance-time matrix"
# best-effort reconstruction — verify against your diagram
fn -> Cache: "Cached matrix"
```
![builddistance](../Images/D2/Build%20distance.svg)
## 4. Construct routes

```d2
direction: right

Build_matrix: "Build distance-\ntime matrix" { shape: text }
Vehicle_store: "Driver and\nvehicle records" { shape: text }
Check: "Check constraints" { shape: text }

fn: "4. Construct routes" {
  shape: rectangle
  style.fill: "#4C8BF5"
  style.font-color: white
}

Build_matrix -> fn: "Distance-time matrix"
Vehicle_store -> fn: "Vehicle records\n(capacity, depot, shift)"
Check -> fn: "Infeasible — rebuild" {
  style.stroke-dash: 3
}

fn -> Check: "Initial routes (NN)"
```

## 5. Check constraints

```d2
direction: right

Construct: "Construct routes" { shape: text }

fn: "5. Check constraints" {
  shape: rectangle
  style.fill: "#4C8BF5"
  style.font-color: white
}

Improve: "Improve routes" { shape: text }
Display: "Display and export" { shape: text }

Construct -> fn: "Initial routes (NN)"

fn -> Construct: "Infeasible — rebuild" {
  style.stroke-dash: 3
}
fn -> Improve: "Feasible routes"
fn -> Display: "Violations or\nunallocated"
```

## 6. Improve routes

```d2
direction: right

Check: "Check constraints" { shape: text }

fn: "6. Improve routes" {
  shape: rectangle
  style.fill: "#4C8BF5"
  style.font-color: white
}

Calculate: "Calculate metric" { shape: text }

Check -> fn: "Feasible routes"

fn -> Calculate: "Improved routes (2-opt)"
```

## 7. Calculate metric

```d2
direction: right

Improve: "Improve routes" { shape: text }

fn: "7. Calculate metric" {
  shape: rectangle
  style.fill: "#4C8BF5"
  style.font-color: white
}

Display: "Display and export" { shape: text }

Improve -> fn: "Improved routes (2-opt)"

fn -> Display: "Distance, time\nand load"
```

## 8. Display and export

```d2
direction: right

Calculate: "Calculate metric" { shape: text }
Check: "Check constraints" { shape: text }
Manual: "Manual Adjustments" { shape: text }

fn: "8. Display and export" {
  shape: rectangle
  style.fill: "#4C8BF5"
  style.font-color: white
}

Audit_log: "Route results and\naudit log" { shape: text }
Delivery_coordinator: "Delivery\ncoordinator" { shape: text }
Drivers_feed: "Drivers feed" { shape: text }

Calculate -> fn: "Distance, time\nand load"
Check -> fn: "Violations or\nunallocated"
Manual -> fn: "Manual edits\nand overrides"

fn -> Audit_log: "Results and\naudit log"
fn -> Delivery_coordinator: "Route plans, warnings\nand map links"
fn -> Drivers_feed: "Google Maps\nnavigation links"
```

## 9. Manual Adjustments

```d2
direction: right

# best-effort reconstruction — this box's exact wiring (particularly
# the link back into Construct routes / the vehicle store) was the
# least legible part of the flattened diagram; verify against your source

Display: "Display and export" { shape: text }

fn: "9. Manual\nAdjustments" {
  shape: rectangle
  style.fill: "#4C8BF5"
  style.font-color: white
}

Vehicle_store: "Driver and\nvehicle records" { shape: text }

Display -> fn: "Route plan for review"

fn -> Display: "Manual edits\nand overrides"
fn -> Vehicle_store: "Updated driver/\nvehicle availability"
```