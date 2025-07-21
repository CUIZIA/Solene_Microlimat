# Results Visualization with PyVista

To facilitate the inspection and 3D visualization of simulation outputs from **Solene-Microclimat**, we recommend using [`pyvista`](https://docs.pyvista.org/). It provides a simple interface to read and render VTK-compatible files.

&nbsp;

## Simulation Output Files

The simulation generates two types of files:

1. **`resu_simu_face.vtu`**

   * Contains face-level data.
   * Includes node `coordinates`, `connectivity`, `offsets`, and `types`.
   * Used to define the unstructured mesh surface.

2. **`resu_simu0.vtu`, `resu_simu1.vtu`, ...**

   * Contains triangular mesh data split from the face file.
   * The number at the end indicates the time step (starting from 0).
   * Each file includes simulation results such as `radiation fluxes`, `surface temperature`, `relative humidity`, etc.

> What is `.vtu`?
>
>  `.vtu` stands for **VTK Unstructured Grid File** — a format used to describe unstructured grid datasets that can consist of arbitrary combinations of cells (e.g., triangles, tetrahedra, etc.). These files can be directly read and visualized using PyVista.

&nbsp;
## Load and Display the Face Mesh

You can use the following code to load and visualize `resu_simu_face.vtu`. Face indices will be shown for easy inspection.

```python
import pyvista as pv

mesh = pv.read('./post/resu_simu_face.vtu')
centers = mesh.cell_centers().points
labels = [str(i) for i in range(mesh.n_cells)]

plotter = pv.Plotter()
plotter.add_mesh(mesh, show_edges=True, line_width=3)
plotter.add_point_labels(centers, labels, font_size=10, point_size=5)
plotter.show()
```

### Result:

<p align="center">
  <img src="/fig/result visualization 01.png" alt="Code Flowchart of SOLENE" width="50%">
</p>

<p align="center"><b>Figure 1: 3D Face Mesh with Indexed Labels.</b></p>
&nbsp;

## Time-Series 3D Visualization

You can also create a dynamic 3D plot showing how a particular variable evolves over time by looping through the time-indexed `.vtu` files.

```python
import pyvista as pv

mesh = pv.read('./post/resu_simu12.vtu')
plotter = pv.Plotter()
plotter.add_mesh(mesh, scalars="Tse", cmap="viridis", show_edges=False, scalar_bar_args=scalar_bar_args)
plotter.show()
```

### Result:

<p align="center">
  <img src="/fig/result visualization 02.png" alt="Code Flowchart of SOLENE" width="50%">
</p>

<p align="center"><b>Figure 2: Surface Temperature Distribution `Tse`.</b></p>
&nbsp;

> If you're unsure which scalar fields (i.e. features or variables) are available in the `.vtu` file for plotting, you can simply print them out with:
> ```python
> mesh = pv.read('./post/resu_simu12.vtu')
> print(mesh.cell_data.keys())
> ```
> This will return a list of all scalar field names contained in the mesh — such as `Tse` (surface temperature), `flux_sol_direct`
> radiation values, or `humidite_relative` humidity — which can then be passed to `add_mesh(..., scalars="FIELD_NAME")` for visualization.

&nbsp;

## Identify Triangles in a Face and Compute Mean Values

After identifying an interesting face, you can locate its corresponding triangular mesh cells in the time-step `.vtu` files, extract data, and compute temporal features such as mean surface temperature or radiation.

> While `pyvista`’s `find_containing_cell()` is one of the **fastest** ways to locate which face (cell) contains a given point, it is not always the **most reliable**.

In practice, you should take **special care when constructing or visualizing the face mesh**, especially to ensure that:

* Faces are correctly grouped by region
* There are no overlapping or duplicated faces

This method internally uses VTK's optimized spatial locator and can **quickly find the index of a cell that contains a given point** (typically the centroid of a triangle). Once identified, these indices can be used to:

* **Group triangles** under their parent faces
* **Extract relevant scalar values** (e.g., `Tse`)
* **Compute face-level statistics**, such as area-weighted or mean values
  
```python
import pyvista as pv
import numpy as np

face_mesh = pv.read('./post/resu_simu_face.vtu')
tri_mesh = pv.read('./post/resu_simu24.vtu')

face_locator = face_mesh.find_containing_cell

tse_values = tri_mesh['Tse']
tri_centers = tri_mesh.cell_centers().points
triangle_to_face = [face_locator(center) for center in tri_centers]

from collections import defaultdict
face_to_triangles = defaultdict(list)

for tri_id, face_id in enumerate(triangle_to_face):
    if face_id >= 0:
        face_to_triangles[face_id].append(tri_id)
face_mean_tse = {}
for face_id, tri_ids in face_to_triangles.items():
    values = tse_values[tri_ids]
    mean_val = np.mean(values)
    face_mean_tse[face_id] = mean_val

for fid, val in face_mean_tse.items():
    print(f"Face {fid} mean Tse = {val:.2f}")
```

This will print all mean value of the `Tse` on this surface.

