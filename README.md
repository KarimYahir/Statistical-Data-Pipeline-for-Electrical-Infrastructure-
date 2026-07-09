# Statistical Data Pipeline for Electrical Infrastructure

> An end-to-end statistical pipeline for analyzing real electrical measurements using SQL, Python and robust statistical techniques to support energy-efficiency decision making.

## Workflow

<p align="center">
<img src="figures/workflow.png" width="900">
</p>

---

## Overview

Modern cities rely on complex electrical infrastructures to sustain daily activities. Universities are no exception. Academic buildings, laboratories, libraries and administrative facilities consume large amounts of electrical energy every day, making continuous monitoring essential for improving operational efficiency and supporting sustainability initiatives.

This project documents the statistical methodology developed during my Social Service at the **Instituto de Ingeniería, Universidad Nacional Autónoma de México (UNAM)**. The objective was to analyze real electrical measurements collected from multiple facilities across Ciudad Universitaria in order to identify consumption patterns, detect anomalous behavior and provide quantitative information for energy-management decisions.

The project combines **SQL database management**, **Python-based data analysis**, **exploratory statistics**, **probability distribution analysis**, **robust outlier detection** and **data visualization** into a single analytical workflow.

Because the original measurements belong to an institutional monitoring system, this repository focuses on documenting the complete methodology rather than distributing confidential datasets.

---

## Motivation

Electrical monitoring systems generate thousands of measurements every day. Although this information contains valuable insights about the operation of electrical infrastructure, manually inspecting such large volumes of data quickly becomes impractical.

The motivation behind this project was to develop a methodology capable of transforming raw electrical measurements into structured statistical information that could support institutional decision-making.

Rather than treating the datasets as isolated CSV files, the project integrates remote data acquisition, database organization, statistical analysis and visualization into a single analytical pipeline.

Beyond describing electrical consumption, the methodology seeks to answer practical engineering questions such as:

- When does electricity consumption increase during the day?
- Are there recurring consumption patterns?
- Which measurements represent abnormal behavior?
- Are these anomalies statistical artifacts or physically meaningful events?
- Which statistical model best represents the observed data?
- How can these results support energy-efficiency strategies?

The long-term motivation was to provide a reproducible analytical framework that could later be extended toward automated monitoring systems, anomaly detection and sustainability indicators such as carbon footprint estimation.

---

## Problem Statement

The Coordinación Universitaria para la Sustentabilidad (COUS-UNAM) required a methodology capable of analyzing electrical measurements collected from different facilities across Ciudad Universitaria.

These measurements were generated continuously by the institutional monitoring system and stored within a NAS infrastructure managed by the Instituto de Ingeniería, UNAM. Each dataset contained electrical variables including phase currents (`Ia`, `Ib`, `Ic`), neutral current (`In`), phase voltages (`Va`, `Vb`, `Vc`, `Vn`), frequency and power-related quantities.

The main challenge was not acquiring the data but processing it efficiently. The monitoring system generated thousands of measurements each day, making manual inspection impossible.

For the case study analyzed in this project, one day of monitoring consisted of:

- **24 hours** of continuous measurements.
- **720 samples per hour.**
- **17,280 observations per day.**

Analyzing this volume of information required an automated workflow capable of organizing, processing and statistically characterizing the measurements.

The project addressed this challenge by combining SQL database management with Python-based statistical analysis.

From an engineering perspective, the primary objective was to understand how electricity consumption changed throughout the day and identify abnormal operating conditions.

This information can be used to:

- Detect unnecessary electricity consumption.
- Compare operational and vacation periods.
- Identify abnormal demand peaks.
- Support energy-efficiency strategies.
- Reduce operational costs.
- Provide evidence for future sustainability studies.

A second challenge involved distinguishing between normal electrical behavior and anomalous observations.

Real electrical measurements are influenced by many physical phenomena, including:

- Demand fluctuations.
- Automatic equipment activation.
- Electrical transients.
- Measurement noise.
- Communication failures.
- Short circuits.
- Power outages.

