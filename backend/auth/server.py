from concurrent import futures
import grpc
import jwt
import datetime
import hashlib
import sqlite3
import os
import auth_pb2_grpc
from auth_pb2 import *
from auth_pb2_grpc import AuthServiceServicer

# JWT Configuration
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION = 24 * 60 * 60  # 24 hours

class AuthService(AuthServiceServicer):
    def __init__(self):
        self.db_path = 'users.db'
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                email TEXT UNIQUE,
                password TEXT,
                full_name TEXT,
                avatar_url TEXT,
                status TEXT,
                is_online BOOLEAN,
                last_seen TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def generate_token(self, username):
        expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXPIRATION)
        return jwt.encode(
            {'username': username, 'exp': expiration},
            JWT_SECRET,
            algorithm=JWT_ALGORITHM
        )

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload['username']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def VerifyToken(self, request, context):
        username = self.verify_token(request.token)
        if not username:
            return VerifyTokenResponse(
                success=False,
                message="Invalid or expired token"
            )
        
        return VerifyTokenResponse(
            success=True,
            username=username,
            message="Token verified successfully"
        )

    def Register(self, request, context):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        try:
            # Check if username exists
            c.execute('SELECT username FROM users WHERE username = ?', (request.username,))
            if c.fetchone():
                return AuthResponse(
                    success=False,
                    message="Username already exists"
                )

            # Check if email exists
            c.execute('SELECT email FROM users WHERE email = ?', (request.email,))
            if c.fetchone():
                return AuthResponse(
                    success=False,
                    message="Email already exists"
                )

            # Insert new user
            c.execute('''
                INSERT INTO users (username, email, password, full_name, avatar_url, status, is_online, last_seen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                request.username,
                request.email,
                self.hash_password(request.password),
                request.full_name,
                request.avatar_url,
                "Available",
                True,
                datetime.datetime.utcnow()
            ))
            conn.commit()

            # Generate token
            token = self.generate_token(request.username)

            return AuthResponse(
                success=True,
                token=token,
                message="Registration successful",
                profile=UserProfile(
                    username=request.username,
                    email=request.email,
                    full_name=request.full_name,
                    avatar_url=request.avatar_url,
                    status="Available",
                    is_online=True,
                    last_seen=datetime.datetime.utcnow().isoformat()
                )
            )

        except Exception as e:
            return AuthResponse(
                success=False,
                message=f"Registration failed: {str(e)}"
            )
        finally:
            conn.close()

    def Login(self, request, context):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        try:
            # Verify credentials
            c.execute('''
                SELECT username, email, full_name, avatar_url, status, is_online, last_seen
                FROM users
                WHERE username = ? AND password = ?
            ''', (request.username, self.hash_password(request.password)))
            
            user = c.fetchone()
            if not user:
                return AuthResponse(
                    success=False,
                    message="Invalid credentials"
                )

            # Generate token
            token = self.generate_token(request.username)

            # Update online status
            c.execute('''
                UPDATE users
                SET is_online = TRUE, last_seen = ?
                WHERE username = ?
            ''', (datetime.datetime.utcnow(), request.username))
            conn.commit()

            return AuthResponse(
                success=True,
                token=token,
                message="Login successful",
                profile=UserProfile(
                    username=user[0],
                    email=user[1],
                    full_name=user[2],
                    avatar_url=user[3],
                    status=user[4],
                    is_online=user[5],
                    last_seen=user[6]
                )
            )

        except Exception as e:
            return AuthResponse(
                success=False,
                message=f"Login failed: {str(e)}"
            )
        finally:
            conn.close()

    def GetProfile(self, request, context):
        username = self.verify_token(request.token)
        if not username:
            return ProfileResponse(
                success=False,
                message="Invalid or expired token"
            )

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        try:
            c.execute('''
                SELECT username, email, full_name, avatar_url, status, is_online, last_seen
                FROM users
                WHERE username = ?
            ''', (request.username,))
            
            user = c.fetchone()
            if not user:
                return ProfileResponse(
                    success=False,
                    message="User not found"
                )

            return ProfileResponse(
                success=True,
                message="Profile retrieved successfully",
                profile=UserProfile(
                    username=user[0],
                    email=user[1],
                    full_name=user[2],
                    avatar_url=user[3],
                    status=user[4],
                    is_online=user[5],
                    last_seen=user[6]
                )
            )

        except Exception as e:
            return ProfileResponse(
                success=False,
                message=f"Failed to get profile: {str(e)}"
            )
        finally:
            conn.close()

    def UpdateProfile(self, request, context):
        username = self.verify_token(request.token)
        if not username:
            return ProfileResponse(
                success=False,
                message="Invalid or expired token"
            )

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        try:
            c.execute('''
                UPDATE users
                SET full_name = ?, avatar_url = ?, status = ?, is_online = ?, last_seen = ?
                WHERE username = ?
            ''', (
                request.full_name,
                request.avatar_url,
                request.status,
                request.is_online,
                request.last_seen,
                request.username
            ))
            conn.commit()

            return self.GetProfile(request, context)

        except Exception as e:
            return ProfileResponse(
                success=False,
                message=f"Failed to update profile: {str(e)}"
            )
        finally:
            conn.close()

    def ChangePassword(self, request, context):
        username = self.verify_token(request.token)
        if not username:
            return AuthResponse(
                success=False,
                message="Invalid or expired token"
            )

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        try:
            # Verify old password
            c.execute('''
                SELECT password FROM users WHERE username = ?
            ''', (request.username,))
            
            current_password = c.fetchone()[0]
            if current_password != self.hash_password(request.old_password):
                return AuthResponse(
                    success=False,
                    message="Invalid old password"
                )

            # Update password
            c.execute('''
                UPDATE users
                SET password = ?
                WHERE username = ?
            ''', (
                self.hash_password(request.new_password),
                request.username
            ))
            conn.commit()

            return AuthResponse(
                success=True,
                message="Password changed successfully"
            )

        except Exception as e:
            return AuthResponse(
                success=False,
                message=f"Failed to change password: {str(e)}"
            )
        finally:
            conn.close()

    def Logout(self, request, context):
        username = self.verify_token(request.token)
        if not username:
            return AuthResponse(
                success=False,
                message="Invalid or expired token"
            )

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        try:
            c.execute('''
                UPDATE users
                SET is_online = FALSE, last_seen = ?
                WHERE username = ?
            ''', (datetime.datetime.utcnow(), request.username))
            conn.commit()

            return AuthResponse(
                success=True,
                message="Logged out successfully"
            )

        except Exception as e:
            return AuthResponse(
                success=False,
                message=f"Logout failed: {str(e)}"
            )
        finally:
            conn.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("🔐 AuthService running at [::]:50053")
    server.wait_for_termination()

if __name__ == '__main__':
    serve() 