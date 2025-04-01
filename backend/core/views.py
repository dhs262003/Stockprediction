from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
import json
from .utils import load_stock_symbols, get_current_stock_price
from .mongo_service import (
    get_model_metadata,
    get_news,
    get_user_watchlist,
    add_stock_to_watchlist,
    update_stock_in_watchlist,
    mark_stock_as_sold
)

def model_metadata_view(request):
    data = get_model_metadata()
    return JsonResponse(data, safe=False)

@csrf_exempt
def news_view(request):
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 30))
    skip = (page - 1) * limit
    newsData = get_news(skip=skip, limit=limit)
    return JsonResponse(newsData, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class UserWatchlistView(View):
    def get(self, request):
        user_email = request.GET.get('userMailId')
        data = get_user_watchlist(user_email)
        if data:
            return JsonResponse(data, safe=False)
        return JsonResponse({"message": "No data found"}, status=404)

    def post(self, request):
        body = json.loads(request.body)
        user_email = body.get('userMailId')
        stock_data = body.get('stock')
        if not user_email or not stock_data:
            return JsonResponse({"error": "Missing data"}, status=400)
        result = add_stock_to_watchlist(user_email, stock_data)
        return JsonResponse({"modified": result})

    def put(self, request):
        body = json.loads(request.body)
        user_email = body.get('userMailId')
        symbol = body.get('symbol')
        update_data = body.get('update')
        if not user_email or not symbol or not update_data:
            return JsonResponse({"error": "Missing data"}, status=400)
        result = update_stock_in_watchlist(user_email, symbol, update_data)
        return JsonResponse({"modified": result})

    def delete(self, request):
        body = json.loads(request.body)
        user_email = body.get('userMailId')
        symbol = body.get('symbol')
        if not user_email or not symbol:
            return JsonResponse({"error": "Missing data"}, status=400)
        result = mark_stock_as_sold(user_email, symbol)
        return JsonResponse({"modified": result})

@csrf_exempt
def allowed_symbols_view(request):
    symbols = load_stock_symbols()
    return JsonResponse({"symbols": list(symbols)})

@csrf_exempt
def get_watchlist_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_email = data.get('userMailId')
        user_data = get_user_watchlist(user_email)

        if not user_data:
            return JsonResponse({'status': 'error', 'message': 'No watchlist found'})

        watchlist = []
        for stock in user_data.get('stock_symbol_list', []):
            if stock.get('status', '').lower() == 'holding':
                symbol = stock.get('symbol')
                current_price = get_current_stock_price(symbol)
                stock['currentPrice'] = current_price
                watchlist.append(stock)

        return JsonResponse({'status': 'success', 'watchlist': watchlist})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    