Some extreme values correspond to genuine electrical events rather than measurement errors. Consequently, the statistical methodology needed to identify anomalous observations without removing information that could be physically meaningful.

Instead of assuming that the measurements followed a predefined statistical model, the workflow first analyzed the empirical distribution of the data. Histogram-based exploration allowed the current measurements to be classified according to their statistical behavior before selecting an appropriate anomaly detection strategy.

This data-driven approach led to the comparison of several robust outlier detection methods, including the Interquartile Range (IQR), the Median Absolute Deviation (MAD) and percentile-based thresholds. The final methodology selected the percentile approach because it adapted better to the positively skewed distributions observed in the current measurements.

The result is a complete statistical pipeline capable of transforming large volumes of raw electrical measurements into structured information suitable for engineering analysis, energy-efficiency assessment and future sustainability applications.

---

## Methodology

The project was designed as an end-to-end statistical pipeline that transforms raw electrical measurements into organized, interpretable and statistically meaningful information.

The workflow combines:

- Remote data acquisition
- SQL database organization
- Python preprocessing
- Exploratory Data Analysis (EDA)
- Probability distribution characterization
- Robust outlier detection
- Signal reconstruction
- Visualization and reporting

Although the original datasets and institutional infrastructure cannot be distributed publicly, the complete analytical methodology is documented in this repository.

### 1. Data Acquisition

Electrical measurements were retrieved from an institutional monitoring infrastructure where CSV files were stored remotely.

Each file contained time-dependent electrical variables, including phase currents, neutral current, voltages, frequency and power-related quantities.

These datasets were generated by monitoring equipment installed in different electrical substations throughout Ciudad Universitaria.

### 2. Metadata Organization

A metadata catalog associated every measured point with its corresponding physical infrastructure.

Each monitored location included information such as:

- Database identifier
- Substation
- Transformer
- Nominal voltage
- Transformer capacity
- SCADA identifier
- Campus facility

This metadata provided the physical context necessary to interpret each dataset correctly.

### 3. SQL Database Organization

After acquisition, the processed information was organized within a relational SQL database.

Instead of treating each CSV file independently, the workflow stored hourly electrical measurements inside structured tables, allowing the information to be queried efficiently according to facility and date range.

The SQL layer supported:

- Automated table creation.
- Hourly energy storage.
- Date-range filtering.
- Aggregation queries.
- Integration with Python.

This organization significantly improved scalability and simplified the analysis of multiple facilities.

### 4. Python Preprocessing

The retrieved measurements were loaded into Python using Pandas.

The preprocessing stage included:

- Timestamp parsing.
- Chronological ordering.
- Missing value identification.
- Variable selection.
- Hourly segmentation.

The resulting DataFrames served as the foundation for the statistical analysis.

### 5. Hourly Statistical Processing

Since electrical behavior changes throughout the day, the complete time series was divided into hourly blocks.

For each hour and each current variable, descriptive statistics were computed, including:

- Mean
- Median
- Variance
- Standard deviation
- Percentiles

Analyzing each hour independently allowed the methodology to capture local variations that would otherwise be hidden by daily averages.

### 6. Exploratory Data Analysis

Before applying any anomaly detection method, the empirical behavior of the measurements was explored through descriptive statistics and frequency histograms.

This stage allowed the distributions to be classified according to characteristics such as:

- Symmetry
- Skewness
- Unimodality
- Multimodality
- Heavy tails

Understanding the shape of the distributions was essential because the choice of an outlier detection method depends on the statistical behavior of the data.

### 7. Probability Distribution Characterization

Rather than assuming that all electrical variables followed the same statistical model, the workflow first analyzed the empirical distribution of the data.

Histograms were constructed for each electrical variable to identify whether the observations exhibited:

- Symmetric distributions
- Right-skewed distributions
- Left-skewed distributions
- Unimodal behavior
- Multimodal behavior
- Heavy-tailed behavior

