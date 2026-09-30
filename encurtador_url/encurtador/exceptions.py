from rest_framework.exceptions import APIException

class RequisicaoIncompletaEncurtaException(APIException):
    status_code = 422
    default_detail = "Dados incompletos"
    default_code = "DADOS_INCOMPLETOS"

class RequisicaoIncompletaEncurtaURLException(APIException):
    status_code = 422
    default_detail = "Você precisa informar a url"
    default_code = "URL_AUSENTE"

class DuplicidadeURLCadastradaException(APIException):
    status_code = 422
    default_detail = "Url ja cadastrada"
    default_code = "URL_JA_CADASTRADA"

class FalhaNoServidorException(APIException):
    status_code = 500
    default_detail = "Falha no servidor"
    default_code = "FALHA_NO_SERVIDOR"

class URLExpiradaException(APIException):
    status_code = 410
    default_detail = "Url expirada"
    default_code = "URL_EXPIRADA"

class URLNaoEncontradaException(APIException):
    status_code = 404
    default_detail = "URL nao encontrada"
    default_code = "NOT_FOUND"

class URLInvalidaException(APIException):
    status_code = 422
    default_detail = "URL invalida"
    default_code = "URL_INVALIDA"