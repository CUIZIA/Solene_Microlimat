## Calculating Coefficients for the 3R2C Conduction Model

When using the **3R2C conduction model**, four key coefficients $m_1, m_2, o_2$ and $p_2$ are required to compute $\alpha_i$ and $\beta_i$. However, when considering a multi-layer wall structure (e.g., 5 layers, 10 layers, or even 100 layers), the calculation becomes increasingly complex. To address this, I identified patterns within the mathematical expressions for these coefficients and implemented them into the following C++ functions for efficient computation.

- **Input**:
  - `r[]`: List of thermal resistances of the layers.
  - `c[]`: List of thermal capacitances of the layers.
  - `n`: Number of layers.

### 1. Function to Calculate $m_1$

The $m_1$ coefficient is computed as:

```cpp
double calculate_m1(double r[], double c[], int n) 
{
  double sum_1 = 0;

  for (int i = 0; i < n; i++) {
      for (int j = 0; j <= i; j++) {
          if (i == j) {
              sum_1 += c[i] * r[j] / 2.0;
          } else {
              sum_1 += c[i] * r[j];
          }
      }
  }
  return sum_1;
}
```

### 2. Function to Calculate $m_2$

The $m_2$ coefficient includes multiple summations and interactions between layers:

```cpp
double calculate_m2(double r[], double c[], int n) 
{
  double sum_1 = 0, sum_2 = 0;

  for (int i = 0; i < n; i++) {
      for (int j = i; j < n; j++) {
          if (i == j) {
              sum_1 += pow(r[i], 2) * c[i] * c[j] / 24.0;
          } else {
              sum_1 += pow(r[i], 2) * c[i] * c[j] / 6.0;
          }
      }
  }

  for (int i = 0; i < n - 1; i++) {
      for (int j = i + 1; j < n; j++) {
          double rr = r[i] * r[j];
          double part_1 = c[i] * c[j] / 4.0 + pow(c[j], 2) / 6.0;

          double part_2 = 0;
          for (int x = j + 1; x < n; x++) {
              part_2 += c[i] * c[x] / 2.0 + c[j] * c[x] / 2.0;
          }

          double part_3 = 0, part_4 = 0;
          for (int y = i + 1; y < j; y++) {
              part_3 += c[y] * c[j] / 2.0;
              for (int z = j + 1; z < n; z++) {
                  part_4 += c[y] * c[z];
              }
          }

          sum_2 += rr * (part_1 + part_2 + part_3 + part_4);
      }
  }
  return sum_1 + sum_2;
}
```

### 3. Function to Calculate $o_2$

The $o_2$ coefficient involves resistances and squared capacitances:

```cpp
double calculate_o2(double r[], double c[], int n) 
{
  double sum_1 = 0;

  for (int i = 0; i < n; i++) {
      sum_1 += r[i] * pow(c[i], 2) / 6.0;
  }

  for (int i = 0; i < n - 1; i++) {
      for (int j = i + 1; j < n; j++) {
          double cc = c[i] * c[j];

          for (int x = i; x <= j; x++) {
              if (x == i || x == j) {
                  sum_1 += r[x] * cc / 2.0;
              } else {
                  sum_1 += r[x] * cc;
              }
          }
      }
  }
  return sum_1;
}
```

### 4. Function to Calculate $p_2$

The $p_2$ coefficient involves resistances and squared capacitances:

```cpp
double calculate_p2(double r[], double c[], int n) 
{
  double sum_1 = 0, sum_2 = 0;

  for (int i = 0; i < n; i++) {
      for (int j = i; j < n; j++) {
          if (i == j) {
              sum_1 += pow(c[i], 2) * r[i] * r[j] / 24.0;
          } else {
              sum_1 += pow(c[i], 2) * r[i] * r[j] / 6.0;
          }
      }
  }

  for (int i = 0; i < n - 1; i++) {
      for (int j = i + 1; j < n; j++) {
          double cc = c[i] * c[j];
          double part_1 = r[i] * r[j] / 4.0 + pow(r[j], 2) / 6.0;

          double part_2 = 0;
          for (int x = j + 1; x < n; x++) {
              part_2 += r[i] * r[x] / 2.0 + r[j] * r[x] / 2.0;
          }

          double part_3 = 0, part_4 = 0;
          for (int y = i + 1; y < j; y++) {
              part_3 += r[y] * r[j] / 2.0;
              for (int z = j + 1; z < n; z++) {
                  part_4 += r[y] * r[z];
              }
          }

          sum_2 += cc * (part_1 + part_2 + part_3 + part_4);
      }
  }
  return sum_1 + sum_2;
}
```
