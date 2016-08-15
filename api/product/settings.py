
# PRODUCT_BASE_URL 

PRODUCT_API = {
    'products'           : {'url' : '/product/products', 'method':'GET'},    
    'product_categories' : {'url' : '/product/categories', 'method':'GET'},
    # 'product_categories' : {'url' : '/product/categories', 'method':'GET'},
}

PRODUCT_COLLECTION_EXPIRE_SECONDS = 604800 # 24 hours * 7 
PRODUCT_DATA_EXPIRE_SECONDS = 300 # 5 minutes

DATE_PATTERN = '^(20\\d{2}|21\\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[1-2]\\d|3[0-1])$'


# PRODUCT_INDEX_URL = 'http://112.74.56.55:5501/pg/product'

