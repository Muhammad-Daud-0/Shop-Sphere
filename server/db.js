/** @format */

const mongoose = require("mongoose");
const dotenv = require("dotenv");

dotenv.config();

const uri = process.env.MONGODB_URI || process.env.MONGO_URI;

if (!uri) {
	console.error(
		"FATAL: Missing MONGODB_URI. Set the MONGODB_URI environment variable to your MongoDB Atlas connection string."
	);
	process.exit(1);
}

const connectDB = async () => {
	try {
		await mongoose.connect(uri);
		console.log("Connected to MongoDB (using MONGODB_URI)");
	} catch (err) {
		console.error("MongoDB connection error:", err.message);
		process.exit(1);
	}
};

module.exports = connectDB;
