"""
Services for competencies app.
"""
from typing import Dict, Any
from .models import UserSkill, PositionCompetency


def calculate_user_skill_gap(user) -> Dict[str, Any]:
    """
    Calculate skill gaps for a user based on their position requirements.
    
    Returns a dictionary containing:
        - required_competencies: list of detailed gap dicts per competency
        - gap_data: dict with labels, required, current, and gap arrays for charts
        - total_required: int
        - with_gap: int
        - without_gap: int
        - avg_gap: float
        - has_position: bool
    """
    position_title = getattr(user, 'position', None)
    position_obj = None
    if position_title:
        from apps.departments.models import Position
        # If position is already a model instance (in case it gets converted to FK later)
        if hasattr(position_title, 'id'):
            position_obj = position_title
        else:
            # Position is a CharField matching the title
            position_obj = Position.objects.filter(title=position_title, department=user.department).first() or \
                           Position.objects.filter(title=position_title).first()

    has_position = position_obj is not None
    
    if not has_position:
        return {
            'required_competencies': [],
            'gap_data': {'labels': [], 'required': [], 'current': [], 'gap': []},
            'total_required': 0,
            'with_gap': 0,
            'without_gap': 0,
            'avg_gap': 0,
            'has_position': False
        }

    # Get user's skills
    user_skills = UserSkill.objects.filter(user=user, is_approved=True).select_related(
        'competency', 'level'
    )

    # Create a mapping of competency to user's current level
    user_skill_map = {
        skill.competency_id: skill.level.score_min if skill.level else 0
        for skill in user_skills
    }

    # Get required competencies for user's position
    required_competencies = []
    gap_data = {
        'labels': [],
        'required': [],
        'current': [],
        'gap': []
    }

    pos_competencies = PositionCompetency.objects.filter(
        position=position_obj
    ).select_related('competency', 'required_level').order_by('-weight')

    for pos_comp in pos_competencies:
        current_level = user_skill_map.get(pos_comp.competency_id, 0)
        required_level = pos_comp.required_level.score_min if pos_comp.required_level else 0
        gap = max(0, required_level - current_level)

        required_competencies.append({
            'competency': pos_comp.competency,
            'required_level': pos_comp.required_level,
            'current_level': current_level,
            'gap': gap,
            'gap_percentage': (gap / required_level * 100) if required_level > 0 else 0,
            'has_gap': gap > 0,
        })

        # Chart data
        gap_data['labels'].append(pos_comp.competency.name[:20])
        gap_data['required'].append(required_level)
        gap_data['current'].append(current_level)
        gap_data['gap'].append(gap)

    # Calculate statistics
    total_required = len(required_competencies)
    with_gap = sum(1 for rc in required_competencies if rc['has_gap'])
    without_gap = total_required - with_gap
    avg_gap = sum(rc['gap'] for rc in required_competencies) / total_required if total_required > 0 else 0

    return {
        'required_competencies': required_competencies,
        'gap_data': gap_data,
        'total_required': total_required,
        'with_gap': with_gap,
        'without_gap': without_gap,
        'avg_gap': round(avg_gap, 2),
        'has_position': True
    }
