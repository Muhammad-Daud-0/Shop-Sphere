<!-- @format -->

# Server - MongoDB Atlas Setup

This file explains how to configure the server to use MongoDB Atlas.

Environment variables

- `MONGODB_URI` (required) - full connection string for MongoDB Atlas. The server will refuse to start if this is not set.

Notes

- The project now uses `server/db.js` to centralize the mongoose connection and requires `MONGODB_URI` to be present. Do NOT commit Atlas credentials to version control. Use a deployment secret manager, CI/CD secrets, or environment variables on your host.

Quick test

1. Ensure you have Node.js installed.
2. From the repository root run:

   node server/server.js

3. You should see a console message `Connected to MongoDB (using MONGODB_URI)` and `Server running on port ...`.

How to get Atlas connection string

1. Create a free cluster at https://cloud.mongodb.com/.
2. In the cluster view click "Connect" → "Connect your application" and copy the connection string.
3. Replace `<password>` and any `<dbname>` placeholders, and store the URI in `MONGODB_URI`.

Security

- Use environment variables in production. Add `server/.env` to `.gitignore` if it isn't already. Use restricted database users and IP access lists in Atlas.
