"""
Utility functions and helper methods
"""
from datetime import datetime
from functools import wraps
import re

def validate_location(location):
    """
    Validate location string
    
    Args:
        location: Location string
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not location or len(location.strip()) < 2:
        return False, "Location must be at least 2 characters"
    
    if len(location) > 200:
        return False, "Location is too long (max 200 characters)"
    
    return True, ""

def sanitize_input(text, max_length=None):
    """
    Sanitize user input to prevent XSS and other attacks
    
    Args:
        text: Input text
        max_length: Maximum allowed length
    
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Strip whitespace
    text = text.strip()
    
    # Remove potential HTML tags (basic sanitization)
    text = re.sub(r'<[^>]*>', '', text)
    
    # Truncate if needed
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text

def format_datetime(dt, format_string='%Y-%m-%d %H:%M:%S'):
    """
    Format datetime object to string
    
    Args:
        dt: datetime object
        format_string: Format string
    
    Returns:
        str: Formatted datetime string
    """
    if not dt:
        return None
    
    return dt.strftime(format_string)

def parse_datetime(dt_string, format_string='%Y-%m-%d %H:%M:%S'):
    """
    Parse datetime string to datetime object
    
    Args:
        dt_string: Datetime string
        format_string: Format string
    
    Returns:
        datetime: Parsed datetime object
    """
    try:
        return datetime.strptime(dt_string, format_string)
    except (ValueError, TypeError):
        return None

def get_severity_color(severity):
    """
    Get color code for alert severity
    
    Args:
        severity: Alert severity level
    
    Returns:
        str: Color code
    """
    colors = {
        'LOW': '#28a745',      # Green
        'MEDIUM': '#ffc107',   # Yellow
        'HIGH': '#fd7e14',     # Orange
        'CRITICAL': '#dc3545'  # Red
    }
    return colors.get(severity.upper(), '#6c757d')

def get_severity_icon(severity):
    """
    Get emoji icon for alert severity
    
    Args:
        severity: Alert severity level
    
    Returns:
        str: Icon/emoji
    """
    icons = {
        'LOW': 'ℹ️',
        'MEDIUM': '⚠️',
        'HIGH': '🚨',
        'CRITICAL': '🔴'
    }
    return icons.get(severity.upper(), '📢')

def paginate_query(query, page, per_page):
    """
    Helper function to paginate SQLAlchemy queries
    
    Args:
        query: SQLAlchemy query object
        page: Page number (1-indexed)
        per_page: Items per page
    
    Returns:
        dict: Pagination data
    """
    total = query.count()
    items = query.limit(per_page).offset((page - 1) * per_page).all()
    
    return {
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    }

def is_valid_severity(severity):
    """
    Check if severity level is valid
    
    Args:
        severity: Severity level to check
    
    Returns:
        bool: True if valid, False otherwise
    """
    from config import Config
    return severity.upper() in Config.ALERT_SEVERITIES

def is_valid_status(status):
    """
    Check if alert status is valid
    
    Args:
        status: Status to check
    
    Returns:
        bool: True if valid, False otherwise
    """
    from config import Config
    return status.upper() in Config.ALERT_STATUSES

def build_api_response(data=None, message=None, error=None, status_code=200):
    """
    Build standardized API response
    
    Args:
        data: Response data
        message: Success message
        error: Error message
        status_code: HTTP status code
    
    Returns:
        tuple: (response_dict, status_code)
    """
    response = {}
    
    if error:
        response['error'] = error
    
    if message:
        response['message'] = message
    
    if data is not None:
        response['data'] = data
    
    response['timestamp'] = datetime.utcnow().isoformat()
    
    return response, status_code

def get_client_ip(request):
    """
    Get client IP address from request
    
    Args:
        request: Flask request object
    
    Returns:
        str: Client IP address
    """
    # Check for proxy headers
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr

def calculate_alert_priority(severity, created_at):
    """
    Calculate alert priority score for sorting
    Higher score = higher priority
    
    Args:
        severity: Alert severity
        created_at: When alert was created
    
    Returns:
        int: Priority score
    """
    severity_scores = {
        'CRITICAL': 1000,
        'HIGH': 100,
        'MEDIUM': 10,
        'LOW': 1
    }
    
    base_score = severity_scores.get(severity.upper(), 0)
    
    # Add time component (recent alerts get slight boost)
    time_diff = datetime.utcnow() - created_at
    time_score = max(0, 100 - time_diff.days)
    
    return base_score + time_score

def truncate_text(text, max_length, suffix='...'):
    """
    Truncate text to specified length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated
    
    Returns:
        str: Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests = {}
    
    def is_allowed(self, key, max_requests=100, window_seconds=3600):
        """
        Check if request is allowed based on rate limit
        
        Args:
            key: Unique identifier (e.g., IP address)
            max_requests: Maximum requests allowed
            window_seconds: Time window in seconds
        
        Returns:
            bool: True if allowed, False if rate limit exceeded
        """
        now = datetime.utcnow()
        
        if key not in self.requests:
            self.requests[key] = []
        
        # Remove old requests outside the window
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if (now - req_time).total_seconds() < window_seconds
        ]
        
        # Check if limit exceeded
        if len(self.requests[key]) >= max_requests:
            return False
        
        # Add current request
        self.requests[key].append(now)
        return True
    
    def reset(self, key):
        """Reset rate limit for a key"""
        if key in self.requests:
            del self.requests[key]

# Global rate limiter instance
rate_limiter = RateLimiter()


"""
Credits:
    Raj & Om: Logic, Code and Idea
    AI Chatbots: Optimization, Formatting
"""

