import requests
import json
import os
import time

SERVER_URL = "https://openapi.sandeshai.in"

LOGIN_CACHE_FILE = 'login_cache.json'

def make_request(endpoint, data=None, method='GET', headers=None):
    url = SERVER_URL + endpoint
    if headers is None:
        headers = {}
    headers['Content-Type'] = 'application/json'
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data, timeout=10)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            print(f"Unsupported HTTP method: {method}")
            return None

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        try:
            return response.json()
        except ValueError:
            print(f"HTTP error occurred: {e}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}")
        return None

def save_login_cache(auth_token, expires_at):
    with open(LOGIN_CACHE_FILE, 'w') as f:
        json.dump({'auth_token': auth_token, 'expires_at': expires_at}, f)

def load_login_cache():
    if os.path.exists(LOGIN_CACHE_FILE):
        with open(LOGIN_CACHE_FILE, 'r') as f:
            data = json.load(f)
            return data.get('auth_token'), data.get('expires_at')
    return None, None

def clear_login_cache():
    if os.path.exists(LOGIN_CACHE_FILE):
        os.remove(LOGIN_CACHE_FILE)

def refresh_token(auth_token):
    data = {'auth_token': auth_token}
    response = make_request('/refresh_token', data=data, method='POST')
    if response and 'auth_token' in response:
        new_token = response['auth_token']
        expires_at = int(time.time()) + 300  # Token valid for 5 minutes
        save_login_cache(new_token, expires_at)
        return new_token
    else:
        print("Failed to refresh token.")
        clear_login_cache()
        return None

def get_valid_token():
    auth_token, expires_at = load_login_cache()
    if auth_token and expires_at:
        current_time = int(time.time())
        if current_time >= expires_at:
            # Token expired, refresh it
            print("Token expired. Refreshing token...")
            auth_token = refresh_token(auth_token)
        elif expires_at - current_time <= 60:
            # Token about to expire in 1 minute, refresh it
            print("Token about to expire. Refreshing token...")
            auth_token = refresh_token(auth_token)
    else:
        auth_token = None
    return auth_token

def register():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    data = {'email': email, 'password': password}
    response = make_request('/register', data=data, method='POST')
    if response:
        print(response.get('message', response.get('error')))
        if 'message' in response:
            code = input("Enter the verification code sent to your email: ")
            verify_data = {'email': email, 'code': code}
            verify_response = make_request('/verify_email', data=verify_data, method='POST')
            if verify_response:
                print(verify_response.get('message', verify_response.get('error')))
    else:
        print("Registration failed due to a network error.")

def login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    data = {'email': email, 'password': password}
    response = make_request('/login', data=data, method='POST')
    if response:
        print(response.get('message', response.get('error')))
        if 'auth_token' in response:
            auth_token = response['auth_token']
            expires_at = int(time.time()) + 300  # Token valid for 5 minutes
            save_login_cache(auth_token, expires_at)
            return auth_token
        else:
            return None
    else:
        print("Login failed due to a network error.")
        return None

def logout():
    auth_token = get_valid_token()
    if not auth_token:
        print("You are not logged in.")
        return
    headers = {'Authorization': auth_token}
    response = make_request('/logout', method='POST', headers=headers)
    if response:
        print(response.get('message', response.get('error')))
        if 'message' in response:
            clear_login_cache()
    else:
        print("Logout failed due to a network error.")

def request_password_reset():
    email = input("Enter your email: ")
    data = {'email': email}
    response = make_request('/request_password_reset', data=data, method='POST')
    if response:
        print(response.get('message', response.get('error')))
    else:
        print("Password reset request failed due to a network error.")

def reset_password():
    email = input("Enter your email: ")
    code = input("Enter the reset code sent to your email: ")
    new_password = input("Enter your new password: ")
    data = {'email': email, 'code': code, 'new_password': new_password}
    response = make_request('/reset_password', data=data, method='POST')
    if response:
        print(response.get('message', response.get('error')))
    else:
        print("Password reset failed due to a network error.")

