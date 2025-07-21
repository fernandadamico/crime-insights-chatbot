from datetime import datetime

def filter_crimes(df, parsed):
    filtered = df

    if parsed['dates']:
        target_dates = [datetime.strptime(d, "%Y-%m").date() for d in parsed['dates'] if len(d) == 7]  # 'YYYY-MM'
        # Note: df['date_only'] is a date, so we compare only year-month:
        filtered = filtered[
            filtered['date'].dt.strftime('%Y-%m').isin([d.strftime('%Y-%m') for d in target_dates])
        ]
    elif parsed['years']:
        filtered = filtered[filtered['date'].dt.year.isin(parsed['years'])]

    if parsed['crime_types']:
        filtered = filtered[filtered['primary_type'].isin(parsed['crime_types'])]

    if parsed['community_areas']:
        filtered = filtered[filtered['community_area'].isin(parsed['community_areas'])]

    return filtered

def summarize_crimes_compact(filtered_df):
    if filtered_df.empty:
        return "No crimes found matching the criteria."

    multi_area = filtered_df['community_area'].nunique() > 1
    multi_crime = filtered_df['primary_type'].nunique() > 1

    if multi_area or multi_crime:
        group_by_cols = ['community_area', 'primary_type']
    else:
        group_by_cols = ['primary_type']

    summary = (
        filtered_df.groupby(group_by_cols)
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(20)
    )

    lines = []
    for _, row in summary.iterrows():
        if 'community_area' in group_by_cols:
            lines.append(f"Community Area {int(row['community_area'])}: {row['count']} {row['primary_type'].lower()}")
        else:
            lines.append(f"{row['count']} {row['primary_type'].lower()}")

    dates = filtered_df['date_only'].unique()
    if len(dates) == 1:
        date_str = dates[0].strftime("%Y-%m-%d")
        summary_text = f"On {date_str}, the following crimes were reported:\n- " + "\n- ".join(lines)
    else:
        date_str = ", ".join(sorted(d.strftime("%Y-%m-%d") for d in dates))
        summary_text = f"On dates {date_str}, the following crimes were reported:\n- " + "\n- ".join(lines)

    return summary_text
