if [[ -z $API_DOMAIN ]]; then
    echo "ERROR: Must provide API_DOMAIN in environment" 1>&2
    exit 1
fi


echo "export const BASE_BACKEND_URL = 'http://$API_DOMAIN/api';

export const HEADERS = {
  Authorization: 'Authorization',
  xSignature: 'X-Signature'
};" > $1