import time
import requests
from celery import shared_task
from .models import ServiceCheck

@shared_task
def check_status(service_name, url):
    """
    Task to check the status of a service and log it.
    """
    start_time = time.time()
    try:
        response = requests.get(url, timeout=10)
        response_time_ms = (time.time() - start_time) * 1000
        
        ServiceCheck.objects.create(
            service_name=service_name,
            success=True,
            http_status_code=response.status_code,
            response_time_ms=response_time_ms
        )
        
        return f"{service_name}: Success ({response.status_code})"
    
    except requests.RequestException as e:
        response_time_ms = (time.time() - start_time) * 1000
        ServiceCheck.objects.create(
            service_name=service_name,
            success=False,
            http_status_code=getattr(getattr(e, "response", None), "status_code", None),
            response_time_ms=response_time_ms,
            error=str(e)
        )
        return f"{service_name}: Failed ({str(e)})"
    
@shared_task
def run_all_checks():
    """
    Runs health checks for all services listed in SERVICES_TO_CHECK.
    """
    SERVICES_TO_CHECK = [
    ("REST API", "http://localhost:8000/api/"),
    ("GraphQL API", "http://localhost:8000/graphql/"),
    ("Swagger Docs", "http://localhost:8000/swagger/"),
    ("Admin Panel", "http://localhost:8000/admin/"),
]
    results = []
    for service_name, url in SERVICES_TO_CHECK:
        result = check_status.delay(service_name, url)  # call the task async
        results.append(f"Triggered: {service_name}")

    return results
