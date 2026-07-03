from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Service:
    name: str
    description: str
    icon_path: str
    icon_width: int
    icon_height: int
    color: str


SERVICES = (
    Service(
        name="Website",
        description=(
            "Connect and convert with website content that clearly "
            "communicates your mission and speaks to what your people care "
            "about."
        ),
        icon_path="icons/blue_star.svg",
        icon_width=126,
        icon_height=120,
        color="blue",
    ),
    Service(
        name="Branding",
        description=(
            "Set your brand apart with a design and copy guide curated to what "
            "you and your audience stand for."
        ),
        icon_path="icons/green_triangle.svg",
        icon_width=120,
        icon_height=120,
        color="green",
    ),
    Service(
        name="Advertising",
        description=(
            "Break into new channels and reach the right people with paid "
            "social ads designed to grab attention and drive immediate action."
        ),
        icon_path="icons/pink_square.svg",
        icon_width=110,
        icon_height=110,
        color="pink",
    ),
    Service(
        name="Social Media",
        description=(
            "Boost brand awareness and build trust with social media content "
            "that stops the scroll, transcends trends, and fully represents "
            "you."
        ),
        icon_path="icons/yellow_circle.svg",
        icon_width=118,
        icon_height=119,
        color="gold",
    ),
    Service(
        name="Print",
        description=(
            "Expand your reach with print advertising, including direct mail, "
            "posters, billboards, brochures, flyers, business cards, and more."
        ),
        icon_path="icons/yellow_star.svg",
        icon_width=126,
        icon_height=120,
        color="gold",
    ),
    Service(
        name="Email",
        description=(
            "Build lasting relationships with thoughtful email campaigns that "
            "keep your audience informed, engaged, and ready to act."
        ),
        icon_path="icons/green_square.svg",
        icon_width=110,
        icon_height=110,
        color="green",
    ),
)
