import logging
from django.utils.timezone import now

logger = logging.getLogger(__name__)

def log_operation(user, action, model, object_id, details=None):
    """Registra una operación del usuario en el sistema"""
    
    log_entry = {
        'timestamp': now().isoformat(),
        'user': user.username if user and user.is_authenticated else 'anonymous',
        'user_id': user.id if user and user.is_authenticated else None,
        'action': action,
        'model': model,
        'object_id': object_id,
        'details': details or {}
    }
    
    logger.info(f"OPERATION: {log_entry}")
    return log_entry


def log_error(request, error, model=None, object_id=None):
    """Registra un error en el sistema"""
    
    log_entry = {
        'timestamp': now().isoformat(),
        'user': request.user.username if request.user.is_authenticated else 'anonymous',
        'path': request.path,
        'method': request.method,
        'error': str(error),
        'model': model,
        'object_id': object_id
    }
    
    logger.error(f"ERROR: {log_entry}")
    return log_entry