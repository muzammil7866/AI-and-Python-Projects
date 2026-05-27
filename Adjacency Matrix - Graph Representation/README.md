# Adjacency Matrix — Graph Representation

## Overview

Implements a graph data structure represented as an **adjacency matrix**. The program allows interactively building a weighted, undirected graph by adding vertices and edges, then displays the resulting matrix.

## Concepts Covered

- Graph theory fundamentals (vertices, edges, weights)
- Adjacency matrix representation
- Dynamic matrix resizing when new vertices are added
- Interactive CLI-driven graph construction

## Files

| File | Description |
|------|-------------|
| `Adjacency Matrix Graph Representation.ipynb` | Jupyter notebook with full implementation and output |
| `Report.docx` | Problem statement and report |

## How to Run

```bash
jupyter notebook "Adjacency Matrix Graph Representation.ipynb"
```

## Key Functions

| Function | Purpose |
|----------|---------|
| `addVertex(v)` | Adds a new vertex and resizes the adjacency matrix |
| `addEdge(s, d, c)` | Adds an undirected edge with cost `c` between vertices `s` and `d` |
| `display(graph)` | Prints the adjacency matrix |

## Sample Interaction

```
ENTER 1 TO ADD VERTEX, ENTER 2 TO ADD EDGE, ENTER 3 TO DISPLAY GRAPH
> 1  →  ENTER VERTEX LABEL: A
> 1  →  ENTER VERTEX LABEL: B
> 2  →  SOURCE: A  DESTINATION: B  COST: 5
> 3  →  [[0, 5], [5, 0]]
```