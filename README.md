<!-- @format -->

# Shop-Sphere

Shop-Sphere is a comprehensive full-stack e-commerce platform that offers a modern, responsive user experience for browsing products, managing shopping carts, secure checkout, and features a dedicated admin dashboard for managing inventory, categories, users, and orders.

## Tech Stack

**Tech Stack:** MongoDB, Express.js, React, Node.js, Vite, Tailwind CSS, Axios, JWT, Bcrypt, Mongoose, and React Router.

## Features

- **User Authentication:** Secure login and registration with JWT and password hashing (bcrypt).
- **Product Management:** Admin can add, update, and delete products and categories.
- **Shopping Cart:** Users can add products to their cart, adjust quantities, and proceed to checkout.
- **Order Management:** Users can view their order history; Admins can view all orders, manage users, and update order statuses.
- **Search & Filtering:** Easily search for products and browse specific categories.
- **Responsive Design:** Fully responsive UI built with Tailwind CSS.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Node.js** (v16.x or higher recommended)
- **MongoDB** (Local instance or MongoDB Atlas cluster URI)
- **Git**

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Shop-Sphere
```

### 2. Environment Variables Setup

**Server Environment Variables (`server/.env`):**
Create a `.env` file in the `server` directory and configure the following variables:

```env
PORT=8080
MONGO_URL=your_mongodb_connection_string
JWT_SECRET=your_jwt_secret_key_here
```

**Client Environment Variables (`client/.env`):**
Create a `.env` file in the `client` directory to connect the frontend to the backend API:

```env
# Change this if your server is hosted elsewhere or on a different port
VITE_API_URL=http://localhost:8080
```

### 3. Installation

Install the Node modules for both the server and the frontend client.

**For the Backend (Server):**

```bash
cd server
npm install
```

**For the Frontend (Client):**

```bash
cd ../client
npm install
```

### 4. Running the Application

You will need two separate terminal windows/tabs to run the client and the server simultaneously.

**Start the Backend Server:**

```bash
# Open terminal #1
cd server
npm start
# Or for development with live-reloading:
npx nodemon server.js
```

**Start the Frontend Client:**

```bash
# Open terminal #2
cd client
npm run dev
```

The Client should now be accessible at `http://localhost:5173` (default for Vite) and connecting to the Server at `http://localhost:8080`.

## Project Structure Overview

- **/client**: Contains the React frontend code (Components, Pages, Context API hooks, React Router configurations).
- **/server**: Contains backend logical code (Express framework, MongoDB Mongoose models, Middlewares, API routes, Controllers).
