// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('@grpc/grpc-js');
var auth_pb = require('./auth_pb.js');

function serialize_auth_AuthResponse(arg) {
  if (!(arg instanceof auth_pb.AuthResponse)) {
    throw new Error('Expected argument of type auth.AuthResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_auth_AuthResponse(buffer_arg) {
  return auth_pb.AuthResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_auth_ChangePasswordRequest(arg) {
  if (!(arg instanceof auth_pb.ChangePasswordRequest)) {
    throw new Error('Expected argument of type auth.ChangePasswordRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_auth_ChangePasswordRequest(buffer_arg) {
  return auth_pb.ChangePasswordRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_auth_GetAvatarRequest(arg) {
  if (!(arg instanceof auth_pb.GetAvatarRequest)) {
    throw new Error('Expected argument of type auth.GetAvatarRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_auth_GetAvatarRequest(buffer_arg) {
  return auth_pb.GetAvatarRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_auth_GetAvatarResponse(arg) {
  if (!(arg instanceof auth_pb.GetAvatarResponse)) {
    throw new Error('Expected argument of type auth.GetAvatarResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_auth_GetAvatarResponse(buffer_arg) {
  return auth_pb.GetAvatarResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_auth_LoginRequest(arg) {
  if (!(arg instanceof auth_pb.LoginRequest)) {
    throw new Error('Expected argument of type auth.LoginRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_auth_LoginRequest(buffer_arg) {
  return auth_pb.LoginRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_auth_LogoutRequest(arg) {
  if (!(arg instanceof auth_pb.LogoutRequest)) {
    throw new Error('Expected argument of type auth.LogoutRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_auth_LogoutRequest(buffer_arg) {
  return auth_pb.LogoutRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_auth_ProfileRequest(arg) {
  if (!(arg instanceof auth_pb.ProfileRequest)) {
    throw new Error('Expected argument of type auth.ProfileRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_auth_ProfileRequest(buffer_arg) {
  return auth_pb.ProfileRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_auth_ProfileResponse(arg) {
  if (!(arg instanceof auth_pb.ProfileResponse)) {
    throw new Error('Expected argument of type auth.ProfileResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_auth_ProfileResponse(buffer_arg) {
  return auth_pb.ProfileResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_auth_RegisterRequest(arg) {
  if (!(arg instanceof auth_pb.RegisterRequest)) {
    throw new Error('Expected argument of type auth.RegisterRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_auth_RegisterRequest(buffer_arg) {
  return auth_pb.RegisterRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_auth_UpdateProfileRequest(arg) {
  if (!(arg instanceof auth_pb.UpdateProfileRequest)) {
    throw new Error('Expected argument of type auth.UpdateProfileRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_auth_UpdateProfileRequest(buffer_arg) {
  return auth_pb.UpdateProfileRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_auth_UploadAvatarRequest(arg) {
  if (!(arg instanceof auth_pb.UploadAvatarRequest)) {
    throw new Error('Expected argument of type auth.UploadAvatarRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_auth_UploadAvatarRequest(buffer_arg) {
  return auth_pb.UploadAvatarRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_auth_UploadAvatarResponse(arg) {
  if (!(arg instanceof auth_pb.UploadAvatarResponse)) {
    throw new Error('Expected argument of type auth.UploadAvatarResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_auth_UploadAvatarResponse(buffer_arg) {
  return auth_pb.UploadAvatarResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_auth_VerifyTokenRequest(arg) {
  if (!(arg instanceof auth_pb.VerifyTokenRequest)) {
    throw new Error('Expected argument of type auth.VerifyTokenRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_auth_VerifyTokenRequest(buffer_arg) {
  return auth_pb.VerifyTokenRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_auth_VerifyTokenResponse(arg) {
  if (!(arg instanceof auth_pb.VerifyTokenResponse)) {
    throw new Error('Expected argument of type auth.VerifyTokenResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_auth_VerifyTokenResponse(buffer_arg) {
  return auth_pb.VerifyTokenResponse.deserializeBinary(new Uint8Array(buffer_arg));
}


var AuthServiceService = exports.AuthServiceService = {
  register: {
    path: '/auth.AuthService/Register',
    requestStream: false,
    responseStream: false,
    requestType: auth_pb.RegisterRequest,
    responseType: auth_pb.AuthResponse,
    requestSerialize: serialize_auth_RegisterRequest,
    requestDeserialize: deserialize_auth_RegisterRequest,
    responseSerialize: serialize_auth_AuthResponse,
    responseDeserialize: deserialize_auth_AuthResponse,
  },
  login: {
    path: '/auth.AuthService/Login',
    requestStream: false,
    responseStream: false,
    requestType: auth_pb.LoginRequest,
    responseType: auth_pb.AuthResponse,
    requestSerialize: serialize_auth_LoginRequest,
    requestDeserialize: deserialize_auth_LoginRequest,
    responseSerialize: serialize_auth_AuthResponse,
    responseDeserialize: deserialize_auth_AuthResponse,
  },
  getProfile: {
    path: '/auth.AuthService/GetProfile',
    requestStream: false,
    responseStream: false,
    requestType: auth_pb.ProfileRequest,
    responseType: auth_pb.ProfileResponse,
    requestSerialize: serialize_auth_ProfileRequest,
    requestDeserialize: deserialize_auth_ProfileRequest,
    responseSerialize: serialize_auth_ProfileResponse,
    responseDeserialize: deserialize_auth_ProfileResponse,
  },
  updateProfile: {
    path: '/auth.AuthService/UpdateProfile',
    requestStream: false,
    responseStream: false,
    requestType: auth_pb.UpdateProfileRequest,
    responseType: auth_pb.ProfileResponse,
    requestSerialize: serialize_auth_UpdateProfileRequest,
    requestDeserialize: deserialize_auth_UpdateProfileRequest,
    responseSerialize: serialize_auth_ProfileResponse,
    responseDeserialize: deserialize_auth_ProfileResponse,
  },
  changePassword: {
    path: '/auth.AuthService/ChangePassword',
    requestStream: false,
    responseStream: false,
    requestType: auth_pb.ChangePasswordRequest,
    responseType: auth_pb.AuthResponse,
    requestSerialize: serialize_auth_ChangePasswordRequest,
    requestDeserialize: deserialize_auth_ChangePasswordRequest,
    responseSerialize: serialize_auth_AuthResponse,
    responseDeserialize: deserialize_auth_AuthResponse,
  },
  logout: {
    path: '/auth.AuthService/Logout',
    requestStream: false,
    responseStream: false,
    requestType: auth_pb.LogoutRequest,
    responseType: auth_pb.AuthResponse,
    requestSerialize: serialize_auth_LogoutRequest,
    requestDeserialize: deserialize_auth_LogoutRequest,
    responseSerialize: serialize_auth_AuthResponse,
    responseDeserialize: deserialize_auth_AuthResponse,
  },
  verifyToken: {
    path: '/auth.AuthService/VerifyToken',
    requestStream: false,
    responseStream: false,
    requestType: auth_pb.VerifyTokenRequest,
    responseType: auth_pb.VerifyTokenResponse,
    requestSerialize: serialize_auth_VerifyTokenRequest,
    requestDeserialize: deserialize_auth_VerifyTokenRequest,
    responseSerialize: serialize_auth_VerifyTokenResponse,
    responseDeserialize: deserialize_auth_VerifyTokenResponse,
  },
  uploadAvatar: {
    path: '/auth.AuthService/UploadAvatar',
    requestStream: false,
    responseStream: false,
    requestType: auth_pb.UploadAvatarRequest,
    responseType: auth_pb.UploadAvatarResponse,
    requestSerialize: serialize_auth_UploadAvatarRequest,
    requestDeserialize: deserialize_auth_UploadAvatarRequest,
    responseSerialize: serialize_auth_UploadAvatarResponse,
    responseDeserialize: deserialize_auth_UploadAvatarResponse,
  },
  getAvatar: {
    path: '/auth.AuthService/GetAvatar',
    requestStream: false,
    responseStream: false,
    requestType: auth_pb.GetAvatarRequest,
    responseType: auth_pb.GetAvatarResponse,
    requestSerialize: serialize_auth_GetAvatarRequest,
    requestDeserialize: deserialize_auth_GetAvatarRequest,
    responseSerialize: serialize_auth_GetAvatarResponse,
    responseDeserialize: deserialize_auth_GetAvatarResponse,
  },
};

exports.AuthServiceClient = grpc.makeGenericClientConstructor(AuthServiceService, 'AuthService');
