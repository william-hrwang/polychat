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

import shutil

<<<<<<< HEAD

def safe_connect(db_path='users.db'):
    if not os.path.exists(db_path):
        print("users.db is missing at runtime. Attempting to restore from backup...")
        if os.path.exists('users_backup.db'):
            shutil.copyfile('users_backup.db', db_path)
            print("Runtime restoration successful.")
        else:
            print("No backup found. Starting with empty DB.")
=======
def backup_sqlite_db():
    original_db = 'users.db'
    backup_db = 'users_backup.db'
    try:
        shutil.copyfile(original_db, backup_db)
        print("✅ Database successfully backed up to 'users_backup.db'")
    except Exception as e:
        print(f"❌ Failed to back up database: {e}")

def safe_connect(db_path='users.db'):
    if not os.path.exists(db_path):
        print("⚠️ users.db is missing at runtime. Attempting to restore from backup...")
        if os.path.exists('users_backup.db'):
            shutil.copyfile('users_backup.db', db_path)
            print("✅ Runtime restoration successful.")
        else:
            print("❌ No backup found. Starting with empty DB.")
>>>>>>> RAFT-2
    return sqlite3.connect(db_path)

# JWT Configuration
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION = 24 * 60 * 60  # 24 hours

class AuthService(AuthServiceServicer):
    def __init__(self):
        self.db_path = 'users.db'
        if not os.path.exists(self.db_path):
<<<<<<< HEAD
            print("Primary database not found. Trying to use backup.")
            if os.path.exists('users_backup.db'):
                shutil.copyfile('users_backup.db', self.db_path)
                print("Restored from backup.")
            else:
                print("Backup also not found. Starting fresh.")
=======
            print("⚠️ Primary database not found. Trying to use backup.")
            if os.path.exists('users_backup.db'):
                shutil.copyfile('users_backup.db', self.db_path)
                print("✅ Restored from backup.")
            else:
                print("❌ Backup also not found. Starting fresh.")
>>>>>>> RAFT-2
        self.init_db()
    def init_db(self):
        conn = safe_connect(self.db_path)
        c = conn.cursor()

        # Create the users table if it doesn't exist
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                email TEXT UNIQUE,
                password TEXT,
                full_name TEXT,
                avatar_url TEXT,
                avatar_data BLOB,
                status TEXT,
                is_online BOOLEAN,
                last_seen TIMESTAMP
            )
        ''')

        # Check if avatar_data column exists, if not add it
        c.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in c.fetchall()]
        if 'avatar_data' not in columns:
            print("📝 Adding avatar_data column to users table")
            c.execute('ALTER TABLE users ADD COLUMN avatar_data BLOB')

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
<<<<<<< HEAD
        print(f"Register: Full request details:")
        print(f"Username: {request.username}")
        print(f"Email: {request.email}")
        print(f"Full name: {request.full_name}")
        print(f"Has avatar_url: {bool(request.avatar_url)}")
=======
        print(f"🔍 Register: Full request details:")
        print(f"🔍 Username: {request.username}")
        print(f"🔍 Email: {request.email}")
        print(f"🔍 Full name: {request.full_name}")
        print(f"🔍 Has avatar_url: {bool(request.avatar_url)}")
>>>>>>> RAFT-2

        # Check if avatar_data exists in the request
        has_avatar_data = False
        try:
            has_avatar_data = hasattr(request, 'avatar_data') and request.avatar_data and len(request.avatar_data) > 0
            print(f"🔍 Has avatar_data attribute: {hasattr(request, 'avatar_data')}")
            if hasattr(request, 'avatar_data'):
                print(f"🔍 Avatar data type: {type(request.avatar_data)}")
                print(f"🔍 Avatar data length: {len(request.avatar_data) if request.avatar_data else 0}")
        except Exception as e:
<<<<<<< HEAD
            print(f"Error checking avatar_data: {str(e)}")

        print(f"Register: Attempting to register user {request.username}")
        print(f"Register: Has avatar data: {has_avatar_data}")
        print(f"Register: Has avatar URL: {bool(request.avatar_url)}")
=======
            print(f"❌ Error checking avatar_data: {str(e)}")

        print(f"📤 Register: Attempting to register user {request.username}")
        print(f"📤 Register: Has avatar data: {has_avatar_data}")
        print(f"📤 Register: Has avatar URL: {bool(request.avatar_url)}")
>>>>>>> RAFT-2

        conn = conn = safe_connect(self.db_path)
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

<<<<<<< HEAD
            print(f"Register: Attempting to register user {request.username}")
            print(f"Register: Has avatar data: {bool(request.avatar_data)}")
            print(f"Register: Has avatar URL: {bool(request.avatar_url)}")
            if request.avatar_data:
                print(f"Register: Avatar data size: {len(request.avatar_data)} bytes")
=======
            print(f"📤 Register: Attempting to register user {request.username}")
            print(f"📤 Register: Has avatar data: {bool(request.avatar_data)}")
            print(f"📤 Register: Has avatar URL: {bool(request.avatar_url)}")
            if request.avatar_data:
                print(f"📤 Register: Avatar data size: {len(request.avatar_data)} bytes")
>>>>>>> RAFT-2

            # Insert new user
            try:
                avatar_data_bytes = None
                if hasattr(request, 'avatar_data') and request.avatar_data:
<<<<<<< HEAD
                    print(f"Register: Converting avatar data to bytes, length: {len(request.avatar_data)}")
                    avatar_data_bytes = bytes(request.avatar_data)
                    print(f"Register: Converted avatar data to bytes, length: {len(avatar_data_bytes)}")
=======
                    print(f"📤 Register: Converting avatar data to bytes, length: {len(request.avatar_data)}")
                    avatar_data_bytes = bytes(request.avatar_data)
                    print(f"📤 Register: Converted avatar data to bytes, length: {len(avatar_data_bytes)}")
>>>>>>> RAFT-2

                c.execute('''
                    INSERT INTO users (
                        username, email, password, full_name, 
                        avatar_url, avatar_data, status, is_online, last_seen
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    request.username,
                    request.email,
                    self.hash_password(request.password),
                    request.full_name,
                    request.avatar_url,
                    avatar_data_bytes,
                    "Available",
                    True,
                    datetime.datetime.utcnow()
                ))
