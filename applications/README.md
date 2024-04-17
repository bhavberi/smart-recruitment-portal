# User management Service Codebase

----

For checking out the docs for the APIs, please setup and start the service using main docker-compose configuration. The, go to the URL -> 

[http://localhost/api/users/docs/](http://localhost/api/users/docs#/)

---

<br/>

## APIs

### **Tag - General**

> Root path - `localhost/api/`

- `/` _[GET]_ -> For checking the running status of the backend.

### **Tag - User**

> Root path - `localhost/api/user/`

- `/login` _[POST]_ -> User Login using `username` and `password`. It sets the authorization cookie. Can also send `email` in the variable `username`.

- `/register` _[POST]_ -> New User Registration using the fields of the [User](#user) Model. It sets the authorization cookie.

- `/logout` _[POST]_ -> User logout endpoint. Doesn't take any input.

- `/details` _[GET]_ -> Returns user details, based on the authorization cookie. Requires user to be logged in.

- `/change-password` _[POST]_ -> Change currently logged in user password. Takes current password and new password. Requires user to be logged in.

- `/edit` _[PUT]_ -> Edit user details using the fields of the [User](#user) Model. Requires user to be logged in.

----

<br/>

## Models

> ### _User_

- username: string - Unique username (Alphanumeric only)
- email: string -  Valid email (Unique only)
- contact: string - Valid Phone Number
- full_name: string - Full Name of the user
- password: string - Valid Password (Stored in hashed form in db for security)

