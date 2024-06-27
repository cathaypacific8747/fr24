from __future__ import annotations

from typing_extensions import Required, TypedDict


class User(TypedDict, total=False):
    id: Required[int]
    identity: str
    locale: str


class Features(TypedDict): ...  # useless anyway


class UserData(TypedDict, total=False):
    accessToken: None | str
    accountType: str
    countryCode: None | str
    dateExpires: int
    dateLastLogin: str
    features: Features
    hasConsented: bool
    hasPassword: bool
    idUser: int
    identity: str
    isActive: bool
    isAnonymousAccount: bool
    isLoggedIn: bool
    localeCode: str
    name: None
    oAuth: None
    oAuthType: None
    publicKey: None
    subscriptionKey: None | str
    tokenLogin: str
    typeSource: str


class Authentication(TypedDict, total=False):
    message: str
    msg: str
    response_code: int
    responseCode: int
    status: str
    success: bool
    token: str
    user: User
    features: Features
    userData: Required[UserData]


class UsernamePassword(TypedDict):
    username: str
    password: str


class TokenSubscriptionKey(TypedDict):
    subscriptionKey: str
    token: str
