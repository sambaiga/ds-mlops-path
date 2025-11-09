from lets_plot import element_blank, element_line, element_rect, element_text, theme

pro_colors = [
    "#0078D4",  # Bright blue (primary accent)
    "#00B294",  # Teal (success/accent)
    "#FF8C00",  # Orange (highlight/accent)
    "#D83B01",  # Red-orange (alert/accent)
    "#5C2D91",  # Purple (secondary accent)
    "#107C10",  # Green (confirmation)
    "#605E5C",  # Neutral gray (text or border)
    "#E1DFDD",  # Light gray (background grid)
]

tablue_colors = ["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377", "#BBBBBB", "#000000"]


def modern_theme(
    show_x_axis: bool = True, font_size: int = 12, line_font_size: float = 1.0, x_axis_angle: int = 0
) -> theme:
    """Create a custom theme for Lets-Plot visualizations.

    Args:
        show_x_axis: Whether to display the x-axis elements.
        font_size: Base font size for text elements.
        line_font_size: Base line width for line elements.
        x_axis_angle: Angle for x-axis text labels.

    Returns:
        A Lets-Plot theme object with customized styles.
    """
    font_family = "Inter, 'Segoe UI', Roboto, sans-serif"
    title_fonts = int(font_size * 1.6)
    subtitle_fonts = int(font_size * 1.4)
    axis_fonts = int(font_size * 1.2)
    result = theme(
        legend_position="top",
        legend_background="blank",
        legend_key=element_blank(),
        panel_background="blank",
        plot_background="blank",
        panel_grid_minor="blank",
        panel_grid_major_y="blank",
        panel_grid_major_x="blank",
        axis_line=element_line(size=line_font_size, color="#606060"),
        axis_ticks=element_line(size=line_font_size, color="#606060"),
        axis_text_x=element_text(angle=x_axis_angle, hjust=1, family=font_family, size=font_size, color="#333333"),
        axis_text_y=element_text(family=font_family, size=font_size, color="#333333"),
        axis_title_x=element_text(family=font_family, size=axis_fonts, color="#222222"),
        axis_title_y=element_text(family=font_family, size=axis_fonts, color="#222222"),
        plot_title=element_text(family=font_family, size=title_fonts, face="bold", hjust=0.5, color="#111111"),
        plot_subtitle=element_text(family=font_family, size=subtitle_fonts, color="#333333"),
        plot_caption=element_text(family=font_family, size=font_size, color="#555555"),
        legend_text=element_text(family=font_family, size=font_size, color="#333333"),
        legend_title=element_text(family=font_family, size=axis_fonts, color="#222222"),
    )

    if not show_x_axis:
        result += theme(axis_ticks_x="blank", axis_text_x="blank", axis_title_x="blank")

    return result