The current measurements analyzed in this project consistently exhibited positive skewness. Most observations were concentrated around normal operating conditions, while relatively few measurements formed a long right tail corresponding to high current values.

This observation was fundamental because it demonstrated that traditional Gaussian assumptions were not appropriate for the analyzed data.

Instead of selecting an anomaly detection technique beforehand, the statistical model was chosen according to the observed behavior of the measurements.

### 8. Outlier Detection

A major objective of the project was identifying anomalous electrical measurements without eliminating physically meaningful events.

Three robust statistical approaches were evaluated:

- Interquartile Range (IQR)
- Median Absolute Deviation (MAD)
- Percentile-based thresholds

Each method was assessed according to its ability to represent the empirical distribution of the current measurements.

Because the distributions exhibited positive skewness, percentile-based thresholds produced the most consistent results.

Unlike Gaussian-based methods, percentile thresholds adapt naturally to asymmetric distributions and therefore reduce the influence of extreme values without assuming statistical normality.

The final methodology computed lower and upper percentile limits independently for each hourly block and each current variable.

Measurements outside these limits were classified as potential anomalies.

### 9. Outlier Registration

Detected outliers were not permanently removed from the dataset.

Instead, every anomalous observation was stored in a structured report containing information such as:

- Timestamp
- Electrical variable
- Measured value
- Statistical threshold

Maintaining this separate registry was an important design decision.

From an engineering perspective, an extreme observation may correspond to:

- Electrical transients
- Demand peaks
- Equipment startup
- Communication failures
- Sensor errors
- Short circuits
- Power outages

Consequently, outliers were considered events requiring interpretation rather than simple statistical errors.

### 10. Signal Reconstruction

After registering the detected outliers, anomalous observations were replaced with missing values (`NaN`).

The resulting gaps were reconstructed through linear interpolation.

This approach produced a cleaned version of the signal while preserving its temporal continuity.

The reconstruction process was not intended to erase anomalous events.

Instead, the workflow generated two complementary products:

- A cleaned dataset for statistical analysis.
- A complete anomaly report for engineering interpretation.

### 11. Visualization and Reporting

The processed measurements were finally visualized using Python.

The generated figures included:

- Electrical current profiles.
- Frequency histograms.
- Statistical summaries.
- Outlier visualization.
- Cleaned signal reconstruction.
- Hourly energy behavior.

These visualizations transformed numerical results into interpretable information suitable for technical reports and engineering decision-making.

---

# Data Engineering and SQL Architecture

The project integrates statistical analysis with a structured data engineering workflow.

Instead of analyzing isolated CSV files, the methodology organizes electrical measurements inside a relational SQL database, allowing information to be stored, queried and analyzed systematically.

This architecture makes the workflow scalable and suitable for long-term monitoring applications.

### 1. Remote Data Acquisition

The original measurements were stored within an institutional monitoring infrastructure.

CSV files were retrieved remotely according to:

- Substation
- Transformer
- Date
- Monitoring point

Because these files belong to an institutional monitoring system, neither the original datasets nor the connection credentials are included in this repository.

Only the analytical methodology is documented.

### 2. Metadata Catalog

Each monitored point was associated with a metadata catalog describing its physical characteristics.

The catalog included information such as:

- Database identifier
- Substation
- Transformer
- Transformer capacity
- Nominal voltage
- SCADA identifier
- Campus building

This metadata allowed every measurement to be associated with its corresponding electrical infrastructure.

### 3. SQL Database Design

Once retrieved, the measurements were organized inside a relational SQL database.

Instead of manually processing individual CSV files, the project stored energy measurements inside structured hourly tables.

Each table contained variables such as:

- Timestamp (`dh`)
- Active energy (`kWh`)
- Reactive energy (`kvarh`)
- Apparent energy (`kVAh`)

The SQL layer provided:

- Structured storage
- Data consistency
- Fast querying
- Date filtering
- Aggregation
- Integration with Python

### 4. Automated Database Generation

The SQL tables were created automatically from the metadata catalog.

