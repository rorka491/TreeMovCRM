from functools import wraps
from rest_framework.response import Response
from rest_framework.request import Request
from mainapp.views import BaseViewSetWithOrdByOrg



def base_search(func):
    @wraps(func)
    def wrapper(
        self: BaseViewSetWithOrdByOrg, request: Request, *args, **kwargs
    ) -> Response:
        query = request.data.get("query", "").strip()

        if not query:
            return Response({"error": "Пустой запрос"}, status=400)

        words = [word for word in query.split()]

        q: Q = func(self, request, words=words, *args, **kwargs)

        results = self.get_queryset().filter(q)
        serializer = self.serializer_class(results, many=True)
        return Response(serializer.data)

    return wrapper