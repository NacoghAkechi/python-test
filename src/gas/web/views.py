"""HTTP とユースケースをつなぐ（Interface Adapters）。業務ルールの判断はしない。"""

import json

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from gas.billing import CustomerNotFoundError, issue_bill
from gas.web.mailers import DjangoMailer
from gas.web.repositories import DjangoBillRepository, DjangoCustomerRepository


@csrf_exempt
@require_POST
def create_bill(request: HttpRequest) -> JsonResponse:
    payload = json.loads(request.body)
    try:
        bill_id = issue_bill(
            customer_id=payload["customer_id"],
            usage=payload["usage"],
            customers=DjangoCustomerRepository(),
            bills=DjangoBillRepository(),
            mailer=DjangoMailer(),
        )
    except CustomerNotFoundError:
        return JsonResponse({"error": "customer not found"}, status=404)
    except ValueError as error:
        return JsonResponse({"error": str(error)}, status=400)
    return JsonResponse({"bill_id": bill_id}, status=201)
