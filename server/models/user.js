const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/ecommerce')

const userModel = mongoose.Schema({
    name: {
        type: String,
        required: true,
    },
    email: {
        type: String,
        required: true,
    },
    password: {
        type: String,
        required: true,
    },
    phone: {
        type: String,
        required: true,  
    },
    address: {
        type: {},
        required: true,
    },
    answer:{
        type: String,
        required: true,
    },
    role:{
        type: String,
        default: 0,
    },
    createdAt: {
        type: Date,
        default: Date.now
    },
}, {timestamps:true})

module.exports = mongoose.model('user', userModel);