def list_api_keys():
    auth_token = get_valid_token()
    if not auth_token:
        print("Please login again.")
        return
    headers = {'Authorization': auth_token}
    response = make_request('/api_keys', headers=headers)
    if response:
        if 'api_keys' in response:
            if response['api_keys']:
                for key in response['api_keys']:
                    status = 'Active' if key['is_active'] else 'Inactive'
                    print(f"ID: {key['id']}, Key: {key['key']}, Status: {status}, Created At: {key['created_at']}")
            else:
                print("No API keys found.")
        else:
            print(response.get('error'))
    else:
        print("Failed to retrieve API keys due to a network error.")

def create_api_key():
    auth_token = get_valid_token()
    if not auth_token:
        print("Please login again.")
        return
    headers = {'Authorization': auth_token}
    response = make_request('/api_keys', method='POST', headers=headers)
    if response:
        print(response.get('message', response.get('error')))
        if 'api_key' in response:
            print(f"Your new API key: {response['api_key']}")
    else:
        print("Failed to create API key due to a network error.")

def delete_api_key():
    auth_token = get_valid_token()
    if not auth_token:
        print("Please login again.")
        return
    key_id = input("Enter the ID of the API key to delete: ")
    headers = {'Authorization': auth_token}
    response = make_request(f'/api_keys/{key_id}', method='DELETE', headers=headers)
    if response:
        print(response.get('message', response.get('error')))
    else:
        print("Failed to delete API key due to a network error.")

def deactivate_api_key():
    auth_token = get_valid_token()
    if not auth_token:
        print("Please login again.")
        return
    key_id = input("Enter the ID of the API key to deactivate: ")
    headers = {'Authorization': auth_token}
    response = make_request(f'/api_keys/{key_id}/deactivate', method='POST', headers=headers)
    if response:
        print(response.get('message', response.get('error')))
    else:
        print("Failed to deactivate API key due to a network error.")

def activate_api_key():
    auth_token = get_valid_token()
    if not auth_token:
        print("Please login again.")
        return
    key_id = input("Enter the ID of the API key to activate: ")
    headers = {'Authorization': auth_token}
    response = make_request(f'/api_keys/{key_id}/activate', method='POST', headers=headers)
    if response:
        print(response.get('message', response.get('error')))
    else:
        print("Failed to activate API key due to a network error.")

def delete_account():
    auth_token = get_valid_token()
    if not auth_token:
        print("Please login again.")
        return
    confirm = input("Are you sure you want to delete your account? This action cannot be undone. (y/n): ")
    if confirm.lower() == 'y':
        headers = {'Authorization': auth_token}
        response = make_request('/delete_account', method='DELETE', headers=headers)
        if response:
            print(response.get('message', response.get('error')))
            if 'message' in response:
                clear_login_cache()
        else:
            print("Failed to delete account due to a network error.")

def main():
    print("Welcome to the Client Interface")
    while True:
        auth_token = get_valid_token()
        if auth_token:
            print("You are logged in.")
            while True:
                print("\nDashboard:")
                print("1. List API Keys")
                print("2. Create New API Key")
                print("3. Delete API Key")
                print("4. Deactivate API Key")
                print("5. Activate API Key")
                print("6. Delete Account")
                print("7. Logout")
                choice = input("Select an option: ")
                if choice == '1':
                    list_api_keys()
                elif choice == '2':
                    create_api_key()
                elif choice == '3':
                    delete_api_key()
                elif choice == '4':
                    deactivate_api_key()
                elif choice == '5':
                    activate_api_key()
                elif choice == '6':
                    delete_account()
                    break
                elif choice == '7':
                    logout()
                    break
                else:
                    print("Invalid option.")
        else:
            print("\nMenu:")
            print("1. Register")
            print("2. Login")
            print("3. Request Password Reset")
            print("4. Reset Password")
            print("5. Exit")
            choice = input("Select an option: ")
            if choice == '1':
                register()
            elif choice == '2':
                login()
            elif choice == '3':
                request_password_reset()
            elif choice == '4':
                reset_password()
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("Invalid option.")

if __name__ == '__main__':
    main()
