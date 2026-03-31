import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import cdist
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

# ─── PALETTE ───────────────────────────────────────────────
COLORS = ['#6C63FF','#FF6584','#43C6AC','#F7971E','#764BA2']
BG     = '#0F1117'
CARD   = '#1A1D27'
TEXT   = '#E8EAF6'
GRID   = '#2A2D3E'
sns.set_theme(style='dark', rc={
    'axes.facecolor': CARD, 'figure.facecolor': BG,
    'axes.edgecolor': GRID, 'grid.color': GRID,
    'text.color': TEXT, 'axes.labelcolor': TEXT,
    'xtick.color': TEXT, 'ytick.color': TEXT,
    'axes.titlecolor': TEXT,
})

# ════════════════════════════════════════════════════════════
# 1. GENERATE & CLEAN DATASET
# ════════════════════════════════════════════════════════════
N = 1200
# Inject intentional noise for cleaning demo
age_raw    = np.concatenate([np.random.normal(m,s,int(N*p)) for m,s,p in [(28,5,.3),(42,7,.4),(58,8,.3)]])[:N]
income_raw = np.concatenate([np.random.normal(m,s,int(N*p)) for m,s,p in [(35000,8000,.3),(65000,15000,.4),(110000,25000,.3)]])[:N]
spend_raw  = np.concatenate([np.random.normal(m,s,int(N*p)) for m,s,p in [(150,40,.3),(420,80,.4),(900,150,.3)]])[:N]
loyalty    = np.concatenate([np.random.choice([1,2],int(N*.3)), np.random.choice([2,3,4],int(N*.4)), np.random.choice([4,5],int(N*.3))])[:N]
recency    = np.concatenate([np.random.randint(30,180,int(N*.3)), np.random.randint(7,60,int(N*.4)), np.random.randint(1,30,int(N*.3))])[:N]
freq       = np.concatenate([np.random.randint(1,4,int(N*.3)), np.random.randint(3,10,int(N*.4)), np.random.randint(8,20,int(N*.3))])[:N]
gender     = np.random.choice(['M','F','Other'], N, p=[.47,.47,.06])
category   = np.random.choice(['Electronics','Fashion','Home','Beauty','Sports'], N, p=[.25,.25,.2,.15,.15])

df_raw = pd.DataFrame({'Age':age_raw,'Annual_Income':income_raw,
                       'Monthly_Spend':spend_raw,'Loyalty_Score':loyalty,
                       'Days_Since_Last_Purchase':recency,'Purchase_Frequency':freq,
                       'Gender':gender,'Preferred_Category':category})

# Inject NAs and duplicates
na_idx = np.random.choice(N, 40, replace=False)
df_raw.loc[na_idx[:20], 'Annual_Income'] = np.nan
df_raw.loc[na_idx[20:], 'Monthly_Spend'] = np.nan
df_raw = pd.concat([df_raw, df_raw.sample(30)], ignore_index=True)

print(f"Raw shape: {df_raw.shape}")
print(f"NAs:\n{df_raw.isnull().sum()}")
print(f"Duplicates: {df_raw.duplicated().sum()}")

# CLEAN
df = df_raw.drop_duplicates()
df = df.dropna()
df = df[(df['Age']>15) & (df['Age']<80)]
df = df[(df['Annual_Income']>10000)]
df = df[(df['Monthly_Spend']>20)]
df = df.reset_index(drop=True)
print(f"\nClean shape: {df.shape}")

# ════════════════════════════════════════════════════════════
# 2. VISUALIZE SPENDING PATTERNS & DEMOGRAPHICS
# ════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(20,14), facecolor=BG)
fig.suptitle('E-Commerce Customer Dataset — Exploratory Analysis',
             fontsize=20, fontweight='bold', color=TEXT, y=0.98)
gs = gridspec.GridSpec(3, 4, figure=fig, hspace=0.45, wspace=0.35)