<<<<<<< HEAD
                print(f"Register: Executed INSERT statement")
                conn.commit()
                print(f"Register: Committed changes to database")

                backup_sqlite_db()  # Backup the database after registering the user
                print("Database backup completed after user registration.")
            except Exception as e:
                print(f"Register: Error inserting user: {str(e)}")
=======
                print(f"📤 Register: Executed INSERT statement")
                conn.commit()
                print(f"📤 Register: Committed changes to database")

                backup_sqlite_db()  # Backup the database after registering the user
                print("📦 Database backup completed after user registration.")
            except Exception as e:
                print(f"❌ Register: Error inserting user: {str(e)}")
>>>>>>> RAFT-2
                raise e  # Re-raise to be caught by outer exception handler

            # Verify the insertion
            c.execute('''
                SELECT username, email, full_name, avatar_url, avatar_data, status, is_online, last_seen
                FROM users
                WHERE username = ?
            ''', (request.username,))
            user = c.fetchone()

            if user:
<<<<<<< HEAD
                print(f"Register: Successfully registered user {request.username}")
                if user[4]:  # avatar_data
                    print(f"Register: Stored avatar data size: {len(user[4])} bytes")
            else:
                print(f"Register: Failed to verify user registration for {request.username}")
=======
                print(f"✅ Register: Successfully registered user {request.username}")
                if user[4]:  # avatar_data
                    print(f"✅ Register: Stored avatar data size: {len(user[4])} bytes")
            else:
                print(f"❌ Register: Failed to verify user registration for {request.username}")
>>>>>>> RAFT-2

            # Generate token
            token = self.generate_token(request.username)

            return AuthResponse(
                success=True,
                token=token,
                message="Registration successful",
                profile=UserProfile(
                    username=user[0],
                    email=user[1],
                    full_name=user[2],
                    avatar_url=user[3],
                    status=user[5],
                    is_online=user[6],
                    last_seen=user[7]
                )
            )

        except Exception as e:
<<<<<<< HEAD
            print(f"Register: Error during registration: {str(e)}")
=======
            print(f"❌ Register: Error during registration: {str(e)}")
