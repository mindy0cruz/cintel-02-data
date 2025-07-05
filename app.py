import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from shiny import App, ui, render
from shinywidgets import output_widget, render_plotly, render_widget
from palmerpenguins import load_penguins


penguins_df = load_penguins()

# Define UI
app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.sidebar(
            ui.h2("Sidebar"),
            ui.input_selectize(
                "selected_attribute",
                "Select Attribute:",
                ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
            ),
            ui.input_numeric(
                "plotly_bin_count",
                "Plotly Histogram Bins:",
                value=15,
            ),
            ui.input_slider(
                "seaborn_bin_count",
                "Seaborn Histogram Bins:",
                min=5,
                max=50,
                value=28,
            ),
            ui.input_checkbox_group(
                "selected_species_list",
                "Species Type:",
                ["Adelie", "Gentoo", "Chinstrap"],
                selected=["Adelie", "Gentoo", "Chinstrap"],
                inline=True,
            ),
            ui.hr(),
            ui.a(
                "GitHub Link",
                href="https://github.com/mindy0cruz/cintel-02-data",
                target="_blank",
            ),
            open="open"
        ),

        ui.layout_columns(
            ui.output_data_frame("data_table"),
            ui.output_data_frame("data_grid"),
        ),

        ui.layout_columns(
            output_widget("plotly_histogram"),
            ui.output_plot("seaborn_histogram"),
        ),

        ui.card(
            ui.card_header("Plotly Scatterplot: Species"),
            output_widget("plotly_scatterplot"),
            full_screen=True,
        ),
    )
)

def server(input, output, session):

    @render.data_frame
    def data_table():
        return penguins_df[
            penguins_df["species"].isin(input.selected_species_list())
        ]

    @render.data_frame
    def data_grid():
        return penguins_df[
            penguins_df["species"].isin(input.selected_species_list())
        ]

    @render_plotly
    def plotly_histogram():
        col = input.selected_attribute()
        bins = input.plotly_bin_count() 
        filtered = penguins_df[
            penguins_df["species"].isin(input.selected_species_list())
        ]
        fig = px.histogram(
            filtered,
            x=col,
            nbins=bins,
            color="species",
            title=f"Plotly Histogram"
        )
        return fig

    @render.plot
    def seaborn_histogram():
        col = input.selected_attribute()
        bins = input.seaborn_bin_count()
        filtered = penguins_df[
            penguins_df["species"].isin(input.selected_species_list())
        ]
        fig, ax = plt.subplots()
        sns.histplot(
            data=filtered,
            x=col,
            bins=bins,
            kde=True,
            hue="species",
            ax=ax
        )
        ax.set_title(f"Seaborn Histogram")
        return fig

    @render_plotly
    def plotly_scatterplot():
        filtered = penguins_df[
            penguins_df["species"].isin(input.selected_species_list())
        ]
        fig = px.scatter(
            filtered,
            x="flipper_length_mm",
            y="body_mass_g",
            color="species",
            hover_data=["island"],
            title="Plotly Scatterplot:Species",
            labels={
                "flipper_length_mm": "Flipper Length (mm)",
                "body_mass_g": "Body Mass (g)",
            },
        )
        return fig


app = App(app_ui, server)