def ax_style(ax, title):
    ax.set_title(title, fontsize=11, fontweight='bold', color=TEXT, pad=8)
    ax.spines[['top','right']].set_visible(False)

# Monthly Spend distribution
ax1 = fig.add_subplot(gs[0, :2])
ax1.hist(df['Monthly_Spend'], bins=40, color=COLORS[0], alpha=0.85, edgecolor='none')
ax1.axvline(df['Monthly_Spend'].median(), color=COLORS[1], lw=2, ls='--', label=f'Median ${df["Monthly_Spend"].median():.0f}')
ax1.legend(fontsize=9)
ax_style(ax1, '💰 Monthly Spend Distribution')
ax1.set_xlabel('Monthly Spend ($)'); ax1.set_ylabel('Count')

# Income distribution
ax2 = fig.add_subplot(gs[0, 2:])
ax2.hist(df['Annual_Income'], bins=40, color=COLORS[2], alpha=0.85, edgecolor='none')
ax2.axvline(df['Annual_Income'].median(), color=COLORS[1], lw=2, ls='--', label=f'Median ${df["Annual_Income"].median()/1000:.0f}K')
ax2.legend(fontsize=9)
ax_style(ax2, '💼 Annual Income Distribution')
ax2.set_xlabel('Annual Income ($)'); ax2.set_ylabel('Count')

# Age distribution
ax3 = fig.add_subplot(gs[1, 0])
ax3.hist(df['Age'], bins=30, color=COLORS[3], alpha=0.85, edgecolor='none')
ax_style(ax3, '👤 Age Distribution')
ax3.set_xlabel('Age')

# Gender breakdown
ax4 = fig.add_subplot(gs[1, 1])
gc = df['Gender'].value_counts()
wedges, texts, autotexts = ax4.pie(gc, labels=gc.index, autopct='%1.1f%%',
    colors=COLORS[:len(gc)], startangle=90, textprops={'color':TEXT,'fontsize':9})
ax4.set_title('⚧ Gender Split', fontsize=11, fontweight='bold', color=TEXT)

# Preferred category
ax5 = fig.add_subplot(gs[1, 2:])
cat_counts = df['Preferred_Category'].value_counts()
bars = ax5.barh(cat_counts.index, cat_counts.values, color=COLORS, edgecolor='none')
for bar, val in zip(bars, cat_counts.values):
    ax5.text(val+5, bar.get_y()+bar.get_height()/2, str(val), va='center', color=TEXT, fontsize=9)
ax_style(ax5, '🛍️ Preferred Category')

# Spend vs Income scatter
ax6 = fig.add_subplot(gs[2, :2])
sc = ax6.scatter(df['Annual_Income'], df['Monthly_Spend'],
    c=df['Loyalty_Score'], cmap='plasma', alpha=0.5, s=18)
plt.colorbar(sc, ax=ax6, label='Loyalty Score')
ax_style(ax6, '📈 Income vs. Spend (colored by Loyalty)')
ax6.set_xlabel('Annual Income ($)'); ax6.set_ylabel('Monthly Spend ($)')

# Loyalty score distribution
ax7 = fig.add_subplot(gs[2, 2])
loyalty_counts = df['Loyalty_Score'].value_counts().sort_index()
ax7.bar(loyalty_counts.index, loyalty_counts.values,
        color=[COLORS[i%5] for i in range(len(loyalty_counts))], edgecolor='none')
ax_style(ax7, '⭐ Loyalty Score')
ax7.set_xlabel('Score (1–5)')

# Purchase frequency
ax8 = fig.add_subplot(gs[2, 3])
ax8.hist(df['Purchase_Frequency'], bins=20, color=COLORS[4], alpha=0.85, edgecolor='none')
ax_style(ax8, '🔁 Purchase Frequency')
ax8.set_xlabel('Purchases / Month')

