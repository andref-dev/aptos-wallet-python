# Aptos Wallet Python Service

This project is a small HTTP server that provides a lightweight test implementation of an Aptos wallet.

| ⚠️ This project is meant to be a learning exercise, **do not** use this for any production code ⚠️ | 
| --- |


# How to run this project

To run this project you just need to install its dependencies:
```
pip install -r requirements.txt
```

and then run the app:
```
flask run
```

Your application will be running on `http://localhost:5000`

# What this project does?

- Users
    - Creates aptos wallets and save them under the "User" entity
    - Allow users to be funded with APT tokens
    - Allow users to transfer APT tokens
- NFTs
    - Creates NTFs collections
    - Query information about the NTFs collections
    - Create tokens under a collection and transfer them to a user
    - Query information about the created tokens
    - Transfer tokens from created users