>>>>>>> RAFT-2
            return AuthResponse(
                success=False,
                message=f"Registration failed: {str(e)}"
            )
        finally:
            conn.close()

    def Login(self, request, context):
<<<<<<< HEAD
        print(f"Login: Attempt for user {request.username}")
=======
        print(f"🔑 Login: Attempt for user {request.username}")
>>>>>>> RAFT-2

        conn = conn = safe_connect(self.db_path)
        c = conn.cursor()
        
        try:
            # First check if user exists and get stored password
            c.execute('SELECT password FROM users WHERE username = ?', (request.username,))
            stored_password_row = c.fetchone()

            if not stored_password_row:
<<<<<<< HEAD
                print(f"Login: User {request.username} not found")
=======
                print(f"❌ Login: User {request.username} not found")
>>>>>>> RAFT-2
                return AuthResponse(
                    success=False,
                    message="Invalid credentials"
                )

            stored_password = stored_password_row[0]
            submitted_hash = self.hash_password(request.password)

<<<<<<< HEAD
            print(f"Login: Comparing passwords")
            print(f"Login: Stored hash: {stored_password}")
            print(f"Login: Submitted hash: {submitted_hash}")
=======
            print(f"🔍 Login: Comparing passwords")
            print(f"🔍 Login: Stored hash: {stored_password}")
            print(f"🔍 Login: Submitted hash: {submitted_hash}")
>>>>>>> RAFT-2

            # Verify credentials
            c.execute('''
                SELECT username, email, full_name, avatar_url, status, is_online, last_seen
                FROM users
                WHERE username = ? AND password = ?
            ''', (request.username, submitted_hash))
            
            user = c.fetchone()
            if not user:
<<<<<<< HEAD
                print(f"Login: Password mismatch for {request.username}")
=======
                print(f"❌ Login: Password mismatch for {request.username}")
>>>>>>> RAFT-2
                return AuthResponse(
                    success=False,
                    message="Invalid credentials"
                )

<<<<<<< HEAD
            print(f"Login: Successful for {request.username}")
=======
            print(f"✅ Login: Successful for {request.username}")
>>>>>>> RAFT-2

            # Generate token
            token = self.generate_token(request.username)

            # Update online status
            c.execute('''
                UPDATE users
                SET is_online = TRUE, last_seen = ?
                WHERE username = ?
            ''', (datetime.datetime.utcnow(), request.username))
            conn.commit()

            backup_sqlite_db()  # Backup the database after user login
<<<<<<< HEAD
            print("Database backup completed after user login.")
=======
            print("📦 Database backup completed after user login.")
>>>>>>> RAFT-2



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

<<<<<<< HEAD

=======
>>>>>>> RAFT-2
    def GetProfile(self, request, context):
        username = self.verify_token(request.token)
        if not username:
            return ProfileResponse(
                success=False,
                message="Invalid or expired token"
            )

        conn = conn = safe_connect(self.db_path)
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
<<<<<<< HEAD
        username = self.verify_token(request.token)
        if not username:
=======
        token_username = self.verify_token(request.token)
        if not token_username:
>>>>>>> RAFT-2
            return ProfileResponse(
                success=False,
                message="Invalid or expired token"
            )

<<<<<<< HEAD
=======
        if request.username != token_username:
            return ProfileResponse(
                success=False,
                message="Token username mismatch"
            )