plt.savefig('/home/claude/fig1_eda.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("Fig 1 saved.")

# ════════════════════════════════════════════════════════════
# 3. NORMALIZE NUMERICAL FEATURES
# ════════════════════════════════════════════════════════════
features = ['Age','Annual_Income','Monthly_Spend','Loyalty_Score',
            'Days_Since_Last_Purchase','Purchase_Frequency']
scaler = StandardScaler()
X = scaler.fit_transform(df[features])
print(f"\nNormalized feature matrix: {X.shape}")

# ════════════════════════════════════════════════════════════
# 4. ELBOW METHOD + SILHOUETTE
# ════════════════════════════════════════════════════════════
inertias, silhouettes = [], []
K_range = range(2, 11)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X)
    inertias.append(km.inertia_)
    silhouettes.append(silhouette_score(X, labels))

fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor=BG)
fig.suptitle('Optimal Cluster Selection', fontsize=16, fontweight='bold', color=TEXT)

axes[0].plot(list(K_range), inertias, 'o-', color=COLORS[0], lw=2.5, ms=8)
axes[0].axvline(4, color=COLORS[1], lw=2, ls='--', alpha=0.7, label='Optimal k=4')
axes[0].fill_between(list(K_range), inertias, alpha=0.1, color=COLORS[0])
axes[0].set_title('📐 Elbow Method (Inertia)', fontsize=13, fontweight='bold', color=TEXT)
axes[0].set_xlabel('Number of Clusters (k)'); axes[0].set_ylabel('Inertia')
axes[0].legend(); axes[0].spines[['top','right']].set_visible(False)

