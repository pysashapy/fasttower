```python
SMTP = {
    'default': {
        'backend': 'fasttower.email.backends.AIOEmailBackend',
        'hostname': 'localhost',
        'port': 1,
        'username': str,
        'password': str,
        'user_tls': bool,
        'start_tls': bool
    }
}

```