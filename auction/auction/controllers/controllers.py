from django.http import JsonResponse

def test_view(request):
    data = {'message': 'This is a test endpoint'}
    return JsonResponse(data)
