================================================================
  UNSUPERVISED LEARNING - E-COMMERCE CUSTOMER SEGMENTATION
  Assessment Submission
================================================================

AUTHOR: Student Submission
TOPIC: Customer Segmentation by Price Sensitivity
METHOD: K-Means + Hierarchical Clustering

----------------------------------------------------------------
FILES INCLUDED:
----------------------------------------------------------------

1. segmentation.py           --> Main Python script (all 10 tasks)
2. customers_segmented.csv   --> Final labelled dataset
3. fig1_eda.png              --> Task 2: EDA & Spending Patterns
4. fig2_elbow.png            --> Task 4: Elbow + Silhouette Method
5. fig3_hierarchical.png     --> Task 6: Hierarchical Clustering & Dendrogram
6. fig4_clusters_viz.png     --> Task 7: PCA + t-SNE Visualization
7. fig5_profiles.png         --> Task 8: Cluster Profiling
8. fig6_boxplots.png         --> Task 9: Cluster Comparison Boxplots
9. fig7_strategy.png         --> Task 10: Marketing Strategy Dashboard
10. README.txt               --> This file

----------------------------------------------------------------
TASK CHECKLIST:
----------------------------------------------------------------

[✓] Task 1  - Load & Clean Dataset (removed NAs & duplicates)
[✓] Task 2  - Visualize Spending Patterns & Demographics
[✓] Task 3  - Normalize Features using StandardScaler
[✓] Task 4  - Optimal Clusters via Elbow + Silhouette Method (k=4)
[✓] Task 5  - K-Means Clustering applied (k=4)
[✓] Task 6  - Hierarchical Clustering (Ward Linkage, ARI=0.948)
[✓] Task 7  - PCA + t-SNE Cluster Visualization
[✓] Task 8  - Cluster Profiling (Age, Income, Loyalty, Spend)
[✓] Task 9  - Original Dataset Labelled with Cluster IDs
[✓] Task 10 - Marketing Strategy per Cluster

----------------------------------------------------------------
CLUSTER RESULTS SUMMARY:
----------------------------------------------------------------

Cluster 0 - Budget Browsers       (30.1%) - Low income, low spend
Cluster 1 - Mid-Market Loyalists  (39.9%) - Medium income, steady buyers
Cluster 2 - Premium Shoppers      (14.1%) - High income, high spend
Cluster 3 - High-Value VIPs       (16.0%) - Top spenders, most loyal

----------------------------------------------------------------
LIBRARIES USED:
----------------------------------------------------------------
pandas, numpy, scikit-learn, matplotlib, seaborn, scipy

================================================================