Rather than manually generating dozens of database tables, Python scripts produced the corresponding SQL statements for every valid monitoring point.

This automation simplified database management and reduced the probability of human error.

### 5. SQL Queries

After organizing the data, SQL queries were used to retrieve information over arbitrary time intervals.

Typical operations included:

- Date-range filtering.
- Hourly retrieval.
- Energy aggregation.
- Time ordering.
- Consumption summaries.

These queries allowed the project to compute accumulated energy consumption while preserving the temporal structure required for statistical analysis.

### 6. Python Integration

Python acted as the analytical layer connected to the SQL database.

After executing SQL queries, the retrieved records were converted into Pandas DataFrames.

These DataFrames were subsequently used for:

- Statistical analysis.
- Exploratory visualization.
- Outlier detection.
- Signal reconstruction.
- Report generation.

The combination of SQL and Python created a complete analytical pipeline in which database management and statistical analysis operated as complementary stages.

### 7. Missing Data Handling

Monitoring systems occasionally contain incomplete measurements due to communication failures or unavailable records.

To preserve the integrity of the time series, the workflow generated a complete expected sequence of timestamps.

Whenever a measurement was missing, the corresponding position was filled with `NaN`.

This strategy preserved chronological consistency and prevented missing observations from shifting the remaining measurements.

### 8. Engineering Contribution

The data engineering component transformed the project from a collection of independent scripts into a structured analytical system.

The SQL layer enabled:

- Efficient storage.
- Automated querying.
- Time-based aggregation.
- Facility comparison.
- Scalable analysis.
- Direct integration with Python.

As a result, the workflow became suitable not only for the statistical analysis presented in this repository but also for future monitoring platforms, dashboards and automated reporting systems.

---

# Statistical Analysis

The statistical component represents the core of this project.

Rather than applying predefined statistical assumptions, the methodology first characterized the empirical behavior of the electrical measurements before selecting the most appropriate analytical strategy.

This philosophy guided every stage of the statistical workflow.

### 1. Statistical Nature of the Variables

The primary variables analyzed were the electrical currents:

- `Ia`
- `Ib`
- `Ic`
- `In`

From a statistical perspective, these variables were classified as quantitative continuous variables.

This classification justified the use of descriptive statistics, probability distributions and robust outlier detection techniques.

### 2. Descriptive Statistics

For every hourly segment and every current variable, the workflow computed:

- Mean
- Median
- Variance
- Standard deviation
- Percentiles

These quantities summarized the behavior of the measurements while providing the numerical basis for later statistical analysis.

Because real electrical data frequently contain extreme observations, classical statistics were interpreted together with robust statistical measures rather than independently.

### 3. Histogram-Based Exploration

Histograms served as the primary exploratory tool throughout the project.

Instead of assuming a distribution, the empirical data determined the statistical interpretation.

The histogram analysis evaluated:

- Symmetry
- Skewness
- Modality
- Tail behavior

This stage provided the statistical evidence required to justify the selection of the final anomaly detection strategy.

### 4. Selection of the Statistical Model

The histogram analysis demonstrated that the current measurements exhibited positive skewness.

Consequently, methods based exclusively on Gaussian assumptions were not appropriate.

Rather than forcing the data to follow a normal distribution, the workflow adopted robust techniques capable of adapting to asymmetric empirical distributions.

This decision became the foundation of the anomaly detection methodology.

### 5. Comparison of Outlier Detection Methods

One of the principal objectives of this project was to identify a statistical method capable of detecting anomalous electrical measurements while preserving physically meaningful events.

Three robust outlier detection techniques were evaluated:

- **Interquartile Range (IQR)**
- **Median Absolute Deviation (MAD)**
- **Percentile-based thresholds**

Each method was analyzed according to the statistical characteristics observed in the electrical current distributions.

The comparison demonstrated that percentile-based thresholds produced the most reliable results for the analyzed datasets. Since the current measurements exhibited positive skewness, percentile limits adapted naturally to the empirical distribution without imposing Gaussian assumptions.

