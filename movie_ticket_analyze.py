import pandas as pd
import plotly.express as px

df = pd.read_excel('電影票房.xlsx')

df_sorted = df.sort_values(by=['start', 'tickets'], ascending=[True, False])

fig = px.bar(df_sorted, x='name', y='tickets', color='start',
             title='Number of Tickets for Each Movie',
             labels={'tickets': 'Number of Tickets', 'start': 'Start Date'})

fig.show()