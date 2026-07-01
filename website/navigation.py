from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NavigationItem:
    label: str
    section_id: str
    icon: str


PRIMARY_NAVIGATION = (
    NavigationItem(
        label="overview",
        section_id="overview",
        icon="icons/green_triangle.svg",
    ),
    NavigationItem(
        label="works",
        section_id="works",
        icon="icons/pink_circle.svg",
    ),
    NavigationItem(
        label="about us",
        section_id="about",
        icon="icons/blue_star.svg",
    ),
    NavigationItem(
        label="services",
        section_id="services",
        icon="icons/yellow_square.svg",
    ),
    NavigationItem(
        label="contact",
        section_id="contact",
        icon="icons/green_triangle.svg",
    ),
)