Instead of selecting an anomaly detection method arbitrarily, the statistical properties of the data determined the final methodology.

### 6. Detection and Interpretation of Outliers

The detected outliers were not treated simply as erroneous observations.

In electrical monitoring systems, extreme values may represent:

- Demand peaks.
- Equipment startup.
- Electrical transients.
- Short circuits.
- Power outages.
- Sensor failures.
- Communication interruptions.

For this reason, every detected anomaly was preserved inside an independent report instead of being permanently removed from the dataset.

This design allows future engineering analyses to distinguish between statistical anomalies and physically meaningful electrical events.

### 7. Signal Reconstruction

Once anomalous observations had been identified, they were temporarily replaced by missing values (`NaN`).

The resulting gaps were reconstructed using linear interpolation.

This procedure generated a cleaned version of the signal while preserving its chronological structure and reducing the influence of extreme observations on later statistical calculations.

Importantly, the interpolation process was applied only to the statistical version of the signal.

The original measurements and the complete outlier registry remained unchanged for engineering interpretation.

### 8. Statistical Contribution

The main statistical contribution of this project lies in demonstrating that anomaly detection should not rely on predefined assumptions regarding the distribution of the data.

Instead, the methodology follows the sequence:

1. Explore the empirical distribution.
2. Characterize the statistical behavior.
3. Compare robust detection methods.
4. Select the method most consistent with the observed data.
5. Detect anomalous observations.
6. Preserve engineering information.
7. Reconstruct the statistical signal.

This data-driven strategy provides a more reliable framework for analyzing real electrical measurements than applying a fixed statistical model to every dataset.

---

# Results and Insights

The proposed methodology successfully transformed large volumes of raw electrical measurements into statistically meaningful information.

Beyond generating descriptive statistics, the workflow revealed consumption patterns, identified anomalous events and provided quantitative evidence capable of supporting institutional energy-efficiency initiatives.

### 1. Electrical Current Distributions

Histogram analysis revealed that the current measurements (`Ia`, `Ib`, `Ic` and `In`) did not follow symmetric distributions.

Instead, the observations exhibited positive skewness, where most measurements remained concentrated around typical operating conditions while relatively few observations formed a long right-hand tail.

This result demonstrated that classical Gaussian assumptions were insufficient to describe the statistical behavior of the analyzed electrical signals.

Consequently, robust statistical methods became necessary.

### 2. Selection of the Outlier Detection Strategy

The comparison between IQR, MAD and percentile-based thresholds showed that percentile limits provided the best representation of the empirical distributions.

Because the analyzed signals were asymmetric, percentile thresholds adapted naturally to the observed behavior without requiring normally distributed data.

This represents one of the principal statistical conclusions of the project:

> The anomaly detection method should be selected according to the observed distribution of the measurements rather than assuming a predefined statistical model.

### 3. Identification of Anomalous Events

The proposed methodology successfully identified measurements exceeding the statistical thresholds defined for each hourly segment.

Rather than deleting these observations, every anomaly was stored independently for subsequent inspection.

These events may correspond to:

- Electrical demand peaks.
- Equipment activation.
- Electrical disturbances.
- Communication failures.
- Measurement errors.
- Operational anomalies.

Consequently, the methodology preserves engineering information while simultaneously generating a statistically cleaned dataset.

### 4. Daily Consumption Behavior

The analyzed measurements revealed a characteristic daily consumption pattern.

Current values remained relatively high during nighttime and early morning hours, decreased throughout normal daytime operation and increased again during the evening.

This behavior suggests that part of the electrical consumption originates from systems operating independently of regular academic activities, including automatic equipment and continuously operating electrical infrastructure.

These observations provide valuable information for future energy-efficiency studies.

### 5. Operational Interpretation

One particularly relevant observation involved periods of reduced academic activity.

Despite lower building occupancy during vacation periods or inactive academic schedules, certain facilities continued exhibiting significant electrical consumption.

This behavior may indicate opportunities for:

