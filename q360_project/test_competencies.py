import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from apps.competencies.models import Competency, ProficiencyLevel, PositionCompetency, UserSkill
from apps.departments.models import Organization, Department, Position
from apps.competencies.services import calculate_user_skill_gap

User = get_user_model()

# 1. Create a competency
comp, created = Competency.objects.get_or_create(
    name="System Architecture",
    description="Designing complex systems",
    is_active=True
)
print(f"Competency created/exists: {comp.name}")

# 2. Create proficiency level
level_adv, _ = ProficiencyLevel.objects.get_or_create(
    name="advanced",
    defaults={"display_name": "Advanced", "score_min": 70, "score_max": 89}
)
level_exp, _ = ProficiencyLevel.objects.get_or_create(
    name="expert",
    defaults={"display_name": "Expert", "score_min": 90, "score_max": 100}
)
print(f"Levels ready: {level_adv.name}, {level_exp.name}")

# 3. Create Org/Dept/Position
org, _ = Organization.objects.get_or_create(name="Tech Corp")
dept, _ = Department.objects.get_or_create(name="Engineering", organization=org)
pos, _ = Position.objects.get_or_create(title="Senior Architect", department=dept, organization=org, is_active=True)

# 4. Bind Competency to Position
PositionCompetency.objects.get_or_create(
    position=pos,
    competency=comp,
    required_level=level_exp,
    weight=1.0,
    is_mandatory=True
)

# 5. Create user and assign skill
user, _ = User.objects.get_or_create(username="architect_user", email="arch@test.com")
user.position = pos.title
user.save()

UserSkill.objects.get_or_create(
    user=user,
    competency=comp,
    level=level_adv,  # user has advanced, but expert is required -> GAP!
    is_approved=True
)

# 6. Test skill gap service
gap_result = calculate_user_skill_gap(user)
print("--- SKILL GAP RESULTS ---")
print(f"Total Required: {gap_result['total_required']}")
print(f"With Gap: {gap_result['with_gap']}")
print(f"Without Gap: {gap_result['without_gap']}")
for req in gap_result['required_competencies']:
    print(f"  - Competency: {req['competency'].name}")
    print(f"    Required Level: {req['required_level'].score_min}")
    print(f"    Current Level: {req['current_level']}")
    print(f"    GAP: {req['gap']}")
    print(f"    Has Gap: {req['has_gap']}")

print("SUCCESS: 1.4 Verification complete.")
