from shiny import App, render, ui, reactive
import pandas as pd
import altair as alt
from shinywidgets import render_altair, output_widget

#Importing dataset
visitor_data = pd.read_excel("/Users/nidhi/Documents/GitHub/commercialisation_national_parks/Tourism Data Anlaysis/National Park Visit Data.xlsx")

#Melting data for easier plotting
visitor_data_long = visitor_data.melt(id_vars="Year", var_name="Park", value_name="Visitors")

#First we build the basic dashboard with an input select for parks and a plot with yearly trend line


#Server Side
# Shiny Server Logic
def app_server(input, output, session):
    @reactive.Calc
    def filtered_data():
        if input.switch_button():  # If toggle is ON, show all parks
            return visitor_data_long
        else:  # If toggle is OFF, filter for the selected park
            selected_park = input.Park()
            return visitor_data_long[visitor_data_long['Park'] == selected_park]
    

    # Render Altair plot using shinywidgets
    @output
    @render_altair
    def visitor_plot():
        selected_data = filtered_data()

        if input.switch_button():  # Comparative plot for two parks
            line_chart = (
                alt.Chart(selected_data)
                .mark_line(point=True)
                .encode(
                    x=alt.X('Year:O', title='Year'),
                    y=alt.Y('Visitors:Q', title='Number of Visitors'),
                    color=alt.Color('Park:N', legend=alt.Legend(title="Park")),  # Differentiates parks by color
                    tooltip=['Year', 'Park', 'Visitors'],  # Add tooltips
                )
                .properties(
                    title="Comparative Visitor Trends",
                    width=600,
                    height=400,
                )
            )
        else:  # Single park plot
            line_chart = (
                alt.Chart(selected_data)
                .mark_line(point=True)
                .encode(
                    x=alt.X('Year:O', title='Year'),
                    y=alt.Y('Visitors:Q', title='Number of Visitors'),
                    tooltip=['Year', 'Visitors'],  # Add tooltips
                    color=alt.value('blue'),  # Single park color
                )
                .properties(
                    title=f"Visitor Trends for {input.Park()}",
                    width=600,
                    height=400,
                )
            )


#UI
app_ui = ui.page_fluid(
    ui.h2("National Park Visitor Trend"),
    ui.input_switch("switch_button", "Toggle to see comparitive chart", value=False),
    ui.input_select(
        "Park",
        "Select National Park:",
        choices=list(visitor_data_long['Park'].unique()) 
    ),
    output_widget("visitor_plot")  # Use output_plot for Altair rendering
)


app = App(app_ui, app_server)





