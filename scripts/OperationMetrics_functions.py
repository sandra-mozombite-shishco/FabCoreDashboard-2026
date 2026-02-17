def total_students_served(df_regOper):

    df = df_regOper.copy()

    df = df[
        (df['Usuario FAB'].notna()) & # Filter only rows with 'Usuario FAB' not null
        (df['Tipo de usuario'].str.contains('pregrado|maestría', case=False, na=False)) # Looks for pregrado or maestria words in 'Tipo de usuario', ignores case and handles NaN values
    ]
    return df['Usuario FAB'].nunique() #Unique count of 'Usuario FAB' in the filtered dataframe



    #Date formtas:
    # dt.month_name() -> Month name
    # dt.year -> Year
    # dt.day_name() -> Day name
    # dt.isocalendar().week -> Week number