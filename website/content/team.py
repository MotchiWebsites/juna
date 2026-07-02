from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TeamMember:
    name: str
    role: str
    description: str
    image_path: str
    image_alt: str
    image_width: int
    image_height: int
    accent: str
    decoration_path: str
    decoration_width: int
    decoration_height: int
    is_reversed: bool = False


TEAM_MEMBERS = (
    TeamMember(
        name="Jun Nguyen",
        role="Art Direction",
        description=(
            "Jun Nguyen is a graphic designer and visual artist with a passion "
            "for branding, performance advertising, and typography. From "
            "digital ads to print, his eye for innovative design helps brands "
            "break the mold, stand out, and make a greater impact."
        ),
        image_path="images/about/duong.jpg",
        image_alt="Jun Nguyen standing outside in downtown Toronto",
        image_width=2000,
        image_height=3000,
        accent="gold",
        decoration_path="icons/yellow_star.svg",
        decoration_width=96,
        decoration_height=96,
    ),
    TeamMember(
        name="Alicia Symons",
        role="Content Strategy",
        description=(
            "Alicia Symons is a performance copywriter and creative strategist "
            "with a background in historical research. From email campaigns to "
            "web content, her knack for understanding audiences and crafting "
            "clear, compelling narratives helps brands connect, convert, and "
            "grow."
        ),
        image_path="images/about/alicia.jpg",
        image_alt="Alicia Symons smiling in an office",
        image_width=2400,
        image_height=2400,
        accent="pink",
        decoration_path="icons/pink_circle.svg",
        decoration_width=96,
        decoration_height=96,
        is_reversed=True,
    ),
)
