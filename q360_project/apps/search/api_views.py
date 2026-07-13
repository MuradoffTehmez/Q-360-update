from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from apps.accounts.models import User
from apps.competencies.models import Competency
from apps.training.models import TrainingResource
from apps.departments.models import Department

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_api_view(request):
    """
    Standardized API endpoint for global search functionality
    """
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return Response({'error': 'Query must be at least 2 characters'}, status=400)
    
    results = []
    
    # Search in users
    user_results = User.objects.annotate(
        search=SearchVector('first_name', 'last_name', 'username', 'email'),
        rank=SearchRank(SearchVector('first_name', 'last_name', 'username', 'email'), SearchQuery(query))
    ).filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(username__icontains=query) |
        Q(email__icontains=query) |
        Q(search=SearchQuery(query))
    ).order_by('-rank')[:10]
    
    for user in user_results:
        results.append({
            'id': user.id,
            'title': user.get_full_name() or user.username,
            'content': f"İstifadəçi - {user.email}",
            'url': f'/accounts/profile/{user.id}/',
            'category': 'İstifadəçilər',
            'model': 'user',
            'rank': float(getattr(user, 'rank', 0))
        })
    
    # Search in competencies
    competency_results = Competency.objects.annotate(
        search=SearchVector('name', 'description'),
        rank=SearchRank(SearchVector('name', 'description'), SearchQuery(query))
    ).filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(search=SearchQuery(query))
    ).order_by('-rank')[:10]
    
    for comp in competency_results:
        results.append({
            'id': comp.id,
            'title': comp.name,
            'content': comp.description[:100] + '...' if len(comp.description) > 100 else comp.description,
            'url': f'/competencies/{comp.id}/',
            'category': 'Kompetensiyalar',
            'model': 'competency',
            'rank': float(getattr(comp, 'rank', 0))
        })
    
    # Search in training resources
    training_results = TrainingResource.objects.annotate(
        search=SearchVector('title', 'description'),
        rank=SearchRank(SearchVector('title', 'description'), SearchQuery(query))
    ).filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(search=SearchQuery(query))
    ).order_by('-rank')[:10]
    
    for training in training_results:
        results.append({
            'id': training.id,
            'title': training.title,
            'content': training.description[:100] + '...' if len(training.description) > 100 else training.description,
            'url': f'/training/{training.id}/',
            'category': 'Təlimlər',
            'model': 'training',
            'rank': float(getattr(training, 'rank', 0))
        })
    
    # Search in departments
    department_results = Department.objects.annotate(
        search=SearchVector('name', 'description'),
        rank=SearchRank(SearchVector('name', 'description'), SearchQuery(query))
    ).filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(search=SearchQuery(query))
    ).order_by('-rank')[:10]
    
    for dept in department_results:
        results.append({
            'id': dept.id,
            'title': dept.name,
            'content': dept.description[:100] + '...' if len(dept.description) > 100 else dept.description,
            'url': f'/departments/{dept.id}/',
            'category': 'Şöbələr',
            'model': 'department',
            'rank': float(getattr(dept, 'rank', 0))
        })
    
    # Sort all results by rank
    results.sort(key=lambda x: x['rank'], reverse=True)
    
    return Response({
        'query': query,
        'results': results,
        'count': len(results)
    })