>>>>>>> RAFT-2
        conn = safe_connect(self.db_path)
        c = conn.cursor()
        
        try:
            c.execute('''
                UPDATE users
                SET full_name = ?,
                    avatar_url = ?,
                    status = ?,
                    is_online = ?,
                    last_seen = ?
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
            
           
<<<<<<< HEAD
            backup_sqlite_db()  # backup added here
            print("Database backup completed after profile update.")
=======
            backup_sqlite_db()  # ✅ backup added here
            print("📦 Database backup completed after profile update.")
>>>>>>> RAFT-2
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

        conn = safe_connect(self.db_path)
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

        conn = safe_connect(self.db_path)
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

    def UploadAvatar(self, request, context):
        username = self.verify_token(request.token)
        if not username:
<<<<<<< HEAD
            print(f"UploadAvatar: Invalid token for user {request.username}")
=======
            print(f"❌ UploadAvatar: Invalid token for user {request.username}")
>>>>>>> RAFT-2
            return UploadAvatarResponse(
                success=False,
                message="Invalid or expired token"
            )

<<<<<<< HEAD
        print(f"UploadAvatar: Attempting to upload avatar for user {request.username}")

        if not request.image_data or len(request.image_data) == 0:
            print(f"UploadAvatar: No image data provided (length: {len(request.image_data) if request.image_data else 0})")
=======
        print(f"📤 UploadAvatar: Attempting to upload avatar for user {request.username}")

        if not request.image_data or len(request.image_data) == 0:
            print(f"❌ UploadAvatar: No image data provided (length: {len(request.image_data) if request.image_data else 0})")
>>>>>>> RAFT-2
            return UploadAvatarResponse(
                success=False,
                message="No image data provided"
            )

<<<<<<< HEAD
        print(f"UploadAvatar: Image data size: {len(request.image_data)} bytes")
        print(f"UploadAvatar: First 20 bytes: {request.image_data[:20]}")
=======
        print(f"📤 UploadAvatar: Image data size: {len(request.image_data)} bytes")
        print(f"📤 UploadAvatar: First 20 bytes: {request.image_data[:20]}")
>>>>>>> RAFT-2

        conn = safe_connect(self.db_path)
        c = conn.cursor()

        try:
            # First check if user exists
            c.execute('SELECT username FROM users WHERE username = ?', (request.username,))
            if not c.fetchone():
<<<<<<< HEAD
                print(f"UploadAvatar: User {request.username} not found")
=======
                print(f"❌ UploadAvatar: User {request.username} not found")
>>>>>>> RAFT-2
                return UploadAvatarResponse(
                    success=False,
                    message="User not found"
                )

            c.execute('''
                UPDATE users
                SET avatar_data = ?,
                    avatar_url = NULL
                WHERE username = ?
            ''', (request.image_data, request.username))
            conn.commit()

            # Verify the update
            c.execute('SELECT avatar_data FROM users WHERE username = ?', (request.username,))
            result = c.fetchone()
            if result and result[0]:
<<<<<<< HEAD
                print(f"UploadAvatar: Successfully stored avatar for user {request.username}")
                print(f"UploadAvatar: Stored image size: {len(result[0])} bytes")
            else:
                print(f"UploadAvatar: Failed to verify avatar storage for user {request.username}")
=======
                print(f"✅ UploadAvatar: Successfully stored avatar for user {request.username}")
                print(f"✅ UploadAvatar: Stored image size: {len(result[0])} bytes")
            else:
                print(f"❌ UploadAvatar: Failed to verify avatar storage for user {request.username}")
>>>>>>> RAFT-2

            return UploadAvatarResponse(
                success=True,
                message="Avatar uploaded successfully"
            )

        except Exception as e:
<<<<<<< HEAD
            print(f"UploadAvatar: Error uploading avatar: {str(e)}")
=======
            print(f"❌ UploadAvatar: Error uploading avatar: {str(e)}")
>>>>>>> RAFT-2
            return UploadAvatarResponse(
                success=False,
                message=f"Failed to upload avatar: {str(e)}"
            )
        finally:
            conn.close()

    def GetAvatar(self, request, context):
        username = self.verify_token(request.token)
        if not username:
<<<<<<< HEAD
            print(f"GetAvatar: Invalid token for user {request.username}")
=======
            print(f"❌ GetAvatar: Invalid token for user {request.username}")
>>>>>>> RAFT-2
            return GetAvatarResponse(
                success=False,
                message="Invalid or expired token"
            )

<<<<<<< HEAD
        print(f"GetAvatar: Attempting to get avatar for user {request.username}")
=======
        print(f"📥 GetAvatar: Attempting to get avatar for user {request.username}")
>>>>>>> RAFT-2

        conn = safe_connect(self.db_path)
        c = conn.cursor()

        try:
            c.execute('''
                SELECT avatar_data, avatar_url
                FROM users
                WHERE username = ?
            ''', (request.username,))

            result = c.fetchone()
            if not result:
<<<<<<< HEAD
                print(f"GetAvatar: User {request.username} not found")
=======
                print(f"❌ GetAvatar: User {request.username} not found")
>>>>>>> RAFT-2
                return GetAvatarResponse(
                    success=False,
                    message="User not found"
                )

            avatar_data, avatar_url = result
<<<<<<< HEAD
            print(f"GetAvatar: Found user {request.username}")
            print(f"GetAvatar: Has avatar data: {bool(avatar_data)}")
            print(f"GetAvatar: Has avatar URL: {bool(avatar_url)}")
            if avatar_data:
                print(f"GetAvatar: Avatar data size: {len(avatar_data)} bytes")

            if avatar_data:
                print(f"GetAvatar: Returning binary avatar data for user {request.username}")
=======
            print(f"📥 GetAvatar: Found user {request.username}")
            print(f"📥 GetAvatar: Has avatar data: {bool(avatar_data)}")
            print(f"📥 GetAvatar: Has avatar URL: {bool(avatar_url)}")
            if avatar_data:
                print(f"📥 GetAvatar: Avatar data size: {len(avatar_data)} bytes")

            if avatar_data:
                print(f"✅ GetAvatar: Returning binary avatar data for user {request.username}")
>>>>>>> RAFT-2
                return GetAvatarResponse(
                    success=True,
                    message="Avatar found",
                    image_data=avatar_data,
                    image_url=""
                )
            elif avatar_url:
<<<<<<< HEAD
                print(f"GetAvatar: Returning avatar URL for user {request.username}: {avatar_url}")
=======
                print(f"✅ GetAvatar: Returning avatar URL for user {request.username}: {avatar_url}")
>>>>>>> RAFT-2
                return GetAvatarResponse(
                    success=True,
                    message="Avatar URL found",
                    image_data=b"",
                    image_url=avatar_url
                )
            else:
<<<<<<< HEAD
                print(f"ℹGetAvatar: No avatar found for user {request.username}")
=======
                print(f"ℹ️ GetAvatar: No avatar found for user {request.username}")
>>>>>>> RAFT-2
                return GetAvatarResponse(
                    success=True,
                    message="No avatar found",
                    image_data=b"",
                    image_url=""
                )

        except Exception as e:
<<<<<<< HEAD
            print(f"GetAvatar: Error getting avatar: {str(e)}")
=======
            print(f"❌ GetAvatar: Error getting avatar: {str(e)}")
>>>>>>> RAFT-2
            return GetAvatarResponse(
                success=False,
                message=f"Failed to get avatar: {str(e)}",
                image_data=b"",
                image_url=""
            )
        finally:
            conn.close()

    def GetAllUsers(self, request, context):
        # Verify token first
        username = self.verify_token(request.token)
        if not username:
            return GetAllUsersResponse(
                success=False,
                message="Invalid or expired token"
            )

        conn = safe_connect(self.db_path)
        c = conn.cursor()
        
        try:
            # Get all users except the requesting user
            c.execute('''
                SELECT username, email, full_name, avatar_url, status, is_online, last_seen
                FROM users
                WHERE username != ?
                ORDER BY username
            ''', (username,))
            
            users = []
            for user in c.fetchall():
                users.append(UserProfile(
                    username=user[0],
                    email=user[1],
                    full_name=user[2],
                    avatar_url=user[3],
                    status=user[4],
                    is_online=user[5],
                    last_seen=user[6]
                ))

            return GetAllUsersResponse(
                success=True,
                message="Users retrieved successfully",
                users=users
            )

        except Exception as e:
<<<<<<< HEAD
            print(f"Error getting all users: {str(e)}")
=======
            print(f"❌ Error getting all users: {str(e)}")
>>>>>>> RAFT-2
            return GetAllUsersResponse(
                success=False,
                message=f"Failed to get users: {str(e)}"
            )
        finally:
            conn.close()

<<<<<<< HEAD
def backup_sqlite_db():
    original_db = 'users.db'
    backup_db = 'users_backup.db'
    try:
        shutil.copyfile(original_db, backup_db)
        print("Database successfully backed up to 'users_backup.db'")
    except Exception as e:
        print(f"Failed to back up database: {e}")


=======
>>>>>>> RAFT-2
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("🔐 AuthService running at [::]:50053")
    server.wait_for_termination()

if __name__ == '__main__':
    serve() 