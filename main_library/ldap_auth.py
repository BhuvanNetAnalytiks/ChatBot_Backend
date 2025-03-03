from ldap3 import Server, Connection, ALL 
from ldap3.core.exceptions import LDAPException


def authenticate_ldap_user(ldap_server, base_dn, username, password):
    """
    Authenticates a user against an LDAP server.
    
    :param ldap_server: LDAP server address (e.g., "ldap://127.0.0.1")
    :param base_dn: Base DN for user lookup (e.g., "dc=example,dc=com")
    :param username: Username to authenticate (e.g., "john")
    :param password: Password for authentication
    :return: True if authentication is successful, False otherwise
    """
    user_dn = f"uid={username},ou=People,{base_dn}"

    try:
        server = Server(ldap_server, get_info=ALL)
        conn = Connection(server, user=user_dn, password=password, auto_bind=True)
        conn.unbind()
        return {"status": "success", "message": f"User {username} authenticated successfully."}
    except LDAPException as e:
        return {"status": "error", "message": f"LDAP error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}

    
