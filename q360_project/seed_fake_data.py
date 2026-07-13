import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.contenttypes.models import ContentType

from apps.workflow_engine.models import WorkflowTemplate, WorkflowStep
from apps.approval_engine.models import ApprovalChain, ApprovalNode
from apps.access_control.models import Role, AbacPolicy
from apps.policy_engine.models import Policy
from apps.feature_flags.models import FeatureFlag

def seed_data():
    print("Seeding Fake Data...")

    # Workflow Engine
    wt1, _ = WorkflowTemplate.objects.get_or_create(name="Məzuniyyət Təsdiqi", description="İşçilərin məzuniyyətə çıxma axını", is_active=True)
    wt2, _ = WorkflowTemplate.objects.get_or_create(name="Ezamiyyət İş Axını", description="Ezamiyyətə göndərilmə və təsdiqlənmə axını", is_active=False)
    
    # Approval Engine
    ac1, _ = ApprovalChain.objects.get_or_create(name="Standart Təsdiq", description="Departament rəhbəri və HR tərəfindən təsdiq", is_active=True)
    ac2, _ = ApprovalChain.objects.get_or_create(name="Büdcə Təsdiqi", description="Maliyyə şöbəsinin mütləq təsdiqi", is_active=True)

    # Access Control
    r1, _ = Role.objects.get_or_create(name="HR Manager", description="İnsan Resursları Meneceri", is_system=True)
    r2, _ = Role.objects.get_or_create(name="Employee", description="Standart İşçi", is_system=True)
    
    # Policy Engine
    p1, _ = Policy.objects.get_or_create(name="İşdən Çıxma Siyasəti", category="HR", description="İşçinin xitam prosesi qaydaları")
    p2, _ = Policy.objects.get_or_create(name="Məlumat Təhlükəsizliyi", category="IT", description="Parol dəyişmə və giriş siyasətləri")

    # Feature Flags
    f1, _ = FeatureFlag.objects.get_or_create(name="AI_SCREENING", description="AI əsaslı namizəd qiymətləndirməsi", is_active=True, percentage_rollout=50)
    f2, _ = FeatureFlag.objects.get_or_create(name="NEW_UI_DASHBOARD", description="Yeni dizaynlı Dashboard ekranı", is_active=False, percentage_rollout=0)

    print("Seeding Complete!")

if __name__ == '__main__':
    seed_data()