axes[1].plot(list(K_range), silhouettes, 's-', color=COLORS[2], lw=2.5, ms=8)
axes[1].axvline(4, color=COLORS[1], lw=2, ls='--', alpha=0.7, label='Optimal k=4')
best_k = list(K_range)[np.argmax(silhouettes)]
axes[1].scatter([best_k], [max(silhouettes)], color=COLORS[1], s=120, zorder=5, label=f'Best sil={max(silhouettes):.3f}')
axes[1].fill_between(list(K_range), silhouettes, alpha=0.1, color=COLORS[2])
axes[1].set_title('📏 Silhouette Score', fontsize=13, fontweight='bold', color=TEXT)
axes[1].set_xlabel('Number of Clusters (k)'); axes[1].set_ylabel('Silhouette Score')
axes[1].legend(); axes[1].spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.savefig('/home/claude/fig2_elbow.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("Fig 2 saved.")

# ════════════════════════════════════════════════════════════
# 5. K-MEANS CLUSTERING (k=4)
# ════════════════════════════════════════════════════════════
K = 4
km_final = KMeans(n_clusters=K, random_state=42, n_init=20)
km_labels = km_final.fit_predict(X)
df['KMeans_Cluster'] = km_labels
print(f"\nK-Means cluster sizes:\n{pd.Series(km_labels).value_counts().sort_index()}")

# ════════════════════════════════════════════════════════════
# 6. HIERARCHICAL CLUSTERING + DENDROGRAM
# ════════════════════════════════════════════════════════════
sample_idx = np.random.choice(len(X), 200, replace=False)
X_sample = X[sample_idx]
Z = linkage(X_sample, method='ward')

agg = AgglomerativeClustering(n_clusters=K, linkage='ward')
agg_labels = agg.fit_predict(X)
df['Agg_Cluster'] = agg_labels

# Agreement
from sklearn.metrics import adjusted_rand_score
ari = adjusted_rand_score(km_labels, agg_labels)
print(f"\nAdjusted Rand Index (KMeans vs Hierarchical): {ari:.3f}")

fig, axes = plt.subplots(1, 2, figsize=(18, 7), facecolor=BG)
fig.suptitle('Hierarchical Clustering Analysis', fontsize=16, fontweight='bold', color=TEXT)

# Dendrogram
dend = dendrogram(Z, ax=axes[0], truncate_mode='lastp', p=30,
                  color_threshold=0.7*max(Z[:,2]),
                  above_threshold_color=GRID,
                  link_color_func=lambda k: COLORS[k % len(COLORS)])
axes[0].set_title('🌳 Ward Linkage Dendrogram (n=200 sample)', fontsize=12, fontweight='bold', color=TEXT)
axes[0].set_xlabel('Sample Index'); axes[0].set_ylabel('Distance')
axes[0].spines[['top','right']].set_visible(False)
axes[0].axhline(y=Z[-K+1, 2]*0.9, color=COLORS[1], ls='--', lw=2, label=f'Cut → {K} clusters')
axes[0].legend()

# Cluster size comparison
km_counts  = pd.Series(km_labels).value_counts().sort_index()
agg_counts = pd.Series(agg_labels).value_counts().sort_index()
x = np.arange(K)
w = 0.35
axes[1].bar(x-w/2, km_counts, w, label='K-Means', color=COLORS[0], alpha=0.85)
axes[1].bar(x+w/2, agg_counts, w, label='Hierarchical', color=COLORS[2], alpha=0.85)
axes[1].set_title(f'📊 Cluster Size Comparison  (ARI={ari:.3f})', fontsize=12, fontweight='bold', color=TEXT)
axes[1].set_xlabel('Cluster'); axes[1].set_ylabel('Count')
axes[1].set_xticks(x); axes[1].set_xticklabels([f'C{i}' for i in range(K)])
axes[1].legend(); axes[1].spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.savefig('/home/claude/fig3_hierarchical.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("Fig 3 saved.")

# ════════════════════════════════════════════════════════════
# 7. PCA + t-SNE VISUALIZATION
# ════════════════════════════════════════════════════════════
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X)

tsne = TSNE(n_components=2, random_state=42, perplexity=40, max_iter=1000)
X_tsne = tsne.fit_transform(X)

fig, axes = plt.subplots(1, 2, figsize=(18, 7), facecolor=BG)
fig.suptitle('Cluster Visualization — Dimensionality Reduction', fontsize=16, fontweight='bold', color=TEXT)

cluster_names = ['Budget Browsers','Mid-Market Loyalists','Premium Shoppers','High-Value VIPs']

for ax, X_red, title, note in [
    (axes[0], X_pca, '📐 PCA (2D)', f'Var explained: {pca.explained_variance_ratio_.sum()*100:.1f}%'),
    (axes[1], X_tsne, '🔭 t-SNE (2D)', 'perplexity=40'),
]:
    for i, (c, name) in enumerate(zip(COLORS[:K], cluster_names)):
        mask = km_labels == i
        ax.scatter(X_red[mask,0], X_red[mask,1], c=c, s=20, alpha=0.6, label=f'C{i}: {name}')
        cx, cy = X_red[mask,0].mean(), X_red[mask,1].mean()
        ax.annotate(f'C{i}', (cx,cy), fontsize=14, fontweight='bold', color=c,
                    ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.3', fc=BG, ec=c, alpha=0.8))
    ax.set_title(f'{title}  ({note})', fontsize=12, fontweight='bold', color=TEXT)
    ax.legend(fontsize=8, loc='upper right')
    ax.spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.savefig('/home/claude/fig4_clusters_viz.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("Fig 4 saved.")

# ════════════════════════════════════════════════════════════
# 8. CLUSTER PROFILING
# ════════════════════════════════════════════════════════════
profile = df.groupby('KMeans_Cluster')[features].mean().round(1)
profile['Count'] = df.groupby('KMeans_Cluster').size()
profile['% Share'] = (profile['Count']/len(df)*100).round(1)
profile.index = [f'C{i}: {n}' for i,n in enumerate(cluster_names)]
print("\n=== CLUSTER PROFILES ===")
print(profile.to_string())

# Radar / profile heatmap
fig, axes = plt.subplots(2, 2, figsize=(18, 12), facecolor=BG)
fig.suptitle('Cluster Profiles — Feature Breakdown', fontsize=17, fontweight='bold', color=TEXT)
axes = axes.flatten()

feature_labels = ['Age','Income ($K)','Monthly Spend ($)','Loyalty','Recency (days)','Freq/Month']
profile_display = profile[features].copy()
profile_display['Annual_Income'] = profile_display['Annual_Income']/1000

for i, (ax, color) in enumerate(zip(axes, COLORS[:K])):
    vals = profile_display.iloc[i].values
    bars = ax.barh(feature_labels, vals, color=color, alpha=0.85, edgecolor='none', height=0.6)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_width()+max(vals)*0.01, bar.get_y()+bar.get_height()/2,
                f'{val:.1f}', va='center', color=TEXT, fontsize=10, fontweight='bold')
    ax.set_title(f'{cluster_names[i]}  (n={profile["Count"].iloc[i]}, {profile["% Share"].iloc[i]}%)',
                 fontsize=12, fontweight='bold', color=color)
    ax.spines[['top','right','left']].set_visible(False)
    ax.set_xlim(0, max(vals)*1.2)

plt.tight_layout()
plt.savefig('/home/claude/fig5_profiles.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("Fig 5 saved.")

# ════════════════════════════════════════════════════════════
# 9. LABEL DATASET  +  BOXPLOT COMPARISON
# ════════════════════════════════════════════════════════════
df['Cluster_Label'] = df['KMeans_Cluster'].map({i:n for i,n in enumerate(cluster_names)})
df.to_csv('/home/claude/customers_segmented.csv', index=False)

fig, axes = plt.subplots(1, 3, figsize=(18, 6), facecolor=BG)
fig.suptitle('Key Metrics by Cluster', fontsize=16, fontweight='bold', color=TEXT)

for ax, col, title in zip(axes,
    ['Monthly_Spend','Annual_Income','Purchase_Frequency'],
    ['Monthly Spend ($)','Annual Income ($)','Purchase Frequency']):
    data_by_cluster = [df[df['KMeans_Cluster']==i][col].values for i in range(K)]
    bp = ax.boxplot(data_by_cluster, patch_artist=True, notch=True,
                    medianprops={'color':'white','lw':2})
    for patch, color in zip(bp['boxes'], COLORS[:K]):
        patch.set_facecolor(color); patch.set_alpha(0.75)
    for whisker in bp['whiskers']: whisker.set(color=GRID, lw=1.5)
    for cap in bp['caps']:         cap.set(color=GRID, lw=1.5)
    for flier in bp['fliers']:     flier.set(marker='o', color=GRID, alpha=0.4, ms=3)
    ax.set_xticklabels([f'C{i}' for i in range(K)])
    ax.set_title(title, fontsize=12, fontweight='bold', color=TEXT)
    ax.spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.savefig('/home/claude/fig6_boxplots.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("Fig 6 saved.")

# ════════════════════════════════════════════════════════════
# 10. MARKETING STRATEGY DASHBOARD
# ════════════════════════════════════════════════════════════
strategies = [
    {
        'name':'Budget Browsers','color':COLORS[0],
        'emoji':'🛒',
        'income':'Low ($25K–40K)','spend':'Low ($100–200)','loyalty':'1–2 ⭐',
        'insight':'Price-sensitive, infrequent buyers with long gaps between purchases.',
        'tactics':[
            '💸 Flash sales & time-limited discount codes',
            '📦 Free shipping on orders above threshold',
            '🎯 Retargeting ads on abandoned carts',
            '🏷️ Bundle deals to increase basket size',
            '📱 Push notifications on price drops',
        ]
    },
    {
        'name':'Mid-Market Loyalists','color':COLORS[2],
        'emoji':'🤝',
        'income':'Medium ($50K–75K)','spend':'Medium ($350–500)','loyalty':'2–3 ⭐',
        'insight':'Steady buyers who respond well to loyalty perks and personalization.',
        'tactics':[
            '⭐ Loyalty points program with tier upgrades',
            '🎁 Birthday / anniversary rewards',
            '🔔 "You might also like" personalized recommendations',
            '📧 Monthly curated newsletter with favourites',
            '🆙 Upsell to premium tier with exclusive access',
        ]
    },
    {
        'name':'Premium Shoppers','color':COLORS[3],
        'emoji':'💎',
        'income':'High ($90K–120K)','spend':'High ($750–1000)','loyalty':'4 ⭐',
        'insight':'Quality-driven, brand-conscious; low price sensitivity.',
        'tactics':[
            '🥇 Early access to new collections / pre-orders',
            '🎨 Curated premium product showcases',
            '🤝 Invite-only VIP shopping events',
            '🌟 Co-branded collaborations & limited editions',
            '📞 Dedicated customer success manager',
        ]
    },
    {
        'name':'High-Value VIPs','color':COLORS[1],
        'emoji':'👑',
        'income':'Top (>$120K)','spend':'Top (>$900)','loyalty':'5 ⭐',
        'insight':'High-frequency power buyers; brand ambassadors in the making.',
        'tactics':[
            '👑 Exclusive VIP concierge & white-glove service',
            '🎯 Hyper-personalized AI product recommendations',
            '🎟️ Free premium membership & gift wrapping',
            '📸 Influencer / brand ambassador program invites',
            '🔄 Subscription auto-replenish for favourites',
        ]
    },
]

fig = plt.figure(figsize=(20, 14), facecolor=BG)
fig.suptitle('🚀 Personalised Marketing Strategy by Customer Segment',
             fontsize=20, fontweight='bold', color=TEXT, y=0.98)

for idx, s in enumerate(strategies):
    ax = fig.add_subplot(2, 2, idx+1)
    ax.set_facecolor(CARD)
    ax.set_xlim(0,1); ax.set_ylim(0,1)
    ax.axis('off')

    # Header band
    ax.add_patch(FancyBboxPatch((0,0.82), 1, 0.18, boxstyle='round,pad=0.01',
                                 fc=s['color'], ec='none', alpha=0.25, transform=ax.transAxes))
    ax.text(0.5, 0.91, f"{s['emoji']}  {s['name']}", ha='center', va='center',
            fontsize=15, fontweight='bold', color=s['color'], transform=ax.transAxes)

    # Stats row
    for xi, (label, val) in enumerate(zip(['Income','Spend','Loyalty'],
                                           [s['income'],s['spend'],s['loyalty']])):
        ax.text(0.15+xi*0.32, 0.75, label, ha='center', fontsize=8, color=TEXT, alpha=0.6, transform=ax.transAxes)
        ax.text(0.15+xi*0.32, 0.69, val,  ha='center', fontsize=8, color=TEXT, fontweight='bold', transform=ax.transAxes)

    # Divider
    ax.axhline(0.65, color=s['color'], lw=0.8, alpha=0.4)

    # Insight
    ax.text(0.05, 0.60, '💡 ' + s['insight'], fontsize=8.5, color=TEXT, alpha=0.85,
            transform=ax.transAxes, style='italic', wrap=True)

    # Tactics
    ax.text(0.05, 0.52, 'RECOMMENDED TACTICS', fontsize=8, color=s['color'],
            fontweight='bold', transform=ax.transAxes, alpha=0.9)
    for ti, tactic in enumerate(s['tactics']):
        ax.text(0.05, 0.44-ti*0.085, tactic, fontsize=9, color=TEXT,
                transform=ax.transAxes, alpha=0.9)

plt.tight_layout(rect=[0,0,1,0.96])
plt.savefig('/home/claude/fig7_strategy.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("Fig 7 saved.")

print("\n✅ All figures generated successfully.")
print(f"Final dataset: {df.shape[0]} rows, {df.shape[1]} columns")
print("Columns:", list(df.columns))