- Reviewing equipment schedules.
- Optimizing automatic systems.
- Reducing unnecessary electricity consumption.
- Lowering operational costs.
- Supporting sustainability initiatives.

The statistical methodology therefore provides quantitative evidence capable of supporting institutional decision-making.

### 6. Technical Contribution

From a technical perspective, the project integrates several disciplines into a single analytical framework.

The complete workflow combines:

- Remote data acquisition.
- Metadata organization.
- SQL database management.
- Python preprocessing.
- Exploratory Data Analysis.
- Probability distribution characterization.
- Robust outlier detection.
- Signal reconstruction.
- Statistical visualization.
- Engineering interpretation.

Rather than representing an isolated statistical exercise, the repository documents a complete analytical pipeline for processing real electrical measurements.

### 7. Main Findings

The principal findings of this project are summarized below:

- Real electrical measurements exhibit asymmetric statistical behavior.
- Current distributions are positively skewed.
- Classical Gaussian assumptions are insufficient for the analyzed datasets.
- Percentile-based thresholds outperform IQR and MAD for the analyzed case study.
- Outliers may represent meaningful engineering events rather than statistical errors.
- Separating anomaly detection from signal reconstruction preserves both statistical and physical information.
- SQL database organization significantly improves scalability and long-term analysis.
- The proposed workflow supports future applications in automated monitoring and sustainability analysis.

### 8. Final Remarks

The most significant contribution of this project is methodological.

Instead of imposing statistical assumptions on the data, the workflow allows the empirical distribution to determine the analytical strategy.

This philosophy results in a more robust, interpretable and transferable methodology for analyzing electrical monitoring systems based on real institutional measurements.

---

# Project Architecture

The project follows an end-to-end analytical architecture integrating remote data acquisition, database organization, statistical analysis and visualization.

```text
                    Institutional Monitoring System
                                   │
                                   ▼
                           Remote NAS Storage
                                   │
                                   ▼
                          Electrical CSV Files
                                   │
                                   ▼
                     Metadata & Substation Catalog
                                   │
                                   ▼
                    SQL Database Organization
                                   │
                                   ▼
                        Python Data Processing
                                   │
               ┌───────────────────┼───────────────────┐
               ▼                   ▼                   ▼
      Exploratory Data      Statistical Analysis   Visualization
           Analysis                                 & Reporting
               │
               ▼
    Probability Distribution Analysis
               │
               ▼
     Robust Outlier Detection
               │
               ▼
      Signal Reconstruction
               │
               ▼
      Energy-Efficiency Insights
```

The architecture integrates SQL, Python and statistical reasoning into a unified workflow capable of transforming raw electrical measurements into actionable engineering information.

---

# Technologies Used

| Category | Technologies |
|----------|--------------|
| Programming Language | Python |
| Database | SQL, MariaDB |
| Data Analysis | Pandas, NumPy |
| Statistical Analysis | SciPy |
| Visualization | Matplotlib |
| Data Storage | NAS |
| Remote Access | SFTP |
| Reporting | Excel |
| Version Control | Git, GitHub |

---

# Confidentiality Statement

This repository documents the methodology developed during an academic project based on real institutional electrical measurements collected at the Universidad Nacional Autónoma de México (UNAM).

Due to confidentiality agreements, the original datasets, SQL databases, server credentials, network infrastructure and institutional resources are **not included** in this repository.

Only the analytical methodology, software architecture and statistical workflow are presented. All examples have been anonymized while preserving the technical approach developed during the project.

---

# References

- Pandas Development Team. *Pandas Documentation*.
- NumPy Developers. *NumPy Documentation*.
- Matplotlib Development Team. *Matplotlib Documentation*.
- SciPy Development Team. *SciPy Documentation*.
- Montgomery, D. C., & Runger, G. C. *Applied Statistics and Probability for Engineers*.
- Tukey, J. W. *Exploratory Data Analysis*.
- NIST/SEMATECH e-Handbook of Statistical Methods.

---

# License

This repository is released under the MIT License.

See the `LICENSE` file for additional information.